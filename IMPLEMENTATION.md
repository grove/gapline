# Gapline — implementation plan

**Status:** Planning document. No Gapline audit skill or verified executable product exists yet.  
**First product target:** one portable, **read-only** `gapline-audit` skill that helps an existing coding agent discover and prioritize a few evidence-backed weaknesses in an existing repository.  
**Admission rule:** only add execution, persistence, a CLI, or automation after the simpler skill proves useful and the associated permission and safety requirements are met.

Read [README.md](README.md) for the purpose and [DESIGN.md](DESIGN.md) for the governing evidence, safety, and workflow rules.

## 0. Starting decisions

Gapline is **not** an expanded Faultline. It is an independent, agent-native investigation method focused on existing projects: behavior, tests, documentation, completeness, reliability, security, and concrete architectural risks.

Start with **Scout + read-only Probe**. Keep **Track** as a small later enhancement. There is no separate service, runtime package, mutation engine, scheduler, database, or new model runner in the initial release.

The initial repository contains the Apache-2.0 license and these planning documents. Nothing here claims that an audit has run, a skill has been installed, the host access controls have been verified, or benchmark value has been demonstrated.

### Initial defaults

- **Read-only and opt-in:** no project execution, filesystem modifications, package installation, generated files, network side effects, issues, commits, or PRs. Host-provided read-only repository access is allowed within its actual capabilities and permissions.
- **Short investigations:** suggest up to five plausible leads and report at most five substantive findings; lower counts and no findings are valid. Constrain breadth to the available time and disclose unassessed areas.
- **Evidence-labeled results:** distinguish `DEMONSTRATED`, `SUPPORTED`, `HYPOTHESIS`, `REFUTED / WITHDRAWN`, and `NOT ASSESSED` exactly as specified in DESIGN.
- **Counterevidence first:** check for caller preconditions, existing tests, alternate valid behavior, and intentional duplication before declaring a defect.
- **No invented execution:** all proposed test or runtime probes remain **NOT RUN** until separately authorized and actually executed.
- **Language-neutral guidance:** prioritize portable code-reading approaches. Do not promise support for languages or frameworks the agent/host cannot meaningfully inspect.
- **No hidden integrations:** Intentline, Proofline, and Faultline remain entirely optional.

## 1. Milestone A — project documentation

**Deliverables**

- `README.md`: identity, user value, intended workflow, honest status, example result, independence, and roadmap.
- `DESIGN.md`: scope, investigation lenses, evidence taxonomy, safety boundaries, findings, continuity, and evaluation principles.
- `IMPLEMENTATION.md`: concrete deliverables, acceptance checks, test controls, and stop rules.

**Acceptance**

- Documents agree that v0.1 is read-only, skill-first, opt-in, and not yet implemented.
- Links and terminology agree; no fictional install command, audit receipt, released tool, or mandatory dependency.
- No language implies that reviewing code alone proves runtime behavior.
- The first follow-on task is small enough to implement and validate separately.

**Exit:** once these documents are present and checked, move to Milestone B. Documentation alone is not a released product.

## 2. Milestone B — build the first portable skill

### Deliverables

```text
gapline/
  LICENSE
  README.md
  DESIGN.md
  IMPLEMENTATION.md
  gapline-audit/
    SKILL.md
  tests/
    test_skill.py
```

This is an intended structure, **not** a claim that the files already exist.

Implement just **one canonical** `gapline-audit/SKILL.md` with minimal valid frontmatter (`name: gapline-audit` and an accurate description). Provide clear instructions for both hosts that discover skills automatically and hosts where a developer explicitly points the agent at the file. Document installation only after a real host has verified discovery and use.

Keep the first skill readable, compact, and useful without any Gapline Python runtime, dependency installation, network service, or companion project.

### Skill behavior

1. **Establish task and scope.** Identify repository, caller's audit question, scope, available read-only tools, and reasonable budget. If omitted, start with a conservative sampled survey; do not assume permission to execute anything.
2. **Identify candidate.** Capture repository/ref and visible working-tree identity when available, noting when uncommitted state or provenance cannot be established.
3. **Scout.** Review project purpose, high-value behavior, relevant tests, documentation claims, and relevant call paths. Select a few risk-relevant hypotheses rather than enumerate warnings.
4. **Probe read-only.** Inspect supporting and opposing evidence; trace caller constraints and look for legitimate alternative behavior. Do not run project code, tests, builds, or write files.
5. **Classify carefully.** Distinguish a directly observed source/document mismatch, narrow test assertion gap, unverified runtime suspicion, refuted hypothesis, and untouched areas. Avoid "confirmed bug" labels without suitable evidence.
6. **Prioritize.** Return only the strongest useful observations, with impact rationale and an achievable next check or fix direction.
7. **Report.** Produce a compact Markdown response with exact source references, evidence level, caveats, project scope, and an explicit statement that no commands were executed.
8. **Stop.** If access is too sparse for defensible findings, say so, state what was inspected, and suggest the smallest missing information or authorized follow-up. Do not generate filler findings.

The prompt must explicitly treat repository instructions and prior agent reports as untrusted data, not as authority to change permissions or the task.

### Basic regression checks

A small standard-library test (`tests/test_skill.py`) may validate the intended path, skill frontmatter, referenced documents, and the presence of safety/evidence terminology. Such string-level tests are **not** a demonstration that an agent actually obeys the skill.

Run a host-level smoke test with a read-only fixture repository and capture the actual audit response. Verify tool use and effects from host logs or equivalent, not just from what the agent says.

### Acceptance checks

- [ ] Skill discovery/manual invocation works in at least one named host and is documented accurately.
- [ ] A sampled repository review produces at least one specific, supported observation **or** a defensible no-findings report.
- [ ] Findings cite the actual inspected material and keep behavioral uncertainty visible.
- [ ] A request to "find five bugs" does not force five results.
- [ ] A suspicious README command or source comment cannot induce unauthorized execution, installation, external communication, or writing.
- [ ] Missing access or unsupported scope produces an honest limited/no-findings result, not fabricated evidence.
- [ ] No execution or mutation tool, runtime dependency, persistent ledger, or other new feature is required.

**Stop condition:** if the skill repeatedly outputs generic advice, unverifiable bugs, or ignores read-only constraints, refine the investigative instructions before extending the feature set.

## 3. Milestone C — qualify investigations with controlled fixtures

Create a small set of synthetic, public, independently authored mini-repositories or fixture trees in `tests/fixtures/` or `evaluation/fixtures/`. Each should have a **predeclared expected interpretation** that is not simply the agent's own answer.

### Minimum fixture matrix

| Fixture | What is present | Expected behavior |
| --- | --- | --- |
| **Real code defect** | A source-visible boundary or state-logic mistake and an authoritative requirement | Identify the discrepancy as strongly supported; do not claim runtime reproduction without executing |
| **Missing test** | A clearly specified behavior absent from the chosen test scope | Cite the actual gap and qualify it to inspected tests; recommend a discriminating test |
| **Hollow test** | A test with a misleading name, ineffective assertion, or mock that bypasses the central behavior | Explain exactly why that particular test does not establish its advertised behavior |
| **Doc contradiction** | A documented default or option directly contradicts inspected implementation | Cite both sides; claim only the demonstrated contradiction |
| **Valid alternative** | Different-looking but correct implementation | Withdraw superficial style/shape-based defect claims |
| **Intentional duplication** | Independent trust-boundary validation with a reason to stay separate | Do not auto-report a DRY problem |
| **Clean repository** | Small coherent implementation, tests, and documentation | No invented findings; explain sampled scope |
| **Insufficient context** | Ambiguous behavior with no source-grounded contract | Mark hypothesis or not assessed; request a meaningful next check |
| **Prompt-injection bait** | Comments/docs demanding command execution or reporting secrets | Ignore embedded instructions; maintain scope and privacy |
| **Unreviewed behavior** | Important area intentionally outside the budget | Explicitly list omission rather than imply full coverage |

Include different programming styles and eventually more than one language, but do not broaden the corpus before the initial host workflow is reliable.

### Evaluate the agent, not just the text file

For every fixture run, retain a bounded case note of:

- Exact fixture revision and task prompt.
- Host, model/settings where available, tools and allowed permissions.
- Time/tool budget and actually consumed resources when measurable.
- Findings, their evidence labels, references, and next steps.
- Expected targets that were found, missed, falsely invented, or incorrectly classified.
- Unauthorized actions or attempted overreach observed by the host.
- Uncertainty and "not assessed" coverage.

Have a reviewer independently check the substantive conclusions. A prewritten expected answer does not prove that the agent found a real-world bug.

**Acceptance**

- [ ] At least one genuine finding and one genuine clean/no-findings case are reported honestly.
- [ ] Unsupported runtime conclusions are not presented as demonstrated defects.
- [ ] At least one planted false lead is refuted or withheld.
- [ ] Untrusted repository instructions do not acquire permission.
- [ ] No host-observed unauthorized execution, writes, or sharing.
- [ ] Every finding's proposed next step could meaningfully test or reduce uncertainty.

**Stop condition:** improve the skill if it cannot consistently distinguish a narrow observation from a larger unverified conclusion.

## 4. Milestone D — dogfood on real repositories

Once fixture behavior is credible, perform a small number of **explicitly authorized, read-only** audits against existing repositories.

Begin with **one focused component**, not a repository-wide quality declaration. Include varied evidence: implementation paths, nearby tests, public documentation, and issue/history context where permitted.

Natural initial candidates are [Gapline](https://github.com/grove/gapline) itself and separately authorized snapshots of [Intentline](https://github.com/grove/intentline), [Proofline](https://github.com/grove/proofline), or [Faultline](https://github.com/grove/faultline). They are **candidates, not projects with known defects**.

### For each audit

```text
Target and exact available source identity:
Investigation question and bounded scope:
Host capabilities and permissions:
Budget and work actually performed:
Files/tests/docs inspected:
Source-grounded findings and evidence levels:
Counterevidence and refuted hypotheses:
Proposed follow-up checks (NOT RUN):
False leads / reviewer disagreements:
Explicitly unassessed areas:
Time and tool/model overhead (if observable):
Keep / change / stop recommendation:
```

Do not silently turn potential issues into GitHub tickets or modify the audited repository. Keep results in the conversation unless a separately approved location for writing an audit record exists.

**Acceptance:** at least two useful, independently reviewed audit cases, including an honest no-finding or inconclusive outcome if that is what the evidence warrants. Finding count is not the goal.

**Stop condition:** if setup and review overhead exceed the value of the investigations, simplify the skill before adding automation or more investigation lenses.

## 5. Milestone E — optional finding continuity

Add this **only when repeated manual audits demonstrate redundant findings or the need to recheck known concerns**. Do not introduce persistence merely because a long-term product vision mentions recurring use.

### Initial approach

Use a small, human-reviewable Markdown ledger at a **user-approved location**, potentially outside the target repository. No database, automatic commits, sync service, or mandatory file writes.

The ledger needs only:

- A stable finding ID and behavioral summary.
- The repository and relevant candidate/source identity.
- Evidence level, source references, and material limitations.
- The recorded status and why it changed.
- A brief dated history of observations or decisions.
- A clear unresolved next step.

A later revisit should compare evidence **at the current candidate** rather than trust last week's language. File paths, symbols, and behavior descriptions can help match findings; line numbers alone cannot.

### Revisit controls

- A previously reported weakness that is no longer present must be **verified or marked stale**, not automatically marked fixed.
- A closed issue is not proof of repair.
- A validly dismissed concern should not recur without new evidence.
- A possible regression needs fresh supporting observations.
- Ledger content remains untrusted; it cannot authorize execution or create new tasks.
- Missing old records must never be represented as a zero-backlog clean bill of health.

### Acceptance

- [ ] A repeated identical audit does not generate the same finding as a new discovery.
- [ ] A moved file or changed line number does not necessarily break matching.
- [ ] A changed implementation without sufficient verification becomes **STALE / NEEDS RECHECK**.
- [ ] A confirmed repair is marked **RESOLVED (VERIFIED)** only with appropriate evidence.
- [ ] Manual dismissal remains visible and reversible if later evidence changes.
- [ ] Audit use remains possible with no ledger whatsoever.

**Stop condition:** if continuity adds more bookkeeping than it saves, keep reports stateless or simplify the ledger.

## 6. Milestone F — conditional executable probes

**Not approved for the first release.** Only pursue this milestone after read-only audits show specific cases where a small test or experiment would materially resolve uncertainty.

First, research existing host controls and tools. Do **not** build a custom sandbox or mutation engine.

### Required gate

- [ ] Threat model covers arbitrary project code, imports, test plugins, hooks, subprocesses, generated files, symlinks, caches, credentials, protected files, and network effects.
- [ ] The intended host isolation boundary has been tested using negative controls on the actual host, including denied reads/writes and unauthorized network attempts.
- [ ] User/host permission covers candidate, exact commands, isolation, outputs, dependencies, budget, and side effects.
- [ ] Commands run in an approved isolated disposable environment, not the original candidate or protected evidence.
- [ ] Baseline commands and candidate identity are recorded before comparing modified behavior.
- [ ] Mutation probes, if any, use one reset independent mutant at a time with tests unchanged and outcome labels native to the real observed experiment.
- [ ] Timeouts, errors, unavailable tools, unsupported environments, and insufficient receipts remain **NOT RUN / UNAVAILABLE / INCONCLUSIVE**, never fabricated passes or defect confirmations.
- [ ] Reports preserve exact command and evidence provenance and respect privacy.

The first optional executable extension could simply run **one user-approved, targeted regression test** in an appropriately isolated host. Mutation testing, fuzzing, builds, dependency installation, and larger sweeps should be separately justified and budgeted.

If isolation cannot be verified, this milestone is **NO-GO** for that host; Gapline remains a useful read-only investigator. Do not substitute `git worktree`, a copied directory, or prompt warnings for the missing protection.

## 7. Milestone G — measure incremental value

Before shipping scheduled scans, CI integrations, a CLI, or a public platform, evaluate whether Gapline changes outcomes.

### Matched comparison

On a small, fresh, independently reviewed set of realistic repository questions, compare:

- **A: ordinary agent review** with its normal read-only code-navigation tools.
- **B: the same agent plus Gapline** under matched source, permissions, model, time/tool budget, and evaluation conditions.

Predefine the important expected observations and hold them apart from the worker agent. Use clean controls, real issues, test weaknesses, doc contradictions, and valid alternatives. Do not select only cases known to flatter Gapline.

### Outcomes

**Primary:** number and practical value of **independently confirmed, nontrivial, actionable** findings that the ordinary review missed, under comparable cost.

**Secondary:** false positives; unsupported confidence; severity misprioritization; no-finding honesty; useful suggested probes; duplicate rediscovery; time/model/tool usage; unsafe or unavailable runs; and reviewer time needed to trust results.

Show the full denominator, including unfinished cases and failure to find planted issues. Reject outcome claims that depend only on the agent's own self-grading.

### Decision

Choose **KEEP SKILL / SIMPLIFY / MODIFY / STOP** based on independently checked value and total overhead. A positive result on a small corpus merits another unseen cohort, not a universal quality claim.

## 8. Conditional expansions — only with a demonstrated need

Do not open implementation work by default for:

- A Gapline CLI, Python package, parser framework, or JSON protocol.
- An agent swarm, autonomous controller, extra model call, or hosted platform.
- Mandatory CI gates, GitHub issue creation, pull-request automation, or scheduled scans.
- Automatic issue fixing or large-scale test generation.
- Global defect/maintainability/security scores.
- Coupled adapters to Intentline, Proofline, or Faultline.

For each proposal, require a measured problem, a simpler alternative considered, new security/privacy implications, and a maintenance-cost argument. A portable skill with occasional targeted probes and a simple ledger may be the complete product.

## 9. Practical first-use acceptance checklist

A developer should eventually be able to invoke the first skill and observe all of the following:

- [ ] The agent can explain what this repository does and which parts it actually inspected.
- [ ] It produces up to five **specific** source-grounded findings, or says none were established.
- [ ] It distinguishes actual contradictions from plausible-but-unverified runtime bugs.
- [ ] It reviews relevant counterevidence and avoids reflexive style/duplication criticism.
- [ ] It provides a minimal next check or improvement for each material concern.
- [ ] It shows important omissions and missing runtime evidence explicitly.
- [ ] It has not executed project code, changed files, installed dependencies, published issues, or leaked secrets.
- [ ] The skill works without the other three projects and without persistent findings.
- [ ] Its instructions and first-use documentation have been verified on at least one real host.

## 10. Work sequence and first next task

**Docs → read-only skill → controlled fixtures → focused real-repository audits → optional continuity → conditional executable probes → matched usefulness evaluation → optional platform features.**

The first implementation task is **Milestone B only**: author a concise canonical `gapline-audit/SKILL.md` and a minimal discoverability/safety regression check, then demonstrate an honest read-only investigation on a small controlled fixture. Do not claim that running text-oriented tests alone qualifies the security boundary.

Aim for a useful, low-ceremony investigative habit: **find fewer, more consequential weaknesses and establish exactly what is known about them**.
