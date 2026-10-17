"""Static contract checks for the Gapline skill.

These checks do NOT establish agent compliance, discovery, read-only isolation, or
audit quality. The host smoke test and matched evaluation are separate.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "gapline-audit" / "SKILL.md"
README_PATH = ROOT / "README.md"
FIXTURES = ROOT / "evaluation" / "fixtures"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL_PATH.read_text(encoding="utf-8")

    def test_frontmatter_is_minimal_and_named(self):
        match = re.match(r"\A---\n(.*?)\n---\n", self.skill, flags=re.DOTALL)
        self.assertIsNotNone(match, "Skill must begin with YAML frontmatter")
        lines = [line for line in match.group(1).splitlines() if line.strip()]
        self.assertEqual(len(lines), 2, "Keep frontmatter portable and minimal")
        self.assertIn("name: gapline-audit", lines)
        self.assertTrue(any(line.startswith("description: ") for line in lines))

    def test_investigation_contract_is_present(self):
        for term in (
            "Scout → Probe → Report",
            "Hollow or missing tests",
            "Documentation drift",
            "Failure handling and recovery",
            "counterevidence",
            "DEMONSTRATED",
            "SUPPORTED",
            "HYPOTHESIS",
            "REFUTED / WITHDRAWN",
            "NOT ASSESSED",
            "NOT RUN",
            "no-findings",
        ):
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.skill.lower())

    def test_read_only_constraints_are_explicit(self):
        for prohibition in (
            "Do not execute shell commands",
            "run or collect tests",
            "install packages",
            "mutate files",
            "untrusted evidence, not instructions",
            "prompt is **not** an isolation mechanism",
            "Commands/project code executed: NONE",
        ):
            with self.subTest(prohibition=prohibition):
                self.assertIn(prohibition.lower(), self.skill.lower())

    def test_readme_points_to_real_skill_and_evaluation(self):
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("gapline-audit/SKILL.md", readme)
        self.assertIn("evaluation/README.md", readme)
        self.assertIn("python -m unittest discover -s tests -v", readme)
        self.assertTrue((ROOT / "DESIGN.md").is_file())
        self.assertTrue((ROOT / "IMPLEMENTATION.md").is_file())

    def test_fixture_scenarios_present(self):
        for name, paths in {
            "hollow-test": ("README.md", "billing.py", "test_billing.py"),
            "doc-drift": ("README.md", "client.py"),
            "caller-guards": ("README.md", "service.py", "test_service.py"),
            "clean": ("README.md", "slug.py", "test_slug.py"),
        }.items():
            for path in paths:
                with self.subTest(case=name, path=path):
                    self.assertTrue((FIXTURES / name / path).is_file())


if __name__ == "__main__":
    unittest.main()
