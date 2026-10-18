"""Package checks for Gapline and regression tests for the install verifier.

Instruction-presence checks only detect accidentally omitted text. They do NOT
establish agent compliance, read-only isolation, host activation, or audit quality.
The real installer smoke and matched agent evaluation are separate checks.
"""

from pathlib import Path
import re
import shutil
import tempfile
import unittest

from scripts.check_install import (
    InstallCheckError,
    check_relative_links,
    payload,
    verify_payload,
)


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "gapline-audit" / "SKILL.md"
README_PATH = ROOT / "README.md"
SKILL_DIRECTORY = SKILL_PATH.parent


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

    def test_inspection_and_evidence_limits_are_documented(self):
        for statement in (
            "read-only",
            "untrusted evidence, not instructions",
            "Project code, tests, and builds executed: NONE",
            "NOT RUN",
        ):
            with self.subTest(statement=statement):
                self.assertIn(statement.lower(), self.skill.lower())

    def test_optional_delegation_preserves_limits_and_review(self):
        # Static instruction guardrails, not proof of host subagent behavior.
        for term in (
            "One agent is the default",
            "host already provides subagents",
            "combined",
            "read-only",
            "no-execution",
            "not independent proof",
            "verify material source references",
            "disprove",
            "do not spawn agents",
            "do not delegate further",
        ):
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.skill.lower())

    def test_compact_verification_guidance_keeps_scope_bounded(self):
        # Presence-only guard; effectiveness requires independent matched trials.
        for term in (
            "For a consequential unresolved claim",
            "relevant setup",
            "observable result supporting the concern",
            "weaken or refute",
            "Clarify an unknown requirement",
            "schema constraints, caller privileges, transaction/session rules",
            "selected path",
            "blocking or serialization",
            "Unknown harness behavior remains an evidence gap",
            "without upgrading the finding's evidence level",
            "routine cases and direct source/document contradictions",
            "three substantive findings",
            "PROPOSED — NOT RUN",
        ):
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.skill.lower())

    def test_one_canonical_skill_entry_point(self):
        self.assertFalse((ROOT / "SKILL.md").exists(), "A root skill would shadow the canonical package")
        self.assertEqual(list(ROOT.glob("*/SKILL.md")), [SKILL_PATH])

    def test_shipped_references_are_present_and_self_contained(self):
        self.assertIn("references/investigation.md", self.skill)
        self.assertTrue((SKILL_DIRECTORY / "references" / "investigation.md").is_file())
        check_relative_links(SKILL_DIRECTORY)

    def test_payload_excludes_repository_development_files(self):
        excluded = {".git", "__pycache__", "node_modules", "evaluation", "tests"}
        for relative in payload(SKILL_DIRECTORY):
            with self.subTest(path=relative):
                self.assertFalse(excluded.intersection(Path(relative).parts))

    def test_license_is_shipped_unchanged(self):
        self.assertEqual((SKILL_DIRECTORY / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())

    def test_readme_points_to_real_skill_and_evaluation(self):
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("gapline-audit/SKILL.md", readme)
        self.assertIn("evaluation/README.md", readme)
        self.assertIn("npx skills@latest add grove/gapline", readme)
        self.assertIn("docs/ADVANCED.md", readme)
        self.assertIn("docs/FAQ.md", readme)
        self.assertNotIn("python -m unittest discover -s tests -v", readme)
        details = (ROOT / "docs" / "ADVANCED.md").read_text(encoding="utf-8")
        self.assertIn("python -m unittest discover -s tests -v", details)
        self.assertTrue((ROOT / "DESIGN.md").is_file())
        self.assertTrue((ROOT / "IMPLEMENTATION.md").is_file())


class InstallVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="gapline-package-test-", dir=ROOT.parent)
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.source = self.work / "source"
        self.installed = self.work / "installed"
        (self.source / "references").mkdir(parents=True)
        (self.source / "SKILL.md").write_text(
            "---\nname: example\ndescription: Example package\n---\n"
            "Read [guide](references/guide.md#details).\n", encoding="utf-8",
        )
        (self.source / "references" / "guide.md").write_text("# Details\n", encoding="utf-8")
        shutil.copytree(self.source, self.installed)

    def test_complete_copy_includes_references(self):
        self.assertEqual(verify_payload(self.source, self.installed), 2)

    def test_missing_support_file_fails(self):
        (self.installed / "references" / "guide.md").unlink()
        with self.assertRaisesRegex(InstallCheckError, "missing=.*references/guide.md"):
            verify_payload(self.source, self.installed)

    def test_changed_support_file_fails(self):
        (self.installed / "references" / "guide.md").write_text("Stale instructions\n", encoding="utf-8")
        with self.assertRaisesRegex(InstallCheckError, "changed=.*references/guide.md"):
            verify_payload(self.source, self.installed)

    def test_unintended_installed_file_fails(self):
        (self.installed / "maintainer-notes.md").write_text("Not shipped\n", encoding="utf-8")
        with self.assertRaisesRegex(InstallCheckError, "extra=.*maintainer-notes.md"):
            verify_payload(self.source, self.installed)

    def test_missing_entry_point_fails(self):
        (self.installed / "SKILL.md").unlink()
        with self.assertRaisesRegex(InstallCheckError, "Missing skill entry point"):
            verify_payload(self.source, self.installed)

    def test_broken_relative_link_fails_even_if_files_were_copied(self):
        (self.installed / "SKILL.md").write_text("[Missing](references/missing.md)\n", encoding="utf-8")
        with self.assertRaisesRegex(InstallCheckError, "Missing linked file"):
            check_relative_links(self.installed)

    def test_link_to_repository_file_outside_package_fails(self):
        (self.work / "README.md").write_text("Only in the source repository\n", encoding="utf-8")
        (self.installed / "SKILL.md").write_text("[Readme](../README.md)\n", encoding="utf-8")
        with self.assertRaisesRegex(InstallCheckError, "Link escapes installed package"):
            check_relative_links(self.installed)

    def test_reference_style_links_are_checked(self):
        (self.installed / "SKILL.md").write_text("Read [guide][g].\n\n[g]: missing.md\n", encoding="utf-8")
        with self.assertRaisesRegex(InstallCheckError, "Missing linked file"):
            check_relative_links(self.installed)

    def test_external_links_fragments_and_fenced_examples_are_not_dependencies(self):
        (self.installed / "SKILL.md").write_text(
            "[Web](https://example.com/readme.md) [Here](#heading)\n"
            "```markdown\n[Example](not-a-shipped-file.md)\n```\n", encoding="utf-8",
        )
        check_relative_links(self.installed)


if __name__ == "__main__":
    unittest.main()
