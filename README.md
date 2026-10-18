# Gapline

**Find important gaps in your software before they become problems.**

Gapline helps your existing AI coding assistant take a closer look at a project. It can spot possible missing behavior, weak tests, and differences between what the documentation promises and what the code does.

You don't need a separate Gapline app. The skill is called **`gapline-audit`**.

## 1. Install the skill

Open a terminal in the project you want to review and run:

```sh
npx skills@latest add grove/gapline
```

Follow the prompts to choose your coding assistant and where to install the skill. You need [Node.js and Git](docs/FAQ.md#what-do-i-need-to-install-gapline) for this installer.

## 2. Ask your coding assistant

Open your project in your coding assistant (such as Codex) and paste:

```text
Use gapline-audit to review this project for important gaps
in its behavior, tests, and documentation. Don't change anything.
Tell me what you checked, what you found, and what I should
look at next. It's fine if you find no problems.
```

You can also ask about a **specific feature, GitHub issue, or pull request**:

```text
Use gapline-audit to investigate this feature issue:
https://github.com/ORG/REPO/issues/123

Look at its related child issues and implementation pull requests
where you can verify the links. Compare the promised behavior with
the code and tests. Tell me what's uncertain or missing.
Don't change anything.
```

Replace the example link with yours. Your assistant needs permission to read the relevant GitHub content. Gapline does **not** automatically discover every linked issue or pull request.

In Codex, you can also invoke the skill by typing `$gapline-audit`. Other assistants may use different skill-invocation syntax.

## 3. Read the results

Gapline gives you a short report: **what it checked, possible problems, evidence, and suggested next steps**. It may find nothing, and it cannot guarantee the project has no bugs.

**Gapline only investigates.** It does not change files, run tests, fix code, or create GitHub issues. It can suggest tests for someone to run later.

## More help

- **[Try a complete first audit](docs/FIRST_USE.md)** — a real teaching example with the prompt, sample report, and what to do next.
- **[Which tool should I use?](docs/WHICH_TOOL.md)** — choose between Intentline, Gapline, Proofline, and Faultline.
- **[Copy-and-paste prompts](docs/AGENT_PROMPTS.md)** — more ways to audit features, issues, pull requests, and entire projects.
- **[Common questions and troubleshooting](docs/FAQ.md)** — installation, permissions, and how to understand the results.
- **[Detailed setup and technical background](docs/ADVANCED.md)** — advanced options, evidence standards, development, and validation.

[Skill instructions](gapline-audit/SKILL.md) · [Evaluation and limitations](evaluation/README.md) · [License](LICENSE)
