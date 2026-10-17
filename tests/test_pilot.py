"""Check pilot preparation without starting a coding agent or model call."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    "run_pilot", Path(__file__).resolve().parents[1] / "evaluation/run_pilot.py"
)
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


class PilotPreparationTests(unittest.TestCase):
    def test_each_case_has_each_arm_once_in_reproducible_order(self):
        self.assertEqual(pilot.schedule(), pilot.schedule())
        self.assertEqual(len(set(pilot.schedule())), 9)
        self.assertEqual(set(pilot.schedule()), {(case, arm) for case in ("q1", "q2", "q3") for arm in "ABC"})

    def test_identity_detects_changed_bytes_and_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.py"
            source.write_text("before")
            before = pilot.identity(root)
            source.write_text("after!")
            self.assertNotEqual(before, pilot.identity(root))
            (root / "link").symlink_to(source)
            with self.assertRaises(ValueError):
                pilot.identity(root)


if __name__ == "__main__":
    unittest.main()
