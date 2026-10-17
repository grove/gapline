# Larger real-repository scouting evaluation: preflight stopped

**Decision: INCONCLUSIVE. No A/B audits ran.** The first independent expectation
session exceeded the frozen token ceiling. Its host inventory also failed the
protocol's stricter tool restriction. The controller stopped before curator 2,
all eight audits, and both reviewers. These are preflight failures, not negative
evidence about scouting effectiveness. **Keep production unchanged; leave #6
open and #7 closed.**

## What was fixed and frozen

The earlier [local Git blocker](preparation-blocked.md) was resolved by the
user's explicit authorization. It is retained as history, not the active blocker.
The [protocol](../../real-scouting-v1.md), [cohort/archives](../../cohorts/real-scouting-1/README.md),
variants, adapter extension, tests and [runner](../../run_real_scouting.py) were
committed locally at `4652d73` **before**
the first paid session. Independent expectations and the final audit freeze were
never accepted; there is no `frozen.json` authorizing audits.

| Case | Public licensed repository | Pinned commit | Supplied text files / bytes |
| --- | --- | --- | --- |
| r1 | [getsops/sops](https://github.com/getsops/sops) | `e39ca97b6209f9132ea40d22beb37d796060cb32` | 154 / 1,096,210 |
| r2 | [litestar-org/advanced-alchemy](https://github.com/litestar-org/advanced-alchemy) | `e051a5de1a008b70f2d67b416e236a8c59e69433` | 385 / 6,039,744 |
| r3 | [pyeventsourcing/eventsourcing](https://github.com/pyeventsourcing/eventsourcing) | `bf665955d9243e728aaaa5bb62ac63b9cfe5ec19` | 335 / 2,394,915 |
| r4 | [requests-cache/requests-cache](https://github.com/requests-cache/requests-cache) | `abe06a833cfb35a885f371d1b3db1199b3a968b5` | 150 / 1,535,586 |

The [manifest](../../cohorts/real-scouting-1/manifest.json) supplies per-file
hashes, binary exclusions, licenses and provenance. Archives retain unchanged
source and notices. Selection used each public default HEAD before behavior
inspection, domain diversity and size; it did not use known bugs. None repeats
pg-trickle or prior Gapline cases. Session novelty does not exclude training-data
familiarity. Public licensing supplies inspection permission, not maintainer
endorsement. Lockfiles/docs inflate totals; raw size alone cannot establish
scouting difficulty. Binary fixtures/assets were not inspectable.

A is production at `b4d1e1c86802f16fe996c68eb33940cc298ea82c`; B adds only PR #11's
Scout paragraph and optional scouting recipe. Both preserve #7's current
shortened Probe guidance. Tests verify the sole differences and unchanged
production bytes. No installable skill or reference was changed.

## Actual attempt and blockers

Only **curator 1**, responsible for r1/r2 pre-audit expectations, ran. It received
source only, no skill, report, arm identities or controller interpretations.
Retained: [exact input](curator-1-input.json), [events](curator-1-events.jsonl),
[adapter activity/results](curator-1-inspections.jsonl), [output](curator-1-report.md),
[run receipt](curator-1-run.json), [stderr](curator-1-stderr.txt), and
[host settings/inventory](curator-1-host.json).

| Measurement | Observed |
| --- | --- |
| Model / reasoning | `gpt-6.1-sol` / `low` |
| CLI | `0.163.0` |
| Actual host sandbox / approvals | `read-only` / `never` |
| Model session result | COMPLETED, exit 0 |
| Evaluator result | REJECTED; stop before further sessions |
| Wall time | 74.439 seconds of 180 |
| Inspection calls | 12 of 12 |
| Input tokens | 343,989 |
| Of which cached | 271,616 (already included in input) |
| Output tokens | 2,300 |
| Input + output | **346,289 > 250,000**, exceeding ceiling by 96,289 |
| Reported reasoning output | 32 tokens (not added to output) |
| Monetary charge | UNAVAILABLE |
| Source changes / forbidden observed calls | None |
| Timeout / authentication failure | None |

The 250,000-token instruction ceiling came from the existing pilot/refinement
infrastructure and was explicitly retained in the new frozen protocol. It is
checked after completion, not enforced by a host token cutoff. The launcher
stopped on `token_budget_met: false`. Caching does not excuse the overrun: input
counts cached tokens. Broad/batched responses and repeated context are visible
in the inspection record; this one attempt does not isolate their cost effects.

Post-stop examination of the exact-thread host trace confirmed the requested
model/effort/read-only/never settings and unchanged before/after source hashes.
Only inspection, clock, and host orchestration calls were observed. However,
the emitted inventory also exposed `apply_patch`, goal lifecycle APIs, and MCP
resource APIs. That fails this protocol's declared **available-tools** restriction.
No extra API was used, no write succeeded or was attempted, and this is **not**
evidence that the host's read-only sandbox was bypassed. Denial of those APIs
and restriction of resource access were not independently demonstrated here.
The adapter itself passed outside-path/execution/over-budget denial checks;
adapter safety alone does not qualify every host API.

All twelve adapter requests succeeded. Its source-cited contracts and proposed boundaries remain unaccepted
sampling notes. They are not audit findings, independent ground truth, test
coverage evidence, or a scouting-quality comparison. No runtime behavior was
reproduced. Do not promote these outputs into frozen expectations after the fact.

## Evidence and limitations

Positive process evidence: public snapshot retrieval and service authentication
worked; the adapter supplied bounded source reads; requested model/sandbox
settings were observed; supplied source stayed unchanged; the post-hoc budget
gate stopped further launches. The adapter's minimal line-range extension makes
later sections of large files inspectable and is exercised by a regression check.

Negative process evidence: one expectation session exceeded its total-token
ceiling despite meeting time/call limits, and the declared strict host tool
inventory was not achieved. The initial sandboxed development suite also failed
ten existing package tests that create sibling temporary directories; that
[failure is retained](prelaunch-sandbox-failure.txt). The subsequently authorized
controller run [passed all 50 prelaunch checks](prelaunch-tests.txt); the final
[regression run passed all 51 checks](development-checks-final.txt). Those development
checks executed authored Gapline fixtures, never the retrieved real projects.

Inconclusive effectiveness evidence: **no audit probe-selection differences,
confirmed misses, false positives, abstention comparisons, verification-effort
judgments, arm overhead, or reviewer agreement/disagreement exist**. There are
no eight audit reports to retain. [Run status](status.json) explicitly records
every unlaunched session rather than inventing placeholder reports. Curator
usage is preparation overhead, not A/B cost. Controller/total elapsed time,
controller tokens, monetary charge, human verification effort and full OS
telemetry are UNAVAILABLE. No population or production-effectiveness claim.

## Acceptance assessment and next step

| Issue #6 acceptance criterion | Assessment |
| --- | --- |
| Observed current-Scout shortcomings distinguished from hypotheses | Prior evidence retained in #6/PR #12; this attempt adds **no current-Scout observation**. |
| Guidance changes prioritization, not required lenses/findings | Sole-difference tests verify the proposed A/B text; no audit behavior observed. |
| Matched realistic trials include positive, negative, inconclusive results | **NOT SATISFIED**: zero matched audits, zero blind reviews. |
| No new required host/parser/runtime/language capability | Production unchanged; evaluator-only adapter line reads and cohort orchestration reuse existing infrastructure. |
| Change installed skill only if tradeoff justifies it | Satisfied as a restraint: production unchanged; no restoration justification. |

The smallest next step is **preflight qualification**, not an extra scouting
rule: qualify effective denial/scope of all native host APIs (or a way to remove
them), and predeclare a workable token policy for these larger sources while
keeping matched 180-second/12-inspection budgets. Any revised design must be
frozen before fresh authorized attempts. A revised token budget is not permission
to silently retry this failed session. This exposed curator material is no
longer unseen; disclose it in any follow-up and reassess independence.

The decision is **INCONCLUSIVE**, with current production retained procedurally.
The larger-real-repository acceptance gap remains, so #6 must stay **OPEN**.
#7 remains **CLOSED** and its shortened verification guidance is unchanged.

Publication is separately blocked: automatic approval review rejected the branch
push because the user's subsequent authorization covered local Git metadata
writes, while this incomplete evaluation produced no justified improvement
requiring a PR. No push/PR workaround was attempted. Evidence is locally
committed; a separate publication approval is needed for a source-evidence link
and CI. See [publication receipt](publication-blocker.json).
