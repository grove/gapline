"""Evaluator only: contract checks for these authored snapshots, not worker input.

Run: python -m unittest discover -s evaluation/cohorts/pilot-1 -p oracle_test.py -v
The q1 contract test has one declared expected failure. Its separate witness
checks the exact planted behavior, so an unrelated exception is not enough.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / "manifest.json").read_text())


def load_case(case_id, filename):
    case = next(case for case in MANIFEST["cases"] if case["id"] == case_id)
    record = next(item for item in case["files"] if item["path"] == filename)
    path = ROOT / "cases" / case_id / filename
    data = path.read_bytes()
    if len(data) != record["size"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
        raise AssertionError(f"source identity changed: {case_id}/{filename}")
    name = f"pilot_1_{case_id}_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class SourceIdentity(unittest.TestCase):
    def test_all_worker_files_match_predeclared_manifest(self):
        self.assertEqual([case["id"] for case in MANIFEST["cases"]], ["q1", "q2", "q3"])
        for case in MANIFEST["cases"]:
            root = ROOT / "cases" / case["id"]
            actual = sorted(
                str(path.relative_to(root)) for path in root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            )
            self.assertEqual(actual, sorted(item["path"] for item in case["files"]))
            for item in case["files"]:
                data = (root / item["path"]).read_bytes()
                self.assertEqual(len(data), item["size"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])


class ArtifactOracle(unittest.TestCase):
    def interrupted_first_publish(self, root):
        module = load_case("q1", "artifacts.py")
        store = module.ArtifactStore(root)
        with patch.object(module.os, "replace", side_effect=OSError("injected before commit")):
            with self.assertRaises(OSError):
                store.publish(b"unapproved configuration")
        self.assertIsNone(store.read())
        self.assertFalse((Path(root) / "CURRENT").exists())
        return module

    @unittest.expectedFailure
    def test_uncommitted_first_generation_must_remain_invisible_on_reopen(self):
        with tempfile.TemporaryDirectory() as root:
            module = self.interrupted_first_publish(root)
            self.assertIsNone(module.ArtifactStore(root).read())

    def test_exact_known_failure_witness(self):
        with tempfile.TemporaryDirectory() as root:
            module = self.interrupted_first_publish(root)
            self.assertEqual(module.ArtifactStore(root).read(), b"unapproved configuration")
            self.assertEqual((Path(root) / "CURRENT").read_text(), "1\n")


class LeaseOracle(unittest.TestCase):
    def test_replay_after_completion_is_not_another_operation(self):
        queue = load_case("q2", "leases.py").BatchQueue()
        job = queue.enqueue("batch/42/item/9", {"item": 9})
        first = queue.reserve("worker", 0, 5)
        self.assertTrue(queue.finish(job, first["token"], {"saved": 9}, 1))
        self.assertEqual(queue.enqueue("batch/42/item/9", {"item": 9}), job)
        self.assertEqual(queue.inspect(job)["state"], "done")
        self.assertIsNone(queue.reserve("worker", 2, 5))
        another = queue.enqueue("batch/42/item/9/revision/2", {"item": 9})
        self.assertNotEqual(another, job)
        self.assertEqual(queue.reserve("worker", 3, 5)["job_id"], another)

    def test_same_owner_does_not_make_old_token_valid(self):
        queue = load_case("q2", "leases.py").BatchQueue()
        job = queue.enqueue("operation", {})
        old = queue.reserve("worker", 0, 5)
        self.assertFalse(queue.finish(job, old["token"], "late", 5))
        new = queue.reserve("worker", 5, 5)
        self.assertFalse(queue.finish(job, old["token"], "late", 6))
        self.assertTrue(queue.finish(job, new["token"], "fresh", 6))
        self.assertEqual(queue.inspect(job)["result"], "fresh")


class ChangeOracle(unittest.TestCase):
    def test_between_page_writes_wait_for_next_pull_without_being_skipped(self):
        feed = load_case("q3", "changes.py").ChangeFeed()
        feed.put("a", {"value": 1})
        feed.put("b", {"value": 2})
        feed.delete("a")
        first = feed.begin(0, 1)
        feed.put("c", {"value": 3})
        middle = feed.resume(first.continuation, 1)
        last = feed.resume(middle.continuation, 1)
        self.assertEqual(first.events + middle.events + last.events, (
            (1, "a", {"value": 1}), (2, "b", {"value": 2}), (3, "a", None),
        ))
        self.assertIsNone(last.continuation)
        self.assertEqual(last.checkpoint, 3)
        later = feed.begin(last.checkpoint, 10)
        self.assertEqual(later.events, ((4, "c", {"value": 3}),))
        self.assertEqual(later.checkpoint, 4)

    def test_compaction_expiration_is_explicit_on_continuation(self):
        module = load_case("q3", "changes.py")
        feed = module.ChangeFeed()
        for number in range(3):
            feed.put(str(number), {})
        page = feed.begin(0, 1)
        feed.compact(2)
        with self.assertRaises(module.CursorExpired):
            feed.resume(page.continuation, 1)
        self.assertEqual(feed.begin(2, 1).events, ((3, "2", {}),))


if __name__ == "__main__":
    unittest.main()
