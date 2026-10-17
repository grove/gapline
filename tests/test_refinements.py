"""Non-billable checks of evaluation isolation and factorial separation."""

from pathlib import Path
import tempfile
import unittest
import sys
import json
import subprocess

EVALUATION = Path(__file__).resolve().parents[1] / "evaluation"
sys.path.insert(0, str(EVALUATION))
from inspect_server import Inspector
from run_refinements import schedule, skill_variants
from review_refinements import mask


class RefinementTests(unittest.TestCase):
    def test_review_mask_preserves_finding_and_removes_origin_and_cost(self):
        finding = "10/10 becomes 50%; alternative is 100%. PROPOSED — NOT RUN."
        report = "Gapline audit\nBudget used: 3 inspection calls, 100 tokens\n" + finding
        report += "\nInspection tool: **3 calls**, no execution."
        report += "\n/private/tmp/gapline-refinement-workers/trial-01/repository/editor.py:12"
        masked = mask(report)
        self.assertIn(finding, masked)
        self.assertIn("editor.py:12", masked)
        for hidden in ("Gapline", "100 tokens", "3 inspection calls", "3 calls", "trial-01"):
            self.assertNotIn(hidden, masked)

    def test_frozen_cohort_and_oracle(self):
        from run_pilot import identity
        cohort = EVALUATION / "cohorts/refinements-1"
        actual = identity(cohort)
        actual.pop("frozen.json")
        self.assertEqual(actual, json.loads((cohort / "frozen.json").read_text()))
        result = subprocess.run([sys.executable, "-B", str(cohort / "oracle.py")],
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_mcp_transport_initializes_and_records_only_allowlisted_reads(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repository"
            root.mkdir()
            (root / "README.md").write_text("contract")
            log = Path(temporary) / "calls.jsonl"
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                    "name": "inspect", "arguments": {"operation": "read", "paths": ["README.md"]}}},
            ]
            result = subprocess.run([sys.executable, "-B", str(EVALUATION / "inspect_server.py"), str(root), str(log)],
                                    input="\n".join(map(json.dumps, messages)) + "\n", text=True,
                                    capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            replies = list(map(json.loads, result.stdout.splitlines()))
            self.assertEqual([reply["id"] for reply in replies], [1, 2, 3])
            self.assertEqual(replies[2]["result"]["content"][0]["text"], "README.md:1: contract")
            self.assertEqual(len(log.read_text().splitlines()), 1)

    def test_factorial_variants_and_balanced_schedule(self):
        variants = skill_variants()
        self.assertEqual(len(set(schedule())), 20)
        self.assertEqual({arm for _, arm in schedule()}, set("ABCD"))
        for arm, files in variants.items():
            self.assertEqual("## Verification-ready next actions" in files["SKILL.md"], arm in "CD")
            self.assertEqual("current user promise" in files["SKILL.md"], arm in "BD")
            self.assertIn("up to **three leads**", files["SKILL.md"])
            self.assertIn("Stay **read-only**", files["SKILL.md"])
        for position in range(4):
            self.assertEqual({schedule()[case * 4 + position][1] for case in range(4)}, set("ABCD"))

    def test_inspection_denies_outside_reads_execution_and_over_budget(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "file.py").write_text("original\n")
            inspector = Inspector(root, limit=6)
            (root / "file.py").write_text("changed\n")
            self.assertEqual(inspector.inspect("read", ["file.py"]), "file.py:1: original")
            for path in ("../secret", "/etc/passwd", "file.py/../file.py"):
                with self.assertRaises(ValueError):
                    inspector.inspect("read", [path])
            with self.assertRaises(ValueError):
                inspector.inspect("execute", ["file.py"])
            self.assertEqual(inspector.inspect("search", query="original"), "file.py:1: original")
            with self.assertRaisesRegex(ValueError, "budget"):
                inspector.inspect("list")
            (root / "link").symlink_to(root / "file.py")
            with self.assertRaises(ValueError):
                Inspector(root)


if __name__ == "__main__":
    unittest.main()
