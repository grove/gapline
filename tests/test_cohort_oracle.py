"""Retain the independently specified pilot distinctions as development checks."""

from pathlib import Path
import subprocess
import sys
import unittest


class CohortOracleTests(unittest.TestCase):
    def test_frozen_cases_and_evaluator_oracles(self):
        oracle = Path(__file__).resolve().parents[1] / "evaluation/cohorts/pilot-1/oracle_test.py"
        result = subprocess.run([sys.executable, "-B", str(oracle), "-v"], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
