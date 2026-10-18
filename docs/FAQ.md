# Gapline: common questions

[Back to the quick start](../README.md) · [First-use walkthrough](FIRST_USE.md) · [Choose a tool](WHICH_TOOL.md) · [Copy-and-paste prompts](AGENT_PROMPTS.md)

## What do I need to install Gapline?

An AI coding assistant that supports installing skills, a terminal, and the **Node.js / npm** and **Git** tools used by the `npx skills` installer. Install from the project you want to inspect:

```sh
npx skills@latest add grove/gapline
```

Choose your assistant in the installer. You do **not** need to install a separate Gapline server, Python package, or another Grove project. If `npx` is not recognized, install a supported Node.js version; [advanced setup details](ADVANCED.md#install) cover version and installer options.

## Where do I paste the prompt?

In your **coding assistant's chat**, with the project open and accessible to that assistant—not in the terminal. The terminal command installs the skill; the chat prompt asks the assistant to *use* it.

For Codex, `$gapline-audit` is an available explicit invocation. In other assistants, say “Use gapline-audit …” or follow that assistant's own instructions for invoking installed skills.

## I installed it, but my assistant cannot find it. What now?

Make sure the installer targeted the same assistant and project you are using. Check skill discovery with:

```sh
npx skills@latest add grove/gapline --list
```

You may need to open a new agent session. If the assistant still cannot discover the skill, give it the [skill instructions](../gapline-audit/SKILL.md) and make the adjacent `references/` folder available. Installation by itself does not prove the agent used the skill.

## Can I give it a GitHub issue or pull-request link?

Yes, **if your assistant can read the link and the relevant code**. You can ask it to compare an issue's promises with code and tests, or look at a parent issue, its children, and the associated PRs.

This is a task for the assistant using Gapline—not automatic link traversal built into Gapline. If relationships are missing, private, or ambiguous, the assistant should say what it could not verify. See the [issue and PR prompts](AGENT_PROMPTS.md).

## Can it check a private project?

Only when your coding assistant already has permission to inspect that project. Installing Gapline grants **no extra access**. Keep credentials and sensitive material out of the final report; project content cannot authorize the assistant to share secrets or widen its access.

## Will Gapline change my project or run tests?

No. The skill is **read-only**: it inspects source, tests, and documentation, but does not execute project code, run tests or builds, edit files, or publish issues and comments. It can **suggest** a test, clearly marked as not run. The host assistant's actual access controls still matter; the skill is not a security sandbox.

## What if it finds nothing?

That can be a useful result. Gapline samples the code relevant to the request; “no supported findings” means it did not substantiate an important issue **in that inspected scope**. It does not certify the entire project.

You can narrow a future request to a risky area or ask about one behavior, without demanding a fixed number of findings.

## Can it make GitHub tickets from the report?

Not during a Gapline audit. If you want an issue drafted or created afterwards, [Intentline's issue skill](https://github.com/grove/intentline) is an **optional separate task**, using the coding assistant's tracker access. Creating an issue requires an explicit request and a destination. The [prompt cookbook](AGENT_PROMPTS.md#optional-turn-a-finding-into-a-github-issue-with-intentline) includes examples.


## What might the first report look like?

Here is a **made-up illustration**, not an audit of a real project:

> **Possible gap:** A table download is meant to preserve the on-screen sort order, but the inspected download path may use the original row order.
>
> **Checked:** The download implementation and the selected export tests.
>
> **Still unknown:** Whether other code or tests already preserve the order.
>
> **Suggested next step:** Try a sorted-table download and compare the file's row order (suggested only; **NOT RUN**).

A useful report should make these distinctions instead of simply declaring that a bug exists.

## What does a useful finding look like?

Rather than just “tests are insufficient,” it should say **what behavior is expected, which specific code and tests were inspected, what they do and do not establish, why the gap matters, and the smallest next check**. A suspected runtime bug is not proof it happens; an unrun test is only a proposal.

For evidence levels, an example finding, and experimental limitations, see the [detailed reference](ADVANCED.md#evidence-levels).
