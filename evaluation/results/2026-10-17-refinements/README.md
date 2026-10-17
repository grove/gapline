# Four-way scouting and verification comparison — 2026-10-17

Published in [PR #12](https://github.com/grove/gapline/pull/12).

**Decisions: REVERT the added scouting guidance; SIMPLIFY verification.**
Twenty bounded audits found no scouting advantage on five compact synthetic
cases. Blinded reviewers found modest gains from explicit refuting outcomes,
but many ties and several shorter adequate baseline handoffs. Retain only a
short setup/support/refutation aid, with unknown requirements clarified first.
The final shortened wording **was not rerun**. This is a bounded product
decision, not proof of production effectiveness or developer time savings.

**Issue disposition:** [#6](https://github.com/grove/gapline/issues/6) remains
open: these cases did not meaningfully constrain scouting choices. The bounded
comparison and simplification satisfy [#7](https://github.com/grove/gapline/issues/7),
whose independent-review criterion permits equal actionability at acceptable
cost. Closure does not certify human usefulness or the shortened wording's
behavioral equivalence.

## Provenance and frozen comparison

Initial working tree was clean on `main`, matching freshly fetched `origin/main`
at `e75d777512cbbbb727648ba1f1e6f3a381858071`. No unrelated work was changed.
The supplied pre-PR revision `a7e498f80ec6b042a6f0c88aa13c5a04682a938b` is PR #11's
actual base; the supplied post revision is its actual merge. The package diff
contains the two additions and matching optional reference paragraphs; licenses,
read-only constraints, evidence vocabulary and default limits are unchanged.
[Issue snapshots](issue-6-before.json), [#7 snapshot](issue-7-before.json), and
[PR #11 metadata](pr-11.json) retain the original criteria and caveats.

The [protocol](../../refinements-v1.md), [curator manifest](../../cohorts/refinements-1/manifest.json),
exact A/D package snapshots, oracle, runner and adapter were committed before
any audit at [`ac175cf`](https://github.com/grove/gapline/commit/ac175cf).
Reviewer preparation was committed before review at
[`82aeec7`](https://github.com/grove/gapline/commit/82aeec7), with a residual
call-count mask correction at [`af98017`](https://github.com/grove/gapline/commit/af98017).
No worker result changed a case, expectation, skill variant or audit schedule.

| Arm | Exact instruction configuration |
| --- | --- |
| A | Original installed package before PR #11 |
| B | A plus PR #11 scouting only, including its optional reference paragraph |
| C | A plus PR #11 verification only, including its optional reference paragraph |
| D | Both, byte-identical to the merged package |

Removing the two additions from D reconstructs A exactly. Historical `git show`
bytes were checked against the retained snapshots before launch. The runner
checks factorial separation and frozen cohort hashes. [Preflight](preflight.json)
retains exact variants, schedule, source identities and runner/server hashes.
Every audit's `*-input.json` retains exact argv/stdin and supplied identities;
`*-run.json` adds observed status, duration, usage and post-run identities.

The isolated curator had no parent history, parent repository access, audit
reports or judging role. It authored five new synthetic systems, rather than
reusing the prior pilot, public teaching cases or pg-trickle examples. Each has
149–191 Python lines across implementation and public tests. The controller's
prelaunch source review caught an overflow flaw in the intended clean control;
the curator bounded its numeric domain and added coverage **before freezing**.
This correction is recorded in [provenance](../../cohorts/refinements-1/README.md).
All 31 public tests and the separate oracle passed before any audit; see
[prelaunch receipts](prelaunch-checks.txt). These are evaluator executions,
never worker reproductions. Synthetic authorship does not prove training novelty.

## Controlled runs and inspection choices

Exactly **20 audit attempts and two reviewer attempts**, all completed, no
retries or replacement sessions. Audits ran sequentially in the frozen order:
s1 A/B/D/C; s2 B/C/A/D; s3 C/D/B/A; s4 D/A/C/B; s5 D/C/A/B. Positions and
predecessors balance over the first four cases; the fifth adds a small imbalance.

All used locally authenticated Codex CLI 0.163.0, `gpt-6.1-sol`, reasoning `low`,
sandbox `read-only`, approval `never`, fresh persisted sessions, no delegation,
identical questions and inspection interface. Own-session turn-context settings
matched all 22 requested configurations; see [measurements](measurements.json).
Every run stayed below 180 seconds, 12 inspections and 250,000 input-plus-output
tokens. Wall time was enforced by process-group termination; adapter operations
after twelve are denied. The token ceiling was instructional and checked after
completion. No timeout or budget-denial path was needed in model sessions.

The evaluator-only [adapter](../../inspect_server.py) exposes immutable supplied
file bytes via list/read/literal-search, with exact allowlisted paths, no
symlinks and no execution, network or mutation operation. Unit checks exercise
outside-path rejection, execution-operation rejection, snapshot stability,
budget denial and MCP transport. Shell execution, browser/computer tools,
apps/plugins/hooks, web, memories and delegation were disabled; see exact argv
and the [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
Skill content was loaded manually through the adapter. Installer discovery
was not part of this comparison.

**Host caveat:** `skip_host_skill_discovery` emitted an under-development warning
and did not remove a common skill catalog. [Own-context checks](host-context-checks.json)
show identical base instructions and identical developer instructions after
project-path normalization across all 20 audits. Neither added paragraph occurs
in those host instructions. This is a common catalog context, not a catalog-free
host. It does not provide evaluator answers or access to other source trees.

Actual event types were agent messages, inspection MCP calls, and the shared
nonfatal feature warning. The only called MCP server was `inspection`; there
were no adapter errors, other tools, commands, project execution/imports/tests,
builds, installs, edits, network-tool calls or delegation. Every supplied tree
matched the exact frozen source/arm before and after. Full OS telemetry remains
unavailable; this does not qualify arbitrary shell access or exclude CLI
infrastructure effects outside model tools.

**Scouting observation:** all twenty audits read the complete public source and
test inventory. Nineteen batched that in one read after skill/listing; s5 B split
it across two reads. None read optional reference recipes. Source selection
therefore provides no evidence of improved prioritization, avoided superficial
probes or missed major boundaries. The budget was too generous relative to case
size to stress that question. Do not infer broad scouting effectiveness from
correct final findings.

## Blinded independent judgments

Two fresh Codex sessions, neither case authors nor audit workers, reviewed all
reports: reviewer 1 s1/s2/s3; reviewer 2 s4/s5. Both input sets were frozen before
either review. Seed 67 shuffled labels/order; absolute trial paths, method names
and telemetry were masked. Source, nonbinding frozen expectations, source-only
inspection choices and public investigation notes were included; skill contents,
arm mapping, elapsed/token costs and controller opinion were withheld. Exact
[inputs](review-inputs.json), masked `review-*-s*.md` bundles, [mapping](review-mapping.json),
[reviewer 1 judgments](review-1-report.md) and [reviewer 2 judgments](review-2-report.md)
are retained. Their `*-frozen.sha256` receipts predate unmasking/product decisions.

This is **independent process-role model review, not independent human validation**.
Each case had one reviewer, not two; the same model family was used throughout.
Generic method/procedural disclosures and report structure remained, so blinding
was imperfect. Both reviewers reported no arm inference. Do not call this a
human application study or measured reduction in developer effort.

| Case | Across A/B/C/D | Material contrasts after unmasking |
| --- | --- | --- |
| s1: rubric publication/result stability | All identify shared mutable criteria crossing publication and changing old results. No material false positive. | A and C additionally note old-result retrieval can raise. C explicitly names a refuting outcome. D and B are already adequate; reviewer calls D the cheapest adequate handoff. |
| s2: uninterrupted licensed playback | All return no findings and reject finish-time reauthorization contrary to the explicit policy. | A is the cheapest adequate handoff. B/C/D mention a qualified repeat-input ambiguity without accusing the correct policy. |
| s3: sensor ledger | All return no consequential findings; all inspect atomicity, UTC identity, replacement and summary boundaries. | C is shortest adequate. A proposes a modest optional fractional-mean test, with a less concrete oracle than ideal. B has a minor atomicity-test citation error. All miss the documentation wording noted below. |
| s4: advance-prepared worksheets | All identify retained snapshots and preserve the unresolved meaning of “next shift.” None proves a runtime violation. | B is cheapest adequate. C adds explicit refutation and rejected leads, but its opening is slightly too strong; D also overstates the opening. A states the contract-scope uncertainty particularly clearly. |
| s5: spacing units | All identify both README contradictions and recommend a direct pixels correction, without runtime reproduction or conversion work. | D is cheapest adequate. A locally reverses expected/actual authority presentation but resolves it in the body. C adds a valid compatibility reminder. |

**Contrary evidence and disagreements:** no consequential factual false positive
was established. Verification guidance did not consistently improve uncertainty
calibration: s4 C/D's opening labels are stronger than their qualified bodies.
Refutation detail is a modest gain, not evidence that the baseline next action
was unusable. Most cases are ties on useful outcomes. No instruction prevented
all citation/presentation defects.

Reviewer 1 independently noticed a shared minor miss in intended-clean s3:
README includes count among statistics then says each statistic is `None` when
empty, while code/tests use count 0 and other values `None`. A short documentation
clarification is warranted; no consequential runtime defect follows. This
disagrees with an overly broad claim of complete contract consistency, while
preserving the frozen no-required-consequential-finding interpretation. The
frozen case was **not repaired after seeing reports** or silently removed.

## Costs and limits

Full per-run durations, inspection counts, input/cache/output tokens and report
links are in [the measurement table](measurements.md). [Recompute them](summarize.py)
from raw `*-run.json`, `*-events.jsonl` and `*-inspections.jsonl`. Input includes
the cached subset; output includes reported reasoning tokens. These are model
usage receipts, not prices or unique source-token counts.

| Arm, five audits | Seconds | Inspections | Input tokens | Cached subset | Output tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 151.405 | 15 | 356,820 | 286,336 | 4,047 |
| B | 142.302 | 16 | 375,185 | 306,048 | 3,708 |
| C | 154.156 | 15 | 313,651 | 247,552 | 3,868 |
| D | 152.116 | 15 | 361,670 | 270,464 | 3,855 |

Scouting contrasts B−A / D−C: **−9.103 / −2.040 seconds**, **+18,365 / +48,019
input tokens**, and **−339 / −13 output tokens**. Verification contrasts C−A /
D−B: **+2.751 / +9.814 seconds**, **−43,169 / −13,515 input tokens**, and
**−179 / +147 output tokens**. D−A: **+0.711 seconds (+0.47%)**, **+4,850 input
tokens (+1.36%)**, **−192 output tokens**. These single observations are noisy:
model tool batching, prefix caching and server load differ; sampling settings
and a model sampling seed were unavailable. Negative token/time differences do
not prove an instruction saves cost. No substantial combined latency increase
was observed, but no population estimate is justified.

All audits consumed **599.979 seconds / 1,407,326 input / 15,478 output tokens**.
Reviewers added **125.493 seconds / 206,945 input / 3,658 output / 7 inspections**.
Total CLI-session elapsed sum was **725.472 seconds**. Curator/controller work,
review preparation and development validation are additional and excluded.
Monetary cost, controller/curator tokens, active reasoning time, full OS
process/filesystem/network telemetry and applied human effort are **UNAVAILABLE**.
No further paid sessions were launched after the declared 22 attempts.

## Product decisions and acceptance

**#6 — REVERT, issue remains OPEN.** The original Scout already prioritizes
promises, boundaries and consequences. Prior pilot evidence showed no wholly
empty reports, uncertain NaN/scaling leads, and potentially useful test-gap
advice, but did not establish wasted scouting or spontaneous pg-trickle
discovery. Here the added prioritization rule changes no useful investigation
outcome or source selection. Remove it and its optional reference paragraph;
preserve the original Scout, narrow/survey modes, three-lead limit, stop budget,
no-findings option and bounded optional delegation. No new runtime/parser or
sibling dependency is installed. The acceptance gap is meaningful selection
under a scarce budget on a larger realistic question, not another presence test.

Smallest remaining experiment, **PROPOSED — NOT RUN**: freeze two fresh larger
maintainer-specified snapshots (one consequential cross-component risk and one
valid distracting design) whose full source cannot be read in twelve calls.
Compare original versus a short scouting aid in four matched single-agent runs,
with neutral prompts, a frozen oracle and blind source-choice/outcome review.
Do not run this now or reuse these public cases as unseen evidence.

**#7 — SIMPLIFY, bounded acceptance satisfied.** Contrasting cases cover an
actionable unresolved mechanism, legitimate alternative, unknown requirement
and direct documentation contradiction. All executable handoffs are explicitly
**PROPOSED — NOT RUN**; all docs-only handoffs permit direct correction. Reviewer
comparisons establish equal material actionability with occasional useful
explicit falsification, low observed combined overhead and no material invented
runtime proof. They do not establish developer time savings. Long recipes and
domain-specific reproduction advice add no demonstrated value here; remove
them. Keep only the setup/observable support/meaningful refutation aid, with
unknown requirements clarified before choosing an expected result. Existing
documentation-contradiction and read-only rules remain sufficient.

The final aid is 37 words in the existing Probe step, with no new report schema,
sections, categories, workflow, dependency or permission. This is a controller
simplification informed by the comparison; **the shortened text has not had an
additional model evaluation**, and no equivalence/effectiveness claim is made
for that exact text. Packaging/presence tests cannot supply that missing evidence.

## Reproduction and final validation

With an explicitly authorized new model budget and existing Codex authentication:

```sh
python3 -B evaluation/cohorts/refinements-1/oracle.py
python3 -B evaluation/run_refinements.py --output /path/to/new/evidence --work /path/to/new/workers
python3 -B evaluation/review_refinements.py --output /path/to/new/evidence --work /path/to/new/reviewers
```

The latter commands invoke twenty plus two real model sessions. They reject
existing working destinations; do not invoke them merely to recompute costs.
Reruns of these now-public cases are calibration, not fresh evaluation. Use the
retained exact argv/stdin for the original host configuration. No reproduction
promises deterministic reports or model availability.

[Predecision full checks](development-checks-before-decision.txt) and
[final regressions](development-checks-final.txt) each passed 46 tests in a
disposable checkout copy. The [real local installation check](install-local.txt)
passed Codex and Claude Code copy/symlink payload and link checks using skills
CLI 1.7.2 and Node 26.12.0. [Candidate CI](ci-candidate.json) passed regression
and Node 22.20.0/24 install jobs for both push and PR events at `ceb2219`; the
subsequent receipt commit changes only evaluation documentation/receipts. Installation
checks are development operations, not audit actions or Claude host qualification.
Prior pilot results were never modified. [Artifact hashes](artifacts.json)
cover the retained record except that hash file itself. Raw CLI and adapter
streams are retained; own-session exports omit instruction bodies, private
reasoning, account metadata and auth. Original report links refer to paths in
their supplied project; consult the matching frozen case tree or numbered
review bundle when reading them from this evidence directory.
