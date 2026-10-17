# Gapline

**Find what your codebase is missing.**

Gapline is a proposed, opt-in **codebase investigation skill for existing coding agents**. Its purpose is to discover consequential weaknesses in an existing software project, investigate promising leads, and give developers evidence-backed next steps.

It is not limited to a pull request or a feature currently being implemented. A developer should be able to revisit a mature repository and ask: **What are we overlooking?**

> **Status: design only.** This repository currently contains project documentation and a license, not an implemented skill, executable scanner, benchmark, or verified audit result. There is no installation command yet.

[Design](DESIGN.md) · [Implementation plan](IMPLEMENTATION.md)

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

The first useful version will be **one portable agent skill**, `gapline-audit`, for a coding agent that already has authorized access to the repository. It will not launch its own model or require another service.

### 1. Scout — discover hypotheses

The agent maps relevant code, tests, docs, and interfaces; chooses a bounded scope; and identifies a few high-value questions. Recent changes, critical behavior, complexity, and documentation promises can guide attention, but are not proof of defects.

### 2. Probe — distinguish suspicion from evidence

The agent first investigates by reading code, tracing paths, and comparing documented claims with implementations and tests.

A later, separately qualified mode may run selected tests, make controlled inputs, or use existing mutation and analysis tools. **Execution must be authorized and appropriately isolated.** A skill prompt, copied directory, or git worktree is not itself a sandbox. The initial skill will be read-only.

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

Once the skill exists and its invocation is verified, the user should be able to ask an agent:

> Use Gapline to investigate this repository. Start read-only. Find up to five consequential weaknesses in behavior, tests, documentation, or reliability. Separate demonstrated problems from hypotheses, and recommend the smallest useful next action.

Or, on a later run:

> Revisit the previous Gapline findings. Check which are still supported, what has actually been fixed, and what new weaknesses deserve investigation.

The skill will support a repository-wide **survey**, a narrow **focus** on a component or concern, and eventually a **revisit** with prior findings. A survey is necessarily sampled and must disclose what was not assessed.

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

1. **Read-only skill:** a small, discoverable `gapline-audit/SKILL.md` with bounded exploration, investigation playbooks, and evidence-aware reports.
2. **Controlled probes:** optional executable checks only after host isolation, permissions, and evidence handling are qualified.
3. **Finding continuity:** opt-in, human-reviewable history to reduce repetitive findings and verify fixes.
4. **Real-world evaluation:** compare useful discoveries, false alarms, and end-to-end cost with an ordinary coding-agent review.
5. **Conditional automation or CLI:** only if measured needs justify the additional complexity.

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for explicit milestones and stopping criteria. The first task is the **read-only skill**, not a general scanning platform.

## License

Apache-2.0. See [LICENSE](LICENSE).
