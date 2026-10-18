# Your first Gapline audit: a complete example

**Try this once, then use the same approach on your own project.** You only need a coding assistant that can read a repository and the installed `gapline-audit` skill.

This walkthrough uses a **real, checked-in teaching example** in the Gapline repository. The example contains a deliberately incomplete validation path; it is **not a claim about a production application**. The example response below is **written for this guide**, not captured from an actual agent run. Your agent's wording and findings may differ.

```text
The requested behavior → Your prompt → The assistant's report → Your decision
```

## 1. The original request

Imagine a small reservation system accepting quantities from both a website and partner systems.

Its [written requirement](../evaluation/fixtures/boundary-gap/README.md) says:

> Both entry points must reject quantities that are not integers from 1 through 100, inclusive. Booleans are not quantities.

It also says partners can submit messages **without passing through the website entry point**. This matters because checking the website alone isn't enough.

The little example project contains the [implementation](../evaluation/fixtures/boundary-gap/orders.py) and [tests](../evaluation/fixtures/boundary-gap/test_orders.py). You can follow the links and inspect them yourself—no code execution is necessary.

## 2. Install Gapline

If you haven't installed the skill, open a terminal in the project directory where you'll use your coding assistant and run:

```sh
npx skills@latest add grove/gapline
```

Choose your coding assistant when prompted. To try this **exact teaching example**, open the [Gapline repository](https://github.com/grove/gapline) in an assistant that can read its files. To use Gapline on **your own** project instead, open that project and change the target paths in the prompt.

## 3. Paste this into your coding assistant

This is a **chat message to the assistant**, not a terminal command.

```text
Use gapline-audit to review the teaching example in
evaluation/fixtures/boundary-gap, read-only.

Start with its README.md to understand the intended behavior.
Inspect orders.py and test_orders.py. Check whether both
public entry points reject invalid quantities, including
messages sent directly by a partner.

Give me the most important supported finding(s), or say
if there are none. For each finding, show the exact files,
what supports it, what might disprove it, and one useful
next action. Tell me what you didn't assess.

Do not change files or run any code, tests, or builds.
```

In Codex, you can also start with `$gapline-audit`. In other assistants, explicitly naming the installed skill is the straightforward option.

## 4. Here's an example of what the assistant might say

**Illustrative response — not an actual Gapline run**

> **Scope:** Reservation intake teaching example. I read its requirement, `orders.py`, and `test_orders.py`. I did not run code or tests.
>
> **Finding: Partner requests appear to bypass quantity validation.** The requirement says both entry points must reject invalid values. `submit` checks the type and range, but `consume` reads `message["quantity"]` and returns it without a corresponding check. Partner messages can go directly to `consume`.
>
> **Evidence:** [Requirement](../evaluation/fixtures/boundary-gap/README.md), [implementation](../evaluation/fixtures/boundary-gap/orders.py), and [selected tests](../evaluation/fixtures/boundary-gap/test_orders.py). The tests check rejected inputs at `submit`, but the inspected partner test passes a valid quantity to `consume`.
>
> **Confidence:** **DEMONSTRATED (source-level mismatch)** for the inspected path; no runtime behavior was reproduced.
>
> **Counterevidence considered:** Website messages go through the guarded `submit` function. That doesn't protect independently supplied partner messages.
>
> **Next step — PROPOSED, NOT RUN:** Check the intended behavior by sending `consume({"quantity": 0})` through the independent partner path and expecting rejection. Then consider validating that entry point and adding the relevant test.
>
> **Not assessed:** Other producers, external constraints, and real deployment behavior.

The point isn't a particular wording or number of findings. It is that the answer names a **specific promise, specific source evidence, limits, and a next step** instead of claiming the whole project is broken.

## 5. What you should do next

1. **Look at the evidence.** Open the cited requirement and source files. Does the observation match the intended behavior?
2. **Decide what needs checking.** The suggested example input is just a proposal. A separate, explicitly authorized coding/testing task can test it or implement a fix; the Gapline audit will not.
3. **If you want a GitHub issue, ask separately.** [Intentline's issue skill](https://github.com/grove/intentline) can help draft one from a finding and, with explicit permission, publish it.

If your own first audit reports **no supported findings**, that's allowed: it means nothing important was substantiated in the sampled scope, not that your code is guaranteed correct.

**Next:** Try the [copy-and-paste prompt cookbook](AGENT_PROMPTS.md) for a specific component, PR, or parent issue, or visit [Which tool should I use?](WHICH_TOOL.md) to compare Intentline, Gapline, Proofline, and Faultline.
