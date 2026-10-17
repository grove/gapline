# Fresh authored cohort: incremental-value pilot — 2026-10-17

**Decision: KEEP the portable skill for another focused trial, with a
single-agent default.** Gapline added two specific regression-check scenarios
that ordinary review omitted. It found **no additional current functional
defect**. The added observations cost more elapsed time and model input in the
single-agent arm. These three small authored cases do not establish superiority
on production repositories or justify expanding the product.

## Frozen inputs and independence

This implements the small comparison requested in [issue #5](https://github.com/grove/gapline/issues/5),
using [protocol v1](../../pilot-v1.md). Contracts, expected outcomes, accepted
alternatives, exact source hashes, evaluator oracle, launcher and its checks
were committed **before any audit launch** at
[`e750a6d39f27df58393a0bf14d0bd3bb36b079d2`](https://github.com/grove/gapline/commit/e750a6d39f27df58393a0bf14d0bd3bb36b079d2).
The [manifest](../../cohorts/pilot-1/manifest.json) is evaluator material;
workers received only one neutral source directory's three public files.
[Preflight](preflight.json) and [run receipts](runs.json) retain protocol,
launcher, cohort and skill identities, exact prompts/argv, and pre/post hashes.
The measured skill payload was unchanged throughout.

A fresh curator context authored the cases without auditing them or seeing
reports. It read old teaching expectations to avoid reproducing them. These
are **new synthetic snapshots**, not sampled real repositories, renamed public
teaching fixtures, proven pretraining-novel cases, or unseen production defects.
The previously exposed pg-trickle scopes/tickets were not included.

A separate reviewer context first checked the contracts and oracle, then judged
all nine reports without the arm mapping, host costs or controller opinion.
[Source assessment](independent-source-review.md),
[frozen report judgments](independent-report-judgments.md),
[exact assignments](reviewer-prompts.md),
[masked inputs](review-inputs.json) and [subsequent mapping](review-mapping.json)
are retained. Reports were shuffled with seed 50; only absolute source roots
were normalized. **This was label masking, not full blinding:** method names
and report structure remained visible. The reviewer reported not inferring or
using arm identities. This is independent process-role model review, not human
or cross-model replication. The controller did not revise its judgments.

## Independently reviewed outcomes

The manifest is nonexhaustive. A case with no planted functional defect can
still contain a useful test gap. Finding counts are deliberately not compared:
C grouped two q3 scenarios that B reported separately.

| Case | A: ordinary review | B: Gapline alone | C: selective Gapline |
| --- | --- | --- | --- |
| q1: artifact recovery | Correct first-publication defect and missing empty-store boundary test (r02). | Same material outcome (r05). | Same material outcome; delegation skipped (r07). |
| q2: batch leases | Correct NaN mechanism, but contract/reachability unresolved; opening certainty slightly too strong (r04). | Useful missing deadline-completion check before reassignment; current implementation correctly guards it (r08). | Same test gap; delegation skipped (r06). |
| q3: offline feed | Useful frozen-pull test gap; valid repeated-scan complexity observation with unmeasured practical importance (r09). | Frozen-pull gap plus missing compaction-during-continuation check; no current behavior defect (r01). | Same two scenarios grouped; delegation skipped (r03). |

**Incremental benefit:** B supplied the ordinary-duration q2 expiry check and
the q3 active-continuation expiry check absent from A. The reviewer found both
source-supported, contract-specific and inexpensive to verify. Existing public
tests miss those scenarios; the withheld evaluator oracle independently
exercises them successfully. This is additional **regression protection
advice**, not evidence of two more implementation defects or observed developer
time savings. B/C omitted A's conditional NaN and scaling observations; those
are useful unresolved leads, not independently confirmed missed production bugs.

**Dismissals, false alarms and abstention:** all arms avoided accusing intentional
completed-key retention, excluded persistence/concurrency, or valid frozen
pagination behavior. No factual false positive was established. q2 A's
unqualified opening needs its body qualification: finite-duration ownership is
unspecified and no adapter was supplied. q3 A's complexity analysis is valid,
but real slowness remains unmeasured. Medium impact labels for test gaps are
prioritization judgments, not witnessed harm. No report returned zero findings;
q2 B/C and all q3 reports explicitly withheld implementation-failure claims.
Thus this cohort covers uncertainty and functional abstention, but does **not**
observe a completely empty report or an unequivocal false-alarm outcome.

All q1 reports identify the same consequential defect: a failed first pointer
replacement leaves complete bytes that reopening promotes despite no commit.
They correctly preserve the existing-commit counterexample. The independent
reviewer's authorized evaluator oracle observed that exact behavior; workers
only reasoned from source and labelled execution proposals **NOT RUN**.
The oracle's one declared expected failure has a separate passing exact witness;
an arbitrary exception is not enough to satisfy it. All eight public tests pass.
Their separate evaluator receipts are in [public checks](public-checks.txt).

## All attempts and observable costs

Nine scheduled attempts, nine completions, no retries, failures or timeouts.
Each ran in a fresh persisted Codex CLI 0.163.0 session on macOS 26.6.2
(25G83), arm64. Requested and
exported settings matched: `gpt-6.1-sol`, reasoning `low`, sandbox `read-only`,
approval `never`. User config/rules, hooks/apps/plugins/web search and shell
snapshots were disabled as recorded in each argv. All arms used the same
question and 180-second, 12-inspection, 250,000-input-plus-output-token aggregate
ceilings. Wall time was enforced; tool/token limits were prompt instructions.
Every observed run remained within all three ceilings.
Sampling parameters and a model sampling seed were UNAVAILABLE; no overrides
were supplied. Replaying exact inputs/settings does not promise identical text.

Order, drawn before outputs using seed 5: q1 A→B→C; q2 A→B→C; q3 B→A→C.
The random draw left C last every time; **order was not counterbalanced**.
Arms ran sequentially, but caches, server load and other host activity were
uncontrolled. The reviewer's source phase overlapped the final audit runs.

| Run | Elapsed s | Inspection calls | Input tokens | Cached subset | Output tokens | Report / host events / own trace |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| q1 A | 24.303 | 2 | 42,716 | 36,352 | 793 | [Report](q1-A-report.md) · [events](q1-A-events.jsonl) · [trace](q1-A-trace.jsonl) |
| q1 B | 39.410 | 3 | 63,899 | 54,784 | 832 | [Report](q1-B-report.md) · [events](q1-B-events.jsonl) · [trace](q1-B-trace.jsonl) |
| q1 C | 47.749 | 3 | 64,117 | 38,912 | 964 | [Report](q1-C-report.md) · [events](q1-C-events.jsonl) · [trace](q1-C-trace.jsonl) |
| q2 A | 32.230 | 2 | 42,802 | 36,224 | 740 | [Report](q2-A-report.md) · [events](q2-A-events.jsonl) · [trace](q2-A-trace.jsonl) |
| q2 B | 28.627 | 3 | 64,187 | 48,512 | 827 | [Report](q2-B-report.md) · [events](q2-B-events.jsonl) · [trace](q2-B-trace.jsonl) |
| q2 C | 29.887 | 2 | 48,010 | 39,040 | 744 | [Report](q2-C-report.md) · [events](q2-C-events.jsonl) · [trace](q2-C-trace.jsonl) |
| q3 A | 26.332 | 3 | 58,628 | 51,712 | 824 | [Report](q3-A-report.md) · [events](q3-A-events.jsonl) · [trace](q3-A-trace.jsonl) |
| q3 B | 40.955 | 4 | 82,999 | 72,832 | 981 | [Report](q3-B-report.md) · [events](q3-B-events.jsonl) · [trace](q3-B-trace.jsonl) |
| q3 C | 34.365 | 2 | 47,996 | 39,040 | 878 | [Report](q3-C-report.md) · [events](q3-C-events.jsonl) · [trace](q3-C-trace.jsonl) |

Input includes the cached subset; do not add them. Output includes any reported
reasoning subset. Counts include repeated context across model calls, not just
unique source bytes. Inspections count host-observed shell invocations, including
skill reads; one invocation can batch several trusted file reads.
[Observations](observations.json) retain commands, exported settings and usage.

Across three cases, A consumed **82.865 s / 144,146 input / 2,357 output / 7
inspections**; B **108.992 s / 211,085 input / 2,640 output / 10 inspections**;
C **112.001 s / 160,123 input / 2,586 output / 7 inspections**. B added
26.127 seconds, 66,939 input tokens and 283 output tokens relative to A in this
single cohort. These are descriptive totals, not causal latency estimates or
prices. Cache utilization differed materially.

**Delegation:** all three C reports judged workers uneconomical; own host traces
contain no spawn calls. Zero workers means coordinator usage covers all model
usage observed for these runs. C added no material finding over B. Its totals
measure enabling selective delegation and choosing to skip, **not** actual
delegated work. Actual delegation's incremental benefit/cost is **NOT MEASURED**;
the earlier [host smoke](../2026-10-17-codex-host/README.md) establishes available
native mechanics, not an effectiveness comparison. The raw launcher receipts'
provisional child-usage UNAVAILABLE field is resolved here by the zero-spawn
trace review; no child costs were silently omitted.

**UNAVAILABLE:** monetary cost; full OS process/filesystem/network telemetry;
permission-decision stream; independent human review/application effort;
reviewer model/token usage and active review time. The reviewer recorded seven
inspection calls, one evaluator-oracle execution and two artifact writes across
its phases. [Timing notes](review-timing.json) include waiting and must not be
treated as active reviewer latency. Curator/controller resource costs were not
instrumented; per-arm totals exclude evaluation administration.

## Activity, integrity and reproduction

Observed audit commands only listed/searched/read supplied project files and,
for B/C, the exact project skill. No project execution, imports, test collection,
builds, writes, installation, network tools, credential reads, evaluator reads
or native worker calls appear in these trial streams. A was instructed not to
use audit skills and no skill read was observed; the global host skill catalog
still existed, so this is a no-invocation control, not a host without awareness
of available skills. B/C loaded the project SKILL; none read its optional recipes.
Global host instructions were inherited even with ignored user config. Unlike
the earlier host smoke, no extra RTK file read appears in these nine runs.

All original public files and installed skill files matched afterward; no
additional files were observed in worker trees. Identities omit Python cache
files. This does not prove containment
or exclude transient/elsewhere effects. Read-only mode does not itself enforce
project-only reads or forbid arbitrary process execution. We ran no host-boundary
challenge. All candidate bytes are public authored data; no secrets were baited.

To replay from this PR's checkout with an authorized, authenticated Codex host:

```sh
python -B evaluation/cohorts/pilot-1/oracle_test.py -v
python -B evaluation/run_pilot.py --output /path/to/new/evidence --work /path/to/new/workers
```

The second command invokes real, potentially billable model sessions. Use new
disposable paths; the launcher rejects existing destinations and mismatched
manifest bytes. It copies the exact local skill rather than retesting installer
discovery. Reruns of these now-public cases are **previously seen calibration**.
For another effectiveness cohort, first author/freeze fresh inputs and update
the fixed schedule/protocol deliberately; do not relabel these inputs as fresh.
Reconstruct reviewer inputs from `review-inputs.json`, withholding the mapping
until the judgments are frozen.

CLI JSONL and empty stderr files are retained unchanged. Readable report files
only strip trailing whitespace; CLI events retain original text. Own-session
trace exports use exact CLI thread IDs and record raw rollout hashes. They omit
global instructions, inherited history, private reasoning, account metadata and
rate limits, retaining selected settings, tool calls/results, public messages
and usage. No unrelated session contents were inspected. Retained artifact
hashes are in [artifacts.json](artifacts.json).

[Development validation](development-checks.txt): **40 tests passed** in a full
disposable checkout copy, including manifest/oracle and launcher preparation
checks. Existing tests create sibling directories, which the original workspace
sandbox disallowed. These were evaluator/development actions, separate from
read-only audit activity. The withheld oracle ran seven checks: six passes
(including the exact failure witness) and one declared expected failure.

## Decision and concrete next experiment

**KEEP**, narrowly: retain the existing optional portable skill and single-agent
default for another trial. The two independently supported, cheap-to-check
regression scenarios justify that limited continuation despite observed added
cost. No skill-body change, ledger, platform, benchmark service or mandatory
delegation is warranted by this evidence. Applied developer value and general
functional improvement remain unproven.

Next, obtain **three permissioned maintainer-specified larger snapshots**: a
consequential defect, an already-covered legitimate design, and a workload or
caller-contract ambiguity with explicit input/performance requirements. Freeze
answers before workers and counterbalance A/B/C order. Include a case large
enough for economical independent scouting/disproof without forcing a spawn.
Have a separate developer apply the proposed checks under separately authorized
execution controls and record added protection, false alarms, important misses,
verification effort and aggregate worker costs. Predeclare how test-only and
conditional findings count, and genuinely redact method disclosures before
review. **PROPOSED — NOT RUN:** no outreach, production audits, fix application
or further model runs were performed as that next experiment.
