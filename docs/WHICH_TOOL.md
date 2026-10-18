# Which tool should I use?

**Start with your question—not a complicated workflow.** The Grove projects are separate, optional tools for different stages of working on software. You don't need to install or run all of them.

## The quick answer

| Your question | Choose | What you'll get |
| --- | --- | --- |
| **“What exactly should this feature do?”** | [Intentline](https://github.com/grove/intentline) | A proposed checklist of expected behavior, with unclear decisions called out |
| **“What important problems might this code have?”** | [Gapline](https://github.com/grove/gapline) | A read-only investigation of code, tests and documentation, with evidence and next steps |
| **“Did my selected checks pass on this change?”** | [Proofline](https://github.com/grove/proofline) | Actual results from the tests/commands you selected, if its supported execution setup is available |
| **“Would my tests detect deliberate mistakes?”** | [Faultline](https://github.com/grove/faultline) | **Not available yet.** It's a design proposal for checking test strength through controlled experiments |

**Important:** Faultline currently has **no installable skill**. Proofline is implemented, but needs a separate runtime checkout and a supported macOS/Codex sandbox setup to execute checks. Installing its agent skill alone is **not** enough. Check [Proofline's setup instructions](https://github.com/grove/proofline#use-with-codex-or-claude-code) before choosing it.

## A simple way to think about them

```text
Before building:   "What does done mean?"          → Intentline
Looking at code:   "What might be missing or wrong?" → Gapline
Checking a change: "Did these chosen tests pass?"    → Proofline
Testing the tests: "Would tests catch wrong code?"   → Faultline (planned only)
```

For example, say you want usernames made up only of spaces to be rejected:

- **Intentline:** Clarify that promised outcome and suggest how to check it. It doesn't write the feature.
- **Gapline:** Inspect existing validation code and tests for a source-supported weakness. It doesn't run those tests.
- **Proofline:** After someone implements the change, run **explicitly selected** checks on a protected copy, when its qualified setup is available. Passing checks don't prove the whole feature is complete.
- **Faultline:** A future project for asking whether tests would catch plausible wrong implementations. **You cannot run it today.** For now, you can ask Gapline to inspect the relevant assertions read-only.

These are **choices**, not required steps. You can use one without the others.

## How to get started

| Tool | How to begin |
| --- | --- |
| **Intentline** | Install skills with `npx skills@latest add grove/intentline`, then ask your coding assistant to **“Use intentline-plan to suggest an unsaved acceptance checklist for this request…”** |
| **Gapline** | Install `npx skills@latest add grove/gapline`, then ask **“Use gapline-audit to investigate this project read-only…”** |
| **Proofline** | See [its installation and supported-host instructions](https://github.com/grove/proofline#get-started); the installable skill is named `proofline-check`, and running checks needs the separate CLI and supported environment |
| **Faultline** | **No install command.** Only the design is published; follow [its repository](https://github.com/grove/faultline) for any future implementation |

The `npx skills` commands install **instructions for your coding assistant**, not a new AI service or a guarantee of access to GitHub, private files, or test-running facilities.

## Two things people often confuse

**Intentline's `intentline-audit` vs Gapline's `gapline-audit`:** Intentline reviews a **saved requirements/acceptance draft** against its original sources. Gapline looks for **weaknesses in actual code, tests, and documentation**. They are not interchangeable.

**An investigation vs a test result:** Gapline can propose a check but **cannot execute it**. Proofline can execute chosen checks in its supported protected environment, but a pass only tells you those checks passed—not that every request was fulfilled.

If you want to create or update a GitHub issue, use **`intentline-issue`**, and explicitly ask for the particular issue/repository and write operation. Gapline and Proofline do not automatically publish findings.

## Want to see a whole example?

- **[Intentline: first feature plan](https://github.com/grove/intentline/blob/main/docs/FIRST_USE.md)** — original request, chat prompt, example response, next action.
- **[Gapline: first code audit](https://github.com/grove/gapline/blob/main/docs/FIRST_USE.md)** — a small real teaching fixture, chat prompt, source-grounded example result, next action.

You can start with just a single skill and one sentence to your coding assistant. No universal pipeline, quality score, or automatic approval is involved.

*Project status checked in October 2026; consult the linked repositories for later changes.*
