"""Authored planning controls, not target-project reproductions or model trials.

See evaluation/proposed-checks.md for the rejected and corrected handoffs.
"""

from pathlib import Path
import sqlite3
import threading
import unittest


def snapshot_path(role, minimum_size):
    """Authored dispatch: owners bypass snapshots; size one is inadmissible."""
    if minimum_size < 2:
        raise ValueError("minimum_size must be at least two")
    if role == "owner":
        return "direct"
    if minimum_size == 1:
        return "fallback"
    return "snapshot"


class ProposedCheckControls(unittest.TestCase):
    def test_nullable_operand_reaches_boundary_and_distinguishes_wrong_rewrite(self):
        with sqlite3.connect(":memory:") as connection:
            connection.execute("CREATE TABLE readings (id TEXT PRIMARY KEY NOT NULL, value INTEGER)")
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute("INSERT INTO readings VALUES (NULL, 1)")
            connection.executemany("INSERT INTO readings VALUES (?, ?)",
                                   [("a", None), ("b", 1), ("c", 2)])
            def selected(predicate):
                return connection.execute(f"SELECT id FROM readings WHERE {predicate} ORDER BY id").fetchall()
            # The original PK-only recipe cannot distinguish the NULL rewrite.
            self.assertEqual(selected("NOT (id = 'b')"), selected("id IS NOT 'b'"))
            self.assertEqual(selected("NOT (value = 1)"), [("c",)])
            self.assertEqual(selected("value IS NOT 1"), [("a",), ("c",)])
            # An ordinary SQL inequality is a valid alternate implementation.
            self.assertEqual(selected("value <> 1"), [("c",)])

    def test_role_selects_claimed_snapshot_branch(self):
        self.assertEqual(snapshot_path("owner", 2), "direct")
        self.assertEqual(snapshot_path("reader", 2), "snapshot")

    def test_minimum_size_guard_refutes_fallback_lead(self):
        with self.assertRaises(ValueError):
            snapshot_path("reader", 1)
        for size in (2, 3, 100):
            self.assertEqual(snapshot_path("reader", size), "snapshot")

    def test_interleaving_rejects_torn_snapshot_and_accepts_valid_repairs(self):
        for implementation in ("torn", "atomic", "serialized"):
            with self.subTest(implementation=implementation):
                state = [0, 0]  # Contract: generation and payload must agree.
                lock = threading.Lock()
                paused, release = threading.Event(), threading.Event()
                attempted, committed = threading.Event(), threading.Event()
                snapshots, errors = [], []

                def pause():
                    paused.set()
                    if not release.wait(10):
                        errors.append("snapshot pause was not released")

                def snapshot():
                    if implementation == "serialized":
                        with lock:
                            generation = state[0]
                            pause()
                            snapshots.append((generation, state[1]))
                    elif implementation == "atomic":
                        with lock:
                            captured = tuple(state)
                        pause()
                        snapshots.append(captured)
                    else:
                        generation = state[0]
                        pause()
                        snapshots.append((generation, state[1]))

                def refresh():
                    attempted.set()
                    with lock:
                        state[:] = [1, 1]
                    committed.set()

                reader = threading.Thread(target=snapshot, daemon=True)
                writer = threading.Thread(target=refresh, daemon=True)
                reader.start()
                try:
                    self.assertTrue(paused.wait(2), "snapshot never reached pause")
                    writer.start()
                    self.assertTrue(attempted.wait(2), "refresh never started")
                    overlapped = committed.wait(2)
                finally:
                    # Release even if refresh blocks or a harness assertion fails.
                    release.set()
                    reader.join(2)
                    if writer.ident is not None:
                        writer.join(2)
                self.assertFalse(reader.is_alive(), "snapshot completion unknown")
                self.assertFalse(writer.is_alive(), "refresh completion unknown")
                self.assertEqual(errors, [])
                self.assertTrue(committed.is_set())
                if implementation == "serialized":
                    self.assertFalse(overlapped)  # Old harness would wait forever here.
                else:
                    self.assertTrue(overlapped, "schedule not reached; harness inconclusive")
                self.assertEqual(len(snapshots), 1)
                generation, payload = snapshots[0]
                self.assertEqual(generation == payload, implementation != "torn")
                self.assertEqual(state, [1, 1])

    def test_direct_document_contradiction_needs_only_source_inspection(self):
        fixture = Path(__file__).resolve().parents[1] / "evaluation/fixtures/doc-drift"
        self.assertIn("retries failed requests twice by default", (fixture / "README.md").read_text())
        self.assertIn("def __init__(self, retry_count=0):", (fixture / "client.py").read_text())
        # No import or execution of the client is needed to identify this mismatch.


if __name__ == "__main__":
    unittest.main()
