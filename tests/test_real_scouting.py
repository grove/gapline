"""Check cohort bytes, sole skill difference, order and masking without model calls."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evaluation"))
from run_real_scouting import COHORT, SCHEDULE, anonymize, cases, supply
from run_pilot import identity


class RealScoutingTests(unittest.TestCase):
    def test_variants_restore_only_historical_scout_and_keep_current_probe(self):
        production = COHORT.parents[2] / "gapline-audit"
        for name in identity(COHORT / "skills/A"):
            original = (COHORT / "skills/A" / name).read_text()
            revised = (COHORT / "skills/B" / name).read_text()
            self.assertEqual(original, (production / name).read_text())
            historical = (COHORT.parent / "refinements-1/skills/D" / name).read_text()
            if name == "SKILL.md":
                addition = next(line + "\n" for line in historical.splitlines()
                                if line.startswith("   When choosing among leads,"))
                self.assertIn("make the next action concrete", revised)
                self.assertNotIn("## Verification-ready next actions", revised)
            elif name == "references/investigation.md":
                addition = historical[historical.index("## Picking a promising probe"):
                                      historical.index("## Making the next observation")]
                self.assertNotIn("## Making the next observation", revised)
            else:
                addition = ""
            self.assertEqual(revised.replace(addition, "", 1) if addition else revised, original)

    def test_archived_bytes_and_counterbalance(self):
        self.assertEqual(len(SCHEDULE), 8)
        self.assertEqual(len(set(SCHEDULE)), 8)
        self.assertEqual([arm for _, arm in SCHEDULE[::2]].count("A"), 2)
        with tempfile.TemporaryDirectory() as temporary:
            for case in cases():
                self.assertGreater(sum(f["size_bytes"] for f in case["files"].values()), 960000)
                self.assertNotIn("pg-trickle", case["repository"])
                supply(case, Path(temporary) / case["id"])

    def test_review_mask_preserves_claims_and_removes_method_and_telemetry(self):
        text = "Risk-guided scout guidance used.\nGapline\nBudget: 12 inspection calls\n"
        text += "/private/tmp/gapline-scout-real/workers/trial-02/repository/a.py:123: durable write missing. PROPOSED — NOT RUN."
        result = anonymize(text)
        self.assertIn("a.py:123: durable write missing. PROPOSED — NOT RUN.", result)
        for hidden in ("Risk-guided", "Gapline", "12 inspection calls", "trial-02"):
            self.assertNotIn(hidden, result)
