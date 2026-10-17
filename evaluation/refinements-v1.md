# Scouting and verification experiment v1

Frozen before paid sessions for issues [#6](https://github.com/grove/gapline/issues/6)
and [#7](https://github.com/grove/gapline/issues/7). This is a small product
decision experiment, not a production benchmark.

## Comparison and budget

Verify historical identities: A is the installed package at
`a7e498f80ec6b042a6f0c88aa13c5a04682a938b`; D is the package at PR #11's merge,
`e75d777512cbbbb727648ba1f1e6f3a381858071`. Preserve exact A/D snapshots in
[the cohort](cohorts/refinements-1/skills). B removes only D's added verification
paragraphs; C removes only D's added scouting paragraphs, including matching
optional reference paragraphs. Removing both additions must produce A byte for
byte. Keep licenses, evidence vocabulary, read-only rules, delegation guidance,
and three-lead/finding ceilings identical. No skill editing during trials.

Exactly **20 audit attempts**: five cases × four arms, no retries/replacements.
Additionally authorize exactly **two fresh Codex reviewer attempts**, no retries.
An isolated native curator prepares cases without seeing reports. Controller
and curator work are outside audit costs and will be disclosed separately.
Do not launch additional paid CLI sessions without user authorization.

All audit and reviewer sessions: locally authenticated Codex CLI,
`gpt-6.1-sol`, reasoning `low`, sandbox `read-only`, approval `never`, 180-second
hard wall limit, 12 inspection calls hard limit, 250,000 input-plus-output-token
instruction ceiling (verify afterward; not a hard token cap). Fresh persisted
session and neutral disposable tree every time. No resume, delegation, worker
code execution, test collection, builds, installs, edits, credentials, network
tools, or other-session access. Service inference uses the CLI's existing auth;
never export authentication material.

Use a standard-library evaluator-only MCP adapter exposing immutable supplied
UTF-8 file snapshots through list/read/literal-search. Exact allowlisted paths,
no symlinks, no execution/network/write interface; errors consume calls. Disable
shell, browser/computer, apps/plugins/hooks, web, memories, host skill discovery
and automatic project instructions. Manually load the supplied skill through
the adapter. This deliberately tests instruction content, not installer
discovery. Preserve all CLI arguments/prompts and adapter requests/results.
Unit-check out-of-scope reads, execution requests and over-budget requests before
launch. Stop if authentication, required adapter or usable controls fail;
retain the attempt and do not fabricate missing measurements. This qualifies
only this restricted inspection interface, not arbitrary-shell host isolation.

Order: s1 A B D C; s2 B C A D; s3 C D B A; s4 D A C B; s5 D C A B.
The first four cases balance arm positions and predecessor pairs; the fifth
creates a disclosed small imbalance. Run sequentially. No sampling seed or
server-load control is available; do not interpret latency differences as
causal estimates. Within each case, use identical question, project bytes,
permissions, tools and aggregate limits. Skill bytes alone differ.

## Frozen cases and judgments

The isolated curator authors five fresh synthetic repositories: consequential
cross-component/state-boundary defect; suspicious correct design; covered clean
implementation; ambiguous authoritative requirement; direct documentation
contradiction. Avoid all previous public teaching/pilot/pg-trickle examples.
Contracts, expected interpretations, accepted alternatives, criteria, exact file
hashes and evaluator oracle must be frozen before audits. Public project
contracts/tests go to workers; manifest, oracle, this protocol, prior results
and other arms stay inaccessible. Synthetic novelty is role/process separation,
not proof of absence from training data. Once published these are calibration
cases, not fresh evaluation evidence.

Controller may execute the curator's oracle and public tests as development
checks before audits; these receipts never turn workers' proposals into
performed experiments. Retain errors and any prelaunch corrections. Novel
source-supported findings can be valid even if absent from the manifest.

Primary scouting contrasts: B−A and D−C; verification contrasts: C−A and D−B.
Also show A/D. Assess actual source inspection choices and public scouting
messages, not finding count or headings. Ask whether consequential promises
were investigated, important boundaries missed, superficial leads wasted
effort, legitimate designs refuted, and no-findings/uncertainty preserved.

For unresolved consequential findings judge starting conditions/trigger,
observable oracle, supporting result, refuting/weaker alternative, assumptions,
and avoidable developer work. No requirement to fill fields when irrelevant.
Documentation contradictions favor a direct correction; unknown requirements
favor clarification. All executable follow-ups must say **PROPOSED — NOT RUN**.
Penalize unnecessary complexity, misleading certainty and verbosity.

Two fresh reviewers, neither case authors nor audit workers, each judge all
four anonymized reports for their assigned cases: reviewer 1 gets s1/s2/s3,
reviewer 2 s4/s5. Shuffle labels/order with seed 67, remove method disclosures
and normalize paths; retain exact originals and masking transformations.
Provide source/contracts, nonbinding expected interpretations, and source-only
probe records with skill contents/paths excluded. Withhold mapping, elapsed/token
costs and controller preferences until judgments are frozen. Treat inferred
origins as imperfect blinding. Reviewers must challenge the oracle, assess
correctness, misses, false positives, refutations, verification clarity, effort
and unnecessary complexity, and report ties/disagreements/negative results.
Reviewer judgments are independent **process-role model review**, not independent
human validation, measured developer savings, cross-model replication, or two
reviewers per case.

## Recording and decision

Retain exact inputs, before/after hashes, event logs, inspection requests/results,
CLI errors, exit status, elapsed time, input/cached/output tokens, report size,
reviewer inputs/judgments, source provenance and all attempts. Missing monetary
cost, active reasoning time, full OS telemetry and controller/curator tokens
are **UNAVAILABLE**, never zero. Input includes cached tokens; do not add them.
No children are authorized. Report infrastructure changes and mismatched or
incomplete runs rather than silently excluding them.

Choose **KEEP / SIMPLIFY / MODIFY / REVERT** separately. Useful incremental
selection or handoff improvement at acceptable observed cost supports KEEP;
equal outcomes do not establish equivalence. Extra instructions/cost without
demonstrated useful benefit supports SIMPLIFY or REVERT. MODIFY only for a
specific observed consequential failure, using the smallest change; do not
append edge-case checklists. Keep negative results and limits visible.

Issue closure requires a justified decision against each acceptance criterion,
not necessarily a positive experiment. If realistic-case or actionability
evidence is inadequate, leave that issue open and name the smallest remaining
experiment. Publish evidence and changes through a focused PR, pass full
regressions/install checks and CI, review/merge, then link evidence and explain
each issue's status. No extra paid reruns of a resulting simplification are
authorized; disclose when final shipped wording was not itself reevaluated.
