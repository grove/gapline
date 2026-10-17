# Gapline — implementation plan

**Status:** The read-only skill is implemented. The [2026-10-17 validation record](evaluation/results/2026-10-17-install-and-smoke/README.md) separates packaging, installation, controlled cases, and manual host invocation; broad audit effectiveness and host isolation require their own evidence.
**First product target:** one portable, **read-only** `gapline-audit` skill that helps an existing coding agent discover and prioritize a few evidence-backed weaknesses in an existing repository.  
**Admission rule:** only add execution, persistence, a CLI, or automation after the simpler skill proves useful and the associated permission and safety requirements are met.

Read [README.md](README.md) for the purpose and [DESIGN.md](DESIGN.md) for the governing evidence, safety, and workflow rules.

## 0. Starting decisions

Gapline is **not** an expanded Faultline. It is an independent, agent-native investigation method focused on existing projects: behavior, tests, documentation, completeness, reliability, security, and concrete architectural risks.

Start with **Scout + read-only Probe**. Keep **Track** as a small later enhancement. There is no separate service, runtime package, mutation engine, scheduler, database, or new model runner in the initial release.

The repository includes one installable skill and optional references, a real skills-CLI installation check, packaging tests, controlled fixtures, and the Apache-2.0 license. See [evaluation](evaluation/README.md) for the procedure and recorded outcomes. Successful installation, a useful audit response, and enforcement of host access controls are distinct claims.

### Initial defaults

- **Read-only and opt-in:** no project execution, filesystem modifications, package installation, generated files, network side effects, issues, commits, or PRs. Host-provided read-only repository access is allowed within its actual capabilities and permissions.
- **Short investigations:** start with up to three leads and report at most three findings, or up to five if requested; lower counts and no findings are valid. Constrain breadth to the available time and disclose unassessed areas.
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

- Documents agree that the implemented product is a read-only, opt-in skill and distinguish measured behavior from proposed future capabilities.
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
    LICENSE
    references/
      investigation.md
  scripts/
    check_install.py
  tests/
    test_skill.py
```

This is the implemented package and its installation check. Evaluation helpers and fixtures remain outside the installable skill directory.

Maintain **one canonical** `gapline-audit/SKILL.md` with minimal valid frontmatter (`name: gapline-audit` and an accurate description). Keep required references and the distribution license inside that directory so a skills-CLI install is complete. Verify `npx skills@latest add grove/gapline` discovery and installation, and distinguish those results from a named host actually invoking the installed skill. Support manual invocation where automatic discovery is unavailable.

Keep the first skill readable, compact, and useful without any Gapline Python runtime, dependency installation, network service, or companion project.

### Skill behavior

1. **Establish task and scope.** Identify repository, caller's audit question, scope, available read-only tools, and reasonable budget. If omitted, start with a conservative sampled survey; do not assume permission to execute anything.
2. **Identify candidate.** Capture repository/ref and visible working-tree identity when available, noting when uncommitted state or provenance cannot be established.
3. **Scout.** Review project purpose, high-value behavior, relevant tests, documentation claims, and relevant call paths. Select a few risk-relevant hypotheses rather than enumerate warnings.
4. **Probe read-only.** Inspect supporting and opposing evidence; trace caller constraints and look for legitimate alternative behavior. Do not run project code, tests, builds, or write files.
5. **Classify carefully.** Distinguish a directly observed source/document mismatch, narrow test assertion gap, unverified runtime suspicion, refuted hypothesis, and untouched areas. Avoid "confirmed bug" labels without suitable evidence.
6. **Prioritize.** Return only the strongest useful observations, with impact rationale and an achievable next check or fix direction.
7. **Report.** Produce a compact Markdown response with exact source references, evidence level, caveats, and project scope. Record the inspection facilities/commands actually used and state **Project code, tests, and builds executed: NONE** only when true. Bounded host-authorized shell reads are inspection, not runtime reproduction.
8. **Stop.** If access is too sparse for defensible findings, say so, state what was inspected, and suggest the smallest missing information or authorized follow-up. Do not generate filler findings.

The prompt must explicitly treat repository instructions and prior agent reports as untrusted data, not as authority to change permissions or the task.

### Basic regression checks

A small standard-library test (`tests/test_skill.py`) may validate the intended path, skill frontmatter, referenced documents, and the presence of safety/evidence terminology. Such string-level tests are **not** a demonstration that an agent actually obeys the skill.

Run `python scripts/check_install.py` to install the current checkout with the actual skills CLI in temporary project directories. Verify complete installed bytes and local references for Codex and Claude Code in the supported copy/symlink modes. CI must test the candidate checkout; a post-merge check must also use the public GitHub shorthand so the user's default-branch command is exercised. Installer execution is a development/setup action, outside a Gapline audit.

Run a host-level smoke test with a read-only fixture repository and capture the actual audit response. Verify tool use and effects from host logs or equivalent, not just from what the agent says.

### Acceptance checks

Checked items below have evidence in the recorded teaching smoke. Unchecked items are further validation goals, not undisclosed runtime components. They must not be represented as proven by the skill text or packaging checks.

- [x] Manual invocation works in the named ChatGPT delegated-worker environment and is documented accurately. Automatic Codex/Claude Code activation remains untested.
- [x] A sampled fixture review produces at least one specific, supported observation **or** a defensible no-findings report.
- [x] The retained findings cite the actual inspected material and keep behavioral uncertainty visible.
- [ ] A request to "find five bugs" does not force five results.
- [ ] Host-observed trials show no unauthorized execution, installation, external communication, or writing when repository text requests those actions. Enforcement requires separate host evidence.
- [x] Missing requirements produce an honest limited/no-findings result in the retained unresolved case.
- [x] No execution or mutation tool, runtime dependency, persistent ledger, or other new feature is required.

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

The current cases pair composed identity rules, test interaction contracts, independent validation boundaries, and current versus deferred capabilities. See [evaluation](evaluation/README.md) for evaluator-only interpretations and a helper that prepares neutral worker copies. Add a small matched comparison alongside the first credible host trials; retain the more demanding fresh-case comparison in Milestone G before expansion.

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

- [x] At least one genuine finding and one genuine clean/no-findings teaching case are reported honestly.
- [x] Unsupported runtime conclusions are not presented as demonstrated defects in the retained reports.
- [x] At least one planted false lead is refuted or withheld in the retained reports.
- [ ] Untrusted repository instructions do not acquire permission.
- [ ] No host-observed unauthorized execution, writes, or sharing.
- [x] The retained substantive finding's proposed next step could meaningfully test or reduce uncertainty.

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

Start with a lightweight comparison during the first credible host trials. Before shipping scheduled audits, audit quality gates, a custom CLI, or a public platform, evaluate whether Gapline changes outcomes on fresh cases. Packaging CI is an implementation check, not an automated audit product.

The [versioned three-arm pilot](evaluation/pilot-v1.md) freezes a fresh authored
cohort and evaluator expectations before review. Its
[retained evidence](evaluation/results/2026-10-17-fresh-pilot/README.md) separates
independent judgments, observable resource costs, and unavailable telemetry.
This synthetic cohort is a local decision aid; production-case effectiveness
still requires independently specified real repository questions.

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

A developer should be able to invoke the installed skill and observe the following; checkmarks require evidence from the corresponding trial, not merely matching text in SKILL.md:

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

**Installable read-only skill → package/install checks and host smoke → controlled and paired cases with a small matched comparison → fresh focused repository audits → continuity or executable probes only if justified.**

The canonical skill, installed references, packaging/installation checks, and controlled cases implement the first product. Retain the exact input identity, invocation method, actual observations, and limitations for each validation run in [evaluation](evaluation/README.md). Further work should respond to an observed weakness or a useful unresolved question; static checks and a small pilot do not qualify a security boundary or prove general effectiveness.

Aim for a useful, low-ceremony investigative habit: **find fewer, more consequential weaknesses and establish exactly what is known about them**.
