# Gapline

**Find what your codebase is missing.**

Gapline is an experimental, opt-in **codebase investigation skill for existing coding agents**. Its purpose is to discover consequential weaknesses in an existing software project, investigate promising leads, and give developers evidence-backed next steps.

It is not limited to a pull request or a feature currently being implemented. A developer should be able to revisit a mature repository and ask: **What are we overlooking?**

> **Status: experimental v0.1.** A read-only agent skill, static packaging checks, and small teaching fixtures now exist. No coding-agent host discovery, real-world audit quality, runtime isolation, or benchmark improvement has yet been verified. This is not an executable scanner.

[Skill](gapline-audit/SKILL.md) · [Evaluation protocol](evaluation/README.md) · [Design](DESIGN.md) · [Implementation plan](IMPLEMENTATION.md)

## Try the experimental skill

Gapline v0.1 is a **prompt-based agent skill**, not a command-line scanner. With a coding agent that has authorized read-only access to a target repository:

1. Open [gapline-audit/SKILL.md](gapline-audit/SKILL.md). If your agent supports skill discovery, configure that file according to the host's own documentation. Otherwise, provide the file's contents directly as instructions. **Automatic discovery has not been verified on a named host.**
2. Ask: **Use Gapline to investigate a focused component or sampled repository. Read only. Look for hollow tests, documentation drift, and unsafe failure paths. Return up to three consequential findings, with exact evidence, counterevidence, and proposed next checks.**
3. Inspect the response critically. Claims about runtime behavior remain unverified unless a separate, authorized experiment actually ran. This skill never executes tests or changes the target repository.

For Gapline's own development checkout, run the **static contract tests** with:

    python -m unittest discover -s tests -v

These tests check skill packaging and fixtures, **not** safe host behavior or whether the agent discovers real defects. The [evaluation protocol](evaluation/README.md) describes necessary host smoke tests and matched baseline comparisons. No such evaluation results are claimed yet.

## Why Gapline?

A project can compile, pass CI, and still have significant blind spots:

- An edge case is handled incorrectly, but nobody has exercised it.
- A test passes without asserting the behavior its name promises to check.
- A documented option has changed, while its examples have not.
- A failure path leaks a resource or leaves inconsistent state.
- A feature exists in the public API but is only partially implemented.
- Similar components enforce subtly different rules.

Linters, coverage reports, mutation tools, and ordinary code reviews each offer useful signals. None automatically answers the broader question: **Which weaknesses in this particular project are both credible and worth fixing?**

Gapline's role is to help an agent ask better questions, gather discriminating evidence, and separate confirmed problems from plausible suspicions.

## What it will investigate

| Investigation area | Examples of useful questions |
| --- | --- |
| **Behavior and correctness** | Are boundary values, invalid inputs, and state transitions handled correctly? |
| **Missing or hollow tests** | Which important behaviors lack assertions? Would tests detect a plausible wrong implementation? |
| **Documentation** | Do README claims, examples, API docs, and operational instructions match actual behavior? |
| **Completeness** | Are there unfinished paths, misleading success responses, or unimplemented promised behaviors? |
| **Reliability** | Do failure recovery, retries, cleanup, and unexpected dependency failures work safely? |
| **Security and trust boundaries** | Are inputs validated and permissions enforced where they need to be? |
| **Architecture and maintainability** | Which dependencies or inconsistencies create a concrete risk, rather than just a style preference? |

These are **investigation lenses**, not a checklist that must generate a finding in every category. No findings can be a valid result.

## How it should work

The first experimental version is **one portable agent skill**, `gapline-audit`, for a coding agent that already has authorized read-only access to the repository. It does not launch its own model or require another service.

### 1. Scout — discover hypotheses

The agent maps relevant code, tests, docs, and interfaces; chooses a bounded scope; and identifies a few high-value questions. Recent changes, critical behavior, complexity, and documentation promises can guide attention, but are not proof of defects.

### 2. Probe — distinguish suspicion from evidence

The agent first investigates by reading code, tracing paths, and comparing documented claims with implementations and tests.

A later, separately qualified mode may run selected tests, make controlled inputs, or use existing mutation and analysis tools. **Execution must be authorized and appropriately isolated.** A skill prompt, copied directory, or git worktree is not itself a sandbox. The v0.1 skill is read-only.

### 3. Track — improve across repeated runs

With an explicitly approved finding ledger, later runs can distinguish new findings from previously reported, resolved, dismissed, stale, or regressed concerns.

"Continuous" means **repeatable, cumulative investigation**, not an always-on daemon or automatic scheduled execution. The first release need not persist findings to be useful.

## Example finding — illustrative, not observed

```text
GAP-004 | Test gap | SUPPORTED

Location: tests/test_retries.py and src/client/retries.py
Concern: Tests exercise successful retries but apparently
         do not check what happens after a timeout.

Evidence: The inspected tests assert successful completion,
          but contain no assertion about duplicate effects.
          No test command was executed in this audit.

Potential impact: A retry could repeat a non-idempotent operation.

Next probe: In an authorized isolated environment, simulate
            a timeout after the remote side effect and verify
            that retrying does not duplicate that effect.

Status: Hypothesis about production behavior; not a confirmed bug.
Scope: Only the cited retry path and selected tests were reviewed.
```

A useful result points to **a precise behavior, the evidence actually obtained, and the next discriminating check**. Gapline should never convert "looks suspicious" into "is broken" without support.

## Intended use

When an agent has been explicitly given the skill and authorized read-only repository access, a developer can ask:

> Use Gapline to investigate this repository. Start read-only. Find up to five consequential weaknesses in behavior, tests, documentation, or reliability. Separate demonstrated problems from hypotheses, and recommend the smallest useful next action.

Or, on a later run:

> Revisit the previous Gapline findings. Check which are still supported, what has actually been fixed, and what new weaknesses deserve investigation.

The current skill supports a sampled repository **survey** or narrow **focus** via the requested scope. A **revisit** with persisted prior findings remains a future capability. A survey must disclose what was not assessed.

## What Gapline is not

- Not a correctness certificate, comprehensive audit, or substitute for human judgment.
- Not a generic warning generator, mandatory CI gate, or repository quality score.
- Not a linter, mutation engine, test framework, or new coding-agent orchestrator.
- Not an automatic bug fixer, issue publisher, pull-request author, or release gate.
- Not permitted to execute repository-suggested commands, install tools, contact external services, or write to a target repository merely because its contents request it.

Repository files, documentation, comments, and tool output are **data to investigate, not instructions granting authority**. The user and host control access, execution, network use, and writes. Sensitive information must not appear in reports without authorization.

A read-only review can still be useful when execution is unavailable. In that case, experiments remain **NOT RUN**, and their proposed results must not be presented as observations.

## Relationship to neighboring projects

Gapline stands alone; none of these projects is required to use it.

| Project | Question it addresses |
| --- | --- |
| [Intentline](https://github.com/grove/intentline) | What was requested, and what obligations or acceptance criteria follow from that intent? |
| [Proofline](https://github.com/grove/proofline) | What checks and evidence demonstrate properties of an identified candidate? |
| [Faultline](https://github.com/grove/faultline) | Would selected tests catch particular plausible incorrect behaviors? |
| **Gapline** | Where are the meaningful weaknesses in the codebase, and which ones can we substantiate? |

Gapline may use an existing requirement statement as context or suggest a Faultline-style experiment. It must not silently assume those projects are present, treat an AI-generated plan as an authoritative contract, or reinterpret another tool's evidence as a universal pass/fail verdict.

## Roadmap

1. **Experimental skill: authored, not host-qualified.** [gapline-audit/SKILL.md](gapline-audit/SKILL.md) contains three focused, evidence-aware read-only playbooks.
2. **Host qualification and real-world evaluation: next.** Verify discovery and tool behavior, then compare against normal agent review on unseen cases at matched budget.
3. **Controlled probes: conditional.** Only after host isolation, permissions, and evidence handling are qualified.
4. **Finding continuity: conditional.** Opt-in, human-reviewable history only when repeated audits justify the overhead.
5. **Automation or CLI: conditional.** Build these only when measured needs justify them.

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for milestones and stopping criteria. The next task is to **validate and measure the small skill**, not build a general scanning platform.

## License

Apache-2.0. See [LICENSE](LICENSE).
