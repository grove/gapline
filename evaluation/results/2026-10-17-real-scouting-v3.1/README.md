# Controlled scouting comparison — stopped at the fourth audit

**Decision: INCONCLUSIVE. Keep issue #6 OPEN; keep #7 CLOSED.** The capability
gate accepted the qualified host configuration, both fresh expectation curators
completed, and three audits completed. The fourth audit, r2-A, hit the unchanged
180-second hard timeout. The controller stopped immediately: the remaining
four audits and both masked reviews are **NOT RUN**. No further session retry
or replacement was authorized or launched. Production remains unchanged.

This is an incomplete experiment, **not a credible negative scouting result**.
It supplies no independent reviewer conclusions, demonstrated scouting advantage,
or justification to restore PR #11's additional guidance. Retaining current
production pending evidence is not a KEEP CURRENT effectiveness verdict.

## Freeze, authorization and provenance

The [adopted v3 protocol](../../real-scouting-v3.md) accepts capabilities under the
existing [tested host boundary](../2026-10-17-host-capabilities/README.md), rather
than demanding that qualified native APIs be invisible. Its
[focused tests](../../../tests/test_real_scouting.py) reject forbidden activity,
unknown capabilities, altered contexts/server configuration and failed curators.
The launcher and inspection adapter were not changed after qualification. This
work did not restart host probes or broaden the isolation claim.

Commit `de45aee` froze v3 before its first curator. That curator refused before
source inspection because the prompt did not explicitly name qualified
`apply_patch`; the [entire failed attempt](../2026-10-17-real-scouting-v3/README.md)
is retained and rejected. Commit `0b357bd` prepared the prospective
[exact-name clarification](../../real-scouting-v3.1.md). The user then explicitly
approved **one replacement curator and continuation**, including the disclosed
aggregate ceilings: 13 attempts / 12,024,298 tokens / 2,173.970 session seconds,
including the retained failure. No further retries or merge authority followed.

Commit `1e05673` froze the [exact twelve prompts, source/host identities,
schedule, protocol and authorization](setup.json), plus
[58 passing prelaunch checks](prelaunch-tests.txt), before the replacement.
Commit `81fdb68` froze both newly accepted curators' reports and
[expectation/instruction identities](frozen.json) **before any A/B audit**.
Neither old v1 interpretations nor the rejected v3 curator were accepted as
fresh evidence. Curators had source only; audit workers had source and one
variant, never expectations, previous answers or controller interpretations.

The [unchanged cohort manifest](../../cohorts/real-scouting-1/manifest.json)
contains exact archive and per-file identities, original upstream licenses,
and binary exclusions. Supplied files are unmodified tracked UTF-8 text:

| Case | Public source | Exact commit | Files / bytes | License |
| --- | --- | --- | ---: | --- |
| r1 | getsops/sops | `e39ca97b6209f9132ea40d22beb37d796060cb32` | 154 / 1,096,210 | MPL-2.0 |
| r2 | litestar-org/advanced-alchemy | `e051a5de1a008b70f2d67b416e236a8c59e69433` | 385 / 6,039,744 | MIT |
| r3 | pyeventsourcing/eventsourcing | `bf665955d9243e728aaaa5bb62ac63b9cfe5ec19` | 335 / 2,394,915 | BSD-3-Clause |
| r4 | requests-cache/requests-cache | `abe06a833cfb35a885f371d1b3db1199b3a968b5` | 150 / 1,535,586 | BSD-2-Clause |

These cases had no previous A/B audits, but r1/r2 had exposed v1 preparation
notes. Fresh process isolation prevents those notes entering new workers;
it cannot establish absence from model training or public familiarity.

A is production at `b4d1e1c86802f16fe996c68eb33940cc298ea82c`. B differs only
by PR #11's extra Scout paragraph and optional scouting recipe. Both preserve
#7's identical shortened verification guidance. Scheduled order was r1 A/B,
r2 B/A, r3 B/A, r4 A/B. The broad question, settings and access were identical
within each pair. All sessions used pinned Codex CLI 0.163.0, `gpt-6.1-sol`,
low reasoning, read-only sandbox, never approvals, strict orchestration flags
and the sole restricted inspection server, with 1M-token / 180-second /
12-inspection ceilings. Binary, OS, interpreter, invocation and launcher/adapter
identities are retained in setup and each run's actual host receipt.

## Actual activity, failure and status

[Per-session measurements](measurements.md), [machine-readable status and
costs](measurements.json), original `*-input.json`, `*-run.json`, `*-events.jsonl`,
`*-host-events.jsonl`, `*-host.json`, `*-inspections.jsonl` and stderr retain every
attempt, actual call/result and supplied file identity. No output is fabricated
for a missing report. There are five completed reports: two curators and three
audits. There is no completed r2-A report and no reviewer input or report.

The failed [r2-A receipt](r2-A-run.json) records `TIMEOUT`, exit -9, **180.018
seconds**, four inspection attempts and unavailable final usage. The final
0.018 seconds are process termination/measurement overhead, not extra authorized
model time. Two malformed skill-read requests failed; a corrected skill read
and a repository listing succeeded. No repository source-content inspection
completed. The model did not return a final report before termination. The
underlying delay is unknown; it is not evidence that A's scouting is slower.

The [partial same-thread usage counters](r2-A-partial-usage.json) last show
62,277 input (48,512 cached) and 199 output = **62,476 tokens**. They are not a
final bill or proof that the final cumulative token ceiling was met. The raw
run's `UNAVAILABLE` usage and budget status remain unchanged. No timeout retry
was made and no remaining model session launched.

All six attempted v3.1 sessions passed host configuration/activity checks:
qualified visible tool names only; actual calls used orchestration and the
inspection adapter; no native patch/generic resource use, dynamic dispatch,
additional server, shell/network execution, permission change or source mutation
was observed. Host and adapter call counts agree. Each stayed at or below twelve
actual inspection attempts, including errors. Full OS process/filesystem/network
telemetry is unavailable; the retained host/adapter events and hashes are the
evidence, not worker self-attestation or proof of general sandbox isolation.

Sixteen of 62 inspection attempts failed on malformed arguments. Such calls
consumed the controller's inspection allowance. The adapter's internal counter
increments after Python argument binding; rejected argument-shape requests may
not increment it. The controller counts **every logged request** and rejects
over-twelve sessions after execution. No accepted session exceeded twelve. This
is a known limit of the qualified adapter, not a claim of a universal hard cap
on malformed requests. No adapter or permission configuration changed mid-run.

## Scouting evidence and independent assessment

The completed [r1-A report](r1-A-report.md) and [r1-B report](r1-B-report.md)
both selected temporary-secret command execution, alleging background cleanup
and unchecked plaintext-delivery errors. Their overlap is observable, but
**agreement is not verification or evidence of equal effectiveness**. Both
preserved runtime uncertainty and proposed unrun checks. The unmatched
[r2-B report](r2-B-report.md) alleges lost file-storage recovery state in the
async listener. It has no completed A counterpart. None of these claims was
independently judged or tested in this stopped experiment; the reports' own
SUPPORTED labels are not evaluator endorsements.

The [fresh curator expectations](expectations/) supply challengeable contracts,
cross-component candidates, valid unusual designs, accepted alternatives and
abstention conditions. They are nonexhaustive interpretations, not ground truth
or a denominator for computing recall. Audit reports chose paths beyond those
candidates; novelty relative to curators is not proof of consequence or correctness.

Both origin-masked reviewer sessions remain NOT RUN. Consequential selection,
missed risks, meaningful incremental weaknesses, false accusations, proper
abstention and practical verification effort therefore remain **UNASSESSED**.
There is no measured human verification effort. No finding-count, verbosity,
wording sophistication or report-agreement score substitutes for those reviews.

## Overhead and limitations

| Observed group | Session seconds | Inspections | Known final tokens |
| --- | ---: | ---: | ---: |
| Two accepted curators | 164.672 | 22 | 831,780 |
| Three completed audits | 167.592 | 36 | 1,032,151 |
| Timed-out r2-A | 180.018 | 4 | UNAVAILABLE |
| v3 prompt refusal, retained separately | 13.970 | 0 | 24,298 |
| Masked reviews / remaining audits | NOT RUN | NOT RUN | NOT RUN |

The sole completed pair has A **58.717 seconds / 275,230 tokens**, B **55.242
seconds / 360,834 tokens**: B used 85,604 more tokens (+31.1%) and 3.475 fewer
seconds (-5.9%) in these observations. Both used twelve attempts, with three
argument errors each. This is one noisy pair without independent quality
judgments, not a causal cost estimate or a restoration/retention justification.
Do not compare the two-arm aggregates when A includes a timeout and B does not.

Current v3.1 session elapsed sum is **512.282 seconds**, with **1,863,931 known
final tokens**, excluding the timed-out session. Including the retained v3
refusal gives **seven attempts / 526.252 seconds / 1,888,229 known final tokens**,
plus the timed-out session's unavailable final usage (62,476 partial observed).
Cached input is already in input; reasoning output is already in output.
Monetary charges, controller usage and active reasoning time are UNAVAILABLE.

Earlier v1, v2 and host-qualification work remains separate preparation overhead
in measurements.json: 74.439 / 11.625 / 33.726 seconds and 346,289 / 23,380 /
80,117 tokens, respectively. No old failure is hidden or treated as new audit
evidence. The diagnostic's twelve data-interface calls include native probes;
its four adapter calls are not directly comparable to audit inspection counts.

Other limits: four purposively selected public repositories; no model sampling
seed/repetitions or variance estimate; bounded text-only sampling; no runtime
tests; same model family for all roles; independent process roles rather than
human maintainers; no blinded judgments completed; no whole clean-repository
control established. Frozen expectations did include legitimate designs and
abstention candidates, but their handling was not independently assessed.

## Issue acceptance and next boundary

| #6 criterion | Evidence / disposition |
| --- | --- |
| Specific current-scout shortcomings, observations vs hypotheses | No independently established semantic shortcoming. Malformed tool calls are observed in both arms; attribution to Scout is unsupported. |
| Guidance changes prioritization, not required lenses/findings | Byte comparison/test verifies only the optional historical Scout additions; production unchanged. |
| Matched realistic trials, contrary and inconclusive results | One completed pair, one unmatched B, one timeout; all retained. Four pairs and masked judgments are incomplete. **Not satisfied.** |
| No required runtime/parser/tool/capability | Existing restricted launcher/adapter reused; no production dependency or capability added. |
| Update production only if justified | No production change justified or made. #7's shortened guidance remains identical. |

**#6 remains OPEN.** The exact gap is the incomplete matched cohort and absent
independent quality assessments, not unqualified native API visibility. Do not
restore scouting or call this a successful negative experiment. Any continuation
needs an explicitly approved prospective exception for the timed-out attempt
and an updated freeze, preserving every existing report, failed cost and fresh
worker isolation. The previous one-replacement approval does not cover it.
No additional paid session is proposed as already authorized. Merging the
infrastructure/evidence PR is a separate effect requiring approval.

## Non-billable reproduction and validation

Run `python3 -B evaluation/results/2026-10-17-real-scouting-v3.1/summarize.py`
to recheck frozen inputs, host activity/configuration, unchanged identities,
completed-run budgets, timeout status and reported measurements. This makes no
model calls. Original reports cannot be deterministically reproduced. The
runner's paid phases reject existing attempts; do not run them as a replay.

The prelaunch suite passed 58 tests. Final checks, controller PR review, artifact
hashes and exact-candidate CI receipts are saved alongside this record. No
host qualification probe or project code/test/build was executed by audit workers.

Published in [PR #13](https://github.com/grove/gapline/pull/13) at candidate
`251dc51b5d0bafae7c23b303c242d3a9019ce077`. All six candidate checks passed:
[PR CI](https://github.com/grove/gapline/actions/runs/39037331295) and
[push CI](https://github.com/grove/gapline/actions/runs/39037328559), each with
regression checks and Node 22.20.0/24 installation jobs. Exact receipts are
[retained](ci-candidate-pr.json), including [push jobs](ci-candidate-push.json).
The following receipt-only commit does not alter the tested runner or skill.
The [#6 evidence update](https://github.com/grove/gapline/issues/6#issuecomment-6234554445)
leaves it open; [#7 remains closed](issue-7-after.json). The
[candidate PR state](pr-candidate.json) is open and mergeable, not merged.
No merge or further paid attempt was performed.
