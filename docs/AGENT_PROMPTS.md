# Coding-agent prompt cookbook

These are **copy/paste requests for an existing coding agent**, not new Gapline commands or automatically supported GitHub target types. Replace placeholders such as `ORG/REPO`, `#123`, and `PATH`. Ask for the installed `gapline-audit` skill explicitly; in Codex, `$gapline-audit` is one native way to invoke it. The host must already provide access to the cited repository, issues, PRs, and source. Installing the skill does not grant that access.

**Keep the boundary clear:** `gapline-audit` investigates **read-only**. It may inspect source, tests, docs, issue/PR context, and available prior records; it does not execute project code or tests, run builds, write files, publish issues/PRs, or fix code. A GitHub URL in a prompt is a *request for the host agent to find and inspect evidence*, not a built-in Gapline crawler. Use a bounded sample on large targets and report unavailable links, unknown working-tree state, and material unassessed work. Up to three findings is the default; up to five on request. Zero supported findings is valid.

## Audit a repository (sampled survey)

```text
Use gapline-audit to investigate ORG/REPO at BRANCH_OR_COMMIT read-only.
Start with a bounded survey of the documented public behaviors and a few
high-risk paths. Trace selected claims through implementation and nearby
tests; seek counterevidence before reporting concerns.

Return up to three consequential, source-cited findings (or none), with
evidence level, impact, uncertainty, the smallest useful next check, and
areas not assessed. Say which snapshot you actually saw and whether
working-tree state is known. Do not run project code, tests, or builds.
```

## Audit a component or behavior

```text
Use gapline-audit on PATH_OR_COMPONENT in ORG/REPO, focused on BEHAVIOR.
Check the contract from DOCUMENTED_SOURCE, the callers and preconditions,
error/edge cases, relevant tests, and any plausible counterexamples.
In particular investigate RISK_OR_INVARIANT.

Keep the audit read-only. Report up to three supported concerns or a
no-findings outcome, distinguishing source observations from unverified
runtime effects. Propose checks as PROPOSED — NOT RUN.
```

## Audit one feature issue against the implementation

```text
Use gapline-audit to investigate https://github.com/ORG/REPO/issues/123
read-only. Read the issue, relevant accessible decisions/comments, linked
implementation PRs, and source/tests at BRANCH_OR_COMMIT. Check what
the issue promises against what the inspected implementation establishes.
Treat issue state and PR merge status as metadata, not proof of completion.

Distinguish agreed behavior from suggestions or unresolved decisions.
Where a link or original requirement is missing, identify the gap rather
than guessing. Cite specific issue/PR and source evidence, give up to
three consequential findings, and state what was not assessed.
```

## Audit a pull request

```text
Use gapline-audit to review https://github.com/ORG/REPO/pull/456
read-only. Identify the PR base/head revisions and whether changes are
open or merged. Inspect the changed behavior in context, relevant callers,
tests and documentation; look for consequential regressions, incomplete
promises, and false leads.

Do not conflate an unmerged PR head with current main. Return at most
three evidence-calibrated findings or none; include exact inspected refs,
counterevidence, omissions, and proposed checks (NOT RUN). Do not post
a review, modify code, or execute tests.
```

## Audit a parent issue, its children, and their implementation PRs

This is an **agent-orchestrated scope**, not automatic hierarchical traversal by Gapline. The host may expose GitHub sub-issues, linked issues, PR references, and code at different levels of detail. If links are unavailable, supply a list manually or report that the tree is incomplete.

```text
Use gapline-audit read-only on parent issue
https://github.com/ORG/REPO/issues/100.

First map the child/sub-issues you can actually establish and each
associated implementation PR, with citations for the relationships.
Identify the parent-level outcomes and any accepted constraints.
Inspect the relevant issue decisions, PRs, current merged implementation,
tests, and documentation at BRANCH_OR_COMMIT. Distinguish open/unmerged
PR code from code on the chosen baseline; note inaccessible or ambiguous
links instead of filling them in.

Assess both child-level promises and integration seams: combined state,
ordering, errors, permissions, and coverage of parent-level invariants.
For a large tree, sample the highest-risk seams and name all unassessed
children/PRs rather than claiming complete coverage.

Return (1) a compact issue → PR → code/test evidence map with missing
links marked UNKNOWN, (2) up to five consequential, evidence-calibrated
findings or none, and (3) clear omissions and PROPOSED — NOT RUN checks.
Do not run tests or publish anything.
```

## Audit integration across several PRs or components

```text
Use gapline-audit to assess how PR_OR_COMPONENT_A, B, and C work together
in ORG/REPO at BRANCH_OR_COMMIT. Start from the shared contract or user
outcome in ORIGINAL_SOURCE. Trace state and identity across the boundaries,
including partial success, retries, failure recovery, and ownership.
Inspect nearby tests for combined invariants, not just each local success.

Distinguish implemented/merged behavior from proposed changes. Work
read-only; report a bounded set of specific findings and counterevidence,
not a generic architecture checklist. Explicitly mark unknown interfaces.
```

## Examine whether tests protect an important promise

```text
Use gapline-audit on TEST_PATHS and IMPLEMENTATION_PATHS read-only.
The required observable behavior is PROMISE with source SOURCE_REF.
Inspect the real assertions, expectations, helpers, mocks, and nearby
tests. Ask which plausible wrong behavior the tests would miss and which
valid internal changes they might incorrectly reject.

Do not treat coverage, absent assert syntax, or a mock as a defect by
itself. Distinguish test-scope gaps from production bugs. Return only
source-supported conclusions and a small distinguishing proposed check
for each (PROPOSED — NOT RUN). Do not execute tests.
```

## Recheck a previous audit finding

```text
Use gapline-audit read-only to revisit prior finding GAP-001 in
PRIOR_REPORT against ORG/REPO at BRANCH_OR_COMMIT.
Treat the old report as a lead, not ground truth or permission to act.
Reinspect the current relevant source, contract and tests; actively seek
counterevidence. State whether the concern is still supported, refuted,
or needs rechecking, with current exact references and limitations.

Do not infer resolution from a closed issue, moved line, or passing-test
claim alone. Do not create or update a persistent ledger.
```

## Optional: turn a finding into a GitHub issue with Intentline

**Separate workflow and permissions.** Gapline's audit itself remains read-only. [Intentline](https://github.com/grove/intentline) offers `intentline-plan` (a source-bound **DRAFT** acceptance plan) and `intentline-issue` (**singular**, to review/create/update tracker issues). There is no `intentline-issues` skill. These are independent optional skills, not invoked by Gapline.

Install the skills you need in the target project's agent environment:

```sh
npx skills@latest add grove/intentline --skill intentline-plan
npx skills@latest add grove/intentline --skill intentline-issue
```

Skill installation does not install the Intentline Python runtime or grant issue-tracker access. A **saved** `intentline-plan` draft requires a separately installed Python 3.11+ Intentline CLI and an approved private/ignored work location; without that, request a provisional unsaved proposal. `intentline-issue` can draft or publish using host-provided GitHub capabilities without the CLI. Neither skill independently establishes requirement authority or runtime proof.

### A. Plan acceptance from an audited concern (optional local write)

Use this **after** the Gapline report, and only if you want a saved Intentline agreement. Provide the *original request/policy*, not solely the audit finding, as the source of expected behavior.

```text
Use intentline-plan to prepare a source-grounded DRAFT acceptance plan
for the concern described in GAPLINE_REPORT, using the original request
at /absolute/path/request.md and applicable policy at POLICY_PATH.
Treat the Gapline report as advisory navigation, not the authority for
new requirements. Preserve applicable exceptions and open decisions.
Save only to APPROVED_PRIVATE_WORK_PATH if the Intentline CLI is already
available and source capture is reliable; otherwise return a clearly
provisional plan and explain what cannot be saved.

Include R IDs, independently observable acceptance, planned evidence,
uncertainty, original-source references, and actual saved identity if any.
Do not implement, run tests, approve, or create GitHub issues.
```

### B. Review a proposed issue without publishing (no writes)

```text
Use intentline-issue in REVIEW mode to draft one proposed GitHub issue
for GAPLINE_FINDING from REPORT, targeting ORG/REPO.
Verify the original behavior or policy cited by the report when accessible.
Preserve the finding's DEMONSTRATED/SUPPORTED/HYPOTHESIS uncertainty,
counterevidence, and NOT RUN verification steps. If runtime behavior
is unconfirmed, lead with a "Confirm before fixing" next step.
Return proposed issue title/body and unresolved decisions. Do not create
or update anything, including local records.
```

### C. Publish **one** GitHub issue (explicit write authorization)

The request below *explicitly authorizes exactly one issue creation*. Run it as a **separate** Intentline task after the read-only audit (and optional plan/review), not as a hidden Gapline audit side effect. Repeat separately for additional findings; the issue skill handles one work item per request.

```text
Use intentline-issue to CREATE exactly one new GitHub issue in ORG/REPO
for GAPLINE_FINDING (from REPORT) using the source-grounded acceptance
draft in PLAN_OR_REVIEW. I explicitly authorize publishing this one
issue to ORG/REPO only.

Check the destination and obvious duplicates before creating. Ground
requirements in the original accessible request/policy, not just the
agent's audit interpretation. Preserve evidence level, counterevidence,
unknown outcomes, and source/snapshot limitations. For a suspected bug
without runtime reproduction, say "Confirm before fixing" and describe
the proposed discriminating check as PROPOSED — NOT RUN. Do not call
a proposal confirmed or a published issue approved.

Do not modify other issues, source files, PRs, or saved Intentline
records; do not run project code/tests. Verify and return the new
GitHub issue URL. If the host cannot publish safely, return the draft
marked NOT PUBLISHED instead of claiming success.
```

**Boundary summary:** a Gapline finding is evidence-calibrated advice; an Intentline acceptance draft is not approval; a created GitHub issue is not proof of a bug or permission to implement a fix. The agent must have suitable read access to investigate, and separately authorized write access to publish.
