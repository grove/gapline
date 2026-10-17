"""Check cohort bytes, sole skill difference, order and masking without model calls."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import copy
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evaluation"))
from run_real_scouting import (COHORT, SCHEDULE, QUALIFICATION, accept_host, anonymize,
                               cases, freeze, normalize_argv, qualified_reference, supply)
from run_pilot import identity
from run_refinements import launch


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

    def test_over_budget_curator_cannot_be_promoted_to_frozen_expectations(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for suffix in ("report.md", "host.json"):
                (output / f"curator-1-{suffix}").write_text("unaccepted")
            (output / "curator-1-run.json").write_text(json.dumps({
                "status": "COMPLETED", "token_budget_met": False}))
            with (patch("run_real_scouting.OUTPUT", output), patch("run_real_scouting.check_setup"),
                  self.assertRaisesRegex(ValueError, "unqualified")):
                freeze()
            self.assertFalse((output / "frozen.json").exists())

    def test_explicit_ceiling_counts_cached_input_once_and_preserves_legacy_default(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "repository"
            project.mkdir()
            def fake_process(argv, **kwargs):
                class Process:
                    returncode = 0
                    def communicate(self, prompt, timeout):
                        kwargs["stdout"].write(json.dumps({"type": "turn.completed", "usage": {
                            "input_tokens": 900000, "cached_input_tokens": 800000, "output_tokens": 100000}}) + "\n")
                return Process()
            with patch("run_refinements.subprocess.Popen", side_effect=fake_process) as process:
                original = launch("legacy", project, root, "check")
                revised = launch("v2", project, root, "check", token_limit=1000000, strict_tools=True)
            self.assertEqual(original["token_limit"], 250000)
            self.assertFalse(original["token_budget_met"])
            self.assertTrue(revised["token_budget_met"])
            self.assertEqual(revised["token_limit"], 1000000)
            argv = process.call_args.args[0]
            for setting in ("features.code_mode_only=true", "features.code_mode_only_strict_3p_tools=true", "features.goals=false"):
                self.assertIn(setting, argv)

    def test_qualified_native_visibility_is_accepted_but_use_and_changes_are_rejected(self):
        reference = qualified_reference()
        valid = {"turn_contexts": [reference["context"]], "experimental_scout_in_host_instructions": False,
                 "expectations_in_host_instructions": False, "available_tool_names": reference["available_tool_names"],
                 "tool_names": ["exec", "mcp__inspection__inspect"], "forbidden_dispatch": False,
                 "mcp_calls": [{"server": "inspection", "tool": "inspect"}]}
        accept_host(valid, reference)  # Visible apply_patch/resources are qualified, never audit permissions.
        changes = [
            {"tool_names": ["exec", "apply_patch"]},
            {"tool_names": ["exec", "read_mcp_resource"]},
            {"mcp_calls": [{"server": "inspection", "tool": "read_mcp_resource", "status": "failed"}]},
            {"mcp_calls": [{"server": "other", "tool": "inspect"}]},
            {"available_tool_names": reference["available_tool_names"] + ["exec_command"]},
            {"forbidden_dispatch": True},
            {"expectations_in_host_instructions": True},
        ]
        changed_context = copy.deepcopy(reference["context"])
        changed_context["sandbox_policy"] = {"type": "workspace-write"}
        changes.append({"turn_contexts": [changed_context]})
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                accept_host(valid | change, reference)

    def test_invocation_normalization_preserves_security_and_server_identity(self):
        reference = json.loads((QUALIFICATION / "probe-input.json").read_text())["argv"]
        normalized = normalize_argv(reference)
        changed = reference.copy()
        changed[changed.index("read-only")] = "workspace-write"
        self.assertNotEqual(normalize_argv(changed), normalized)
        changed = reference.copy() + ["-c", 'mcp_servers.extra.command="unsafe"']
        self.assertNotEqual(normalize_argv(changed), normalized)
        changed = reference.copy()
        changed[changed.index("-C") + 1] = "/different/source"
        with self.assertRaisesRegex(ValueError, "root mismatch"):
            normalize_argv(changed)

    def test_blinding_preserves_substantive_token_findings(self):
        finding = "Access tokens can be logged at client.py:21; PROPOSED — NOT RUN."
        self.assertIn(finding, anonymize("Tokens: 12345\n" + finding))
        self.assertNotIn("12345", anonymize("Tokens: 12345\n" + finding))
