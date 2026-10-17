"""Exercise the documented Git reads against configured executable helpers.

This is a maintainer regression check in a disposable repository, not an audit
action or a claim that a skill prompt provides host isolation.
"""

import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name == "posix" and shutil.which("git"), "requires POSIX Git")
class GitInspectionTests(unittest.TestCase):
    def test_documented_revision_read_avoids_helpers_and_preserves_index(self):
        with tempfile.TemporaryDirectory(prefix="gapline-git-read-", dir=ROOT.parent) as directory:
            work = Path(directory)
            repository = work / "repository"
            repository.mkdir()
            environment = dict(os.environ)
            environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)

            def run(*arguments):
                return subprocess.run(
                    arguments, cwd=repository, env=environment, check=True,
                    capture_output=True, text=True, timeout=15,
                )

            run("git", "init", "--quiet")
            (repository / "tracked.txt").write_text("old value\n", encoding="utf-8")
            (repository / ".gitattributes").write_text("tracked.txt diff=sentinel filter=sentinel\n", encoding="utf-8")
            run("git", "add", ".")
            run(
                "git", "-c", "user.name=Gapline tests", "-c", "user.email=tests@example.invalid",
                "-c", "commit.gpgSign=false", "commit", "--quiet", "-m", "Test input",
            )
            expected_head = run("git", "rev-parse", "HEAD").stdout
            (repository / "tracked.txt").write_text("new value\n", encoding="utf-8")
            sentinel = work / "helper-ran"
            helper = work / "helper.sh"
            helper.write_text(
                "#!/bin/sh\n"
                f"printf 'helper\\n' >> {shlex.quote(str(sentinel))}\n"
                "printf 'token\\0'\n", encoding="utf-8",
            )
            helper.chmod(0o700)
            run("git", "config", "core.fsmonitor", str(helper))
            run("git", "config", "diff.external", str(helper))
            run("git", "config", "diff.sentinel.textconv", str(helper))
            clean_filter = work / "clean-filter.sh"
            clean_filter.write_text(
                "#!/bin/sh\n"
                f"printf 'clean-filter\\n' >> {shlex.quote(str(sentinel))}\n"
                "cat\n", encoding="utf-8",
            )
            clean_filter.chmod(0o700)
            run("git", "config", "filter.sentinel.clean", str(clean_filter))

            # An unprotected diff reaches fsmonitor. Disabling it still leaves
            # a separate clean-filter execution path in worktree comparisons.
            run("git", "--no-pager", "diff", "--no-ext-diff", "--no-textconv")
            self.assertIn("helper", sentinel.read_text(encoding="utf-8"))
            sentinel.unlink()
            for command in (
                ["status", "--short"],
                ["diff", "--no-ext-diff", "--no-textconv"],
            ):
                run("git", "--no-optional-locks", "-c", "core.fsmonitor=false", "--no-pager", *command)
                self.assertIn("clean-filter", sentinel.read_text(encoding="utf-8"))
                sentinel.unlink()

            index = repository / ".git" / "index"
            before = index.read_bytes()
            skill = (ROOT / "gapline-audit" / "SKILL.md").read_text(encoding="utf-8")
            commands = re.findall(r"`(git [^`]+)`", skill)
            self.assertTrue(commands, "Exercise the actual commands shipped in the skill")
            revision_output = None
            for command in commands:
                with self.subTest(command=command):
                    arguments = shlex.split(command)
                    result = run(*arguments)
                    if "rev-parse" in arguments:
                        revision_output = result.stdout
                    self.assertFalse(sentinel.exists(), "Inspection invoked a configured helper")
                    self.assertEqual(index.read_bytes(), before, "Inspection rewrote the index")
            self.assertEqual(revision_output, expected_head, "The permitted read must identify HEAD")


if __name__ == "__main__":
    unittest.main()
