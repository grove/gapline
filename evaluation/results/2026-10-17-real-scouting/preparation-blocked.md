# Larger-repository scouting evaluation: blocked preparation

**Decision: INCONCLUSIVE — NOT RUN.** No audit, expectation-curator, or reviewer
sessions were launched. This is a permission-blocker record, not negative
effectiveness evidence. Issue #6 remains open; #7 remains closed.

The controller read issue #6, PRs #11/#12, the current evaluation protocols,
the existing pilot/refinement launchers, restricted inspection adapter, review
masking, and their tests. Local `main` and `origin/main` both identified
`b4d1e1c86802f16fe996c68eb33940cc298ea82c`. Production files were not changed.

## Preparation completed

Four public, licensed default-HEAD snapshots were fetched once, without
selecting known defects. These projects are absent from the prior retained
Gapline evaluation cases. Model training familiarity cannot be excluded.
No project code, tests, builds, or dependencies were executed or installed.

| Proposed case | Repository | Exact commit | Text files / bytes | License |
| --- | --- | --- | --- | --- |
| r1 | [getsops/sops](https://github.com/getsops/sops) | `e39ca97b6209f9132ea40d22beb37d796060cb32` | 154 / 1,096,210 | MPL-2.0 |
| r2 | [litestar-org/advanced-alchemy](https://github.com/litestar-org/advanced-alchemy) | `e051a5de1a008b70f2d67b416e236a8c59e69433` | 385 / 6,039,744 | MIT |
| r3 | [pyeventsourcing/eventsourcing](https://github.com/pyeventsourcing/eventsourcing) | `bf665955d9243e728aaaa5bb62ac63b9cfe5ec19` | 335 / 2,394,915 | BSD-3-Clause |
| r4 | [requests-cache/requests-cache](https://github.com/requests-cache/requests-cache) | `abe06a833cfb35a885f371d1b3db1199b3a968b5` | 150 / 1,535,586 | BSD-2-Clause |

[Prepared identities](prepared-snapshots.json) retain exact per-file hashes,
sizes, and excluded binary paths. The temporary source trees are at
`/private/tmp/gapline-scout-real/snapshots/r1` through `r4`; they are not committed
snapshots. Suitability, independent expectations, and the new protocol were
**not frozen**. Do not launch audits from this preparation record.

The intended comparison was current main versus main with only PR #11's Scout
paragraph and optional scouting recipe restored. The existing shortened Probe
verification guidance would be identical. Intended budgets were 180 seconds
and 12 inspection calls, using the existing restricted host, eight fresh audit
attempts, counterbalanced A/B order, and separate anonymized review. These are
unexecuted plans, not observed controls or frozen experiment inputs.

## Permission blocker

`git switch -c evaluate/real-scouting` failed with exit 128:

```text
fatal: cannot lock ref 'refs/heads/evaluate/real-scouting': Unable to create '/Users/grove/projects/gapline/.git/refs/heads/evaluate/real-scouting.lock': Operation not permitted
```

The supplied environment grants only read access to `.git`. User AGENTS.md
requires ordinary local Git operations to remain inside the sandbox, and the
task explicitly requires stopping on a permissions blocker. No outside-sandbox
local Git mutation or GitHub checkout workaround was attempted. There was no
automatic approval-review rejection; this was a local sandbox denial.

The smallest unblock is a checkout whose local Git metadata permits ordinary
branch/commit operations within the sandbox, or an explicit revision of that
boundary. The evaluation must still freeze and validate its inputs and host
controls before any paid audits.

## Evidence, overhead, and disposition

Retained: [blocker receipt](blocker.json), [issue #6](issue-6-before.json),
[issue #7](issue-7-before.json), [PR #12](pr-12.json), and
[PR #11's original diff](pr-11.diff).

- Audit reports, probe-quality findings, false positives, misses, abstention,
  and verification-effort judgments: **NOT RUN**.
- Audit/curator/reviewer timeouts and failures: no attempts. The failed local
  branch command is a preparation failure, not a failed audit.
- New paid Codex CLI usage: none. Controller tokens, money, and total controller
  elapsed time are unavailable. Four successful public snapshot fetches and
  local text preparation are preparation overhead only.
- GitHub inspection succeeded. Authentication and actual permission controls
  for new Codex workers were not tested; previous host receipts cannot certify
  this unrun cohort.
- No effectiveness comparison supports restoring or modifying Scout. Retain
  current production pending a completed controlled experiment. This is a
  procedural hold, not a KEEP CURRENT effectiveness result.

Issue #6's larger-repository acceptance gap remains unsatisfied. Leave it open
and report the blocker. Leave #7 closed and preserve its verification guidance.
These files remain local and uncommitted because of the same boundary; an
issue comment must not claim that new evidence is published in GitHub source.

[Issue #6 was updated](https://github.com/grove/gapline/issues/6#issuecomment-6233888523)
with the blocker, exact proposed pins, and the absence of audit evidence.
Post-update receipts confirm [#6 is open](issue-6-after.json) and
[#7 is closed](issue-7-after.json). Local validation checked every prepared
file hash, local evidence link, and JSON record, and confirmed production
skill bytes match HEAD. The development suite and CI were not run.
