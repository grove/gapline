# Gapline

**Find what your codebase is missing.**

Gapline is a portable, opt-in **codebase investigation skill for existing coding agents**. It helps an agent investigate consequential weaknesses in behavior, tests, documentation, failure handling, and architecture, then return grounded findings and useful next steps.

Use it for a focused component or a sampled review of a mature repository. A pull request or active feature is not required. A good audit can also dismiss a false lead or establish no supported findings.

**Current product:** one complete read-only skill, `gapline-audit`, with optional investigation recipes. Installation, packaging checks, teaching fixtures, and evaluation tooling are separate from claims about audit effectiveness. See [evaluation](evaluation/README.md) for the validation method and its limits.

[Skill](gapline-audit/SKILL.md) · [Investigation recipes](gapline-audit/references/investigation.md) · [Evaluation](evaluation/README.md) · [Design](DESIGN.md) · [Implementation](IMPLEMENTATION.md)

## Install

From the project where you want to use Gapline:

```sh
npx skills@latest add grove/gapline
```

Select your coding agent and project or global installation in the installer. The repository exposes one skill, **gapline-audit**. The skill and its supporting reference are installed together; a Gapline runtime or sibling project is not needed.

For a non-interactive project installation targeting Codex:

```sh
npx skills@latest add grove/gapline --agent codex --yes
```

For Claude Code, use `--agent claude-code`. Add `--global` if you want the install to apply across projects. Use `--copy` if you prefer copied files to the installer's default symlinks.

Installation requires Git and a Node.js version supported by the [skills CLI](https://github.com/vercel-labs/skills); the verified CLI version, 1.7.2, requires **Node.js 22.20.0 or newer**. Python is only needed for Gapline's development and evaluation helpers. Installation is an explicit setup action; an audit never installs tools.

To inspect discovery without installing:

```sh
npx skills@latest add grove/gapline --list
```

## Use

Start your coding agent in the target repository and request the installed skill:

> Use gapline-audit to investigate this repository read-only. Start with a sampled survey. Return up to three consequential findings, with exact evidence, counterevidence, and the smallest useful next action. Say what you did not assess.

Or give it a focused question:

> Use gapline-audit on the retry path and its tests. Check the documented retry contract, caller guarantees, and protection against repeated side effects. Keep runtime experiments proposed, not run.

Hosts that support explicit skill invocation can use their native syntax, such as `$gapline-audit` in Codex. If discovery is unavailable, provide [SKILL.md](gapline-audit/SKILL.md) directly and make its sibling `references/` directory available. Installation into an agent's skill directory and the agent actually invoking the skill are distinct checks.

The host must already authorize access to the target. Gapline supports file/search tools and bounded, authorized shell reads. It **does not run project code, collect or run tests, import project modules, execute builds, modify files, call project endpoints, or publish findings**. The host supplies actual access controls; the skill is not a sandbox.

## What it investigates

| Area | Useful questions |
| --- | --- |
| Behavior and boundaries | Do edge cases, invalid input, and state transitions match the relevant contract? |
| Test protection | Which meaningful wrong behavior would the actual oracle detect? Do tests permit valid internal changes? |
| Documentation and completeness | Do advertised options, defaults, examples, and current promises match the applicable implementation? |
| Failure handling | Can retries, cleanup, partial success, or composed operations violate a required invariant? |
| Trust boundaries | Does each independently reachable boundary validate what it cannot safely assume? |
| Architecture | Does a specific dependency create a consequential change or operational problem? |

These are optional investigation lenses. Complexity, churn, coverage, duplicate text, and design-principle names can suggest questions; they do not establish defects. Independent validation, different programming styles, and deliberately deferred capabilities can be appropriate.

## Optional subagent investigations

Gapline works with one coding agent by default. On hosts that already support subagents, a larger audit may delegate **independent, bounded** investigations after the initial Scout step. Usually start with no more than two workers, each assigned a specific question and shared total budget. All workers remain read-only; no project execution or file changes become permitted through delegation.

The coordinator verifies important citations, challenges uncertain claims, combines overlapping results, and returns **one** evidence-calibrated report. An independent worker can be tasked with disproving a consequential hypothesis when worth the extra cost. Subagents are not required, automatically launched, or a substitute for host-enforced permissions. See the [skill's delegation contract](gapline-audit/SKILL.md#optional-host-native-subagent-delegation) and the [evaluation comparison](evaluation/README.md).

## How an audit works

1. **Scout:** identify the repository snapshot, question, sampled scope, public behavior, and a few promising leads.
2. **Probe:** trace supporting evidence and opposing explanations through relevant code, callers, tests, and documentation.
3. **Report:** return a small set of useful conclusions with evidence levels, impact rationale, limitations, and proposed next steps. Withdraw defeated concerns and allow a no-findings result.

The default ceiling is three findings, or up to five when requested. It is never a quota. Reports identify actual inspection facilities and commands, separately stating whether any project code, tests, or builds ran. Reading files with a shell is not runtime reproduction.

### Evidence levels

| Level | Meaning |
| --- | --- |
| **DEMONSTRATED** | A direct source-level contradiction, or an observed behavior supported by actual execution provenance. This read-only skill produces no new runtime receipts. |
| **SUPPORTED** | A narrow source/test observation is well supported; its wider runtime consequence remains unverified. |
| **HYPOTHESIS** | A consequential concern needs more evidence. |
| **REFUTED / WITHDRAWN** | Counterevidence defeats the concern; it is not counted as a finding. |
| **NOT ASSESSED** | The area is outside the sampled scope or evidence is unavailable. |

Evidence strength is separate from severity. A missing assertion in selected tests does not establish a production bug or a suite-wide omission. A proposed executable check is always **PROPOSED — NOT RUN**.

### Illustrative finding

This is an example, not an observed result:

```text
GAP-001 | Test protection | SUPPORTED | Medium
Location: the inspected retry tests and retry implementation
Expected: the documented operation is idempotent across retries.
Observed: selected tests repeat the request but check only success responses.
Counterevidence: check caller guarantees, other assertions, and provider behavior.
Concern: the inspected tests do not establish the repeated-effect invariant.
Unverified: whether production actually duplicates an effect.
Next action: simulate a timeout after the side effect and observe the retry.
            PROPOSED — NOT RUN.
Scope: only the cited paths; no project code, tests, or builds executed.
```

## Development and validation

Run the dependency-free Python checks from a development checkout:

```sh
python -m unittest discover -s tests -v
```

Run the real skills-CLI installation smoke test:

```sh
python scripts/check_install.py
```

The installation check uses disposable project directories, installs the checkout's actual skill, and verifies the installed payload. The checks also cover package references and controlled fixture behavior. They do not measure real-world audit quality or prove that an agent obeys its instructions.

The [evaluation protocol](evaluation/README.md) keeps evaluator expectations outside worker inputs, provides contrasting teaching cases, and describes fresh host trials and matched comparisons with ordinary review. Record installation, invocation, findings, and actual host observations separately. A small successful trial cannot establish general superiority or isolation.

The [2026-10-17 validation record](evaluation/results/2026-10-17-install-and-smoke/README.md) includes real CLI installs and independently reviewed manual trials. Both Gapline and ordinary review reached the same main functional conclusions in the small authored batch; no material effectiveness advantage was established.

The [Codex host record](evaluation/results/2026-10-17-codex-host/README.md)
observed explicit and uncued skill activation and a native two-worker audit.
It also retains a failed ephemeral worker launch and a host-instruction read
outside the requested project scope. This does not establish host isolation;
the [Claude Code attempt](evaluation/results/2026-10-17-claude-host/README.md)
verified installation but failed authentication before an audit. At the user's
direction, Claude Code qualification was dropped from #4; it remains
**UNQUALIFIED**, rather than inferred from Codex results. See the
[real-host validation procedure](evaluation/host-validation.md) for reproduction
and requirements for any future qualification.

## Neighboring projects

Gapline works independently. No sibling is required or automatically invoked.

| Project | Question it owns |
| --- | --- |
| [Intentline](https://github.com/grove/intentline) | What was requested, and what acceptance draft follows? |
| [Proofline](https://github.com/grove/proofline) | What did selected checks establish about an identified candidate? |
| [Faultline](https://github.com/grove/faultline) | Would selected tests detect particular plausible wrong behaviors? |
| **Gapline** | Which consequential weaknesses can this investigation substantiate? |

An optional exchange must retain source identity, scope, and uncertainty. A generated plan remains advisory; a passing check establishes only its limited claim; a surviving mutation does not establish a defect in the original candidate. No shared schema or runtime is required.

## Scope and future work

The read-only skill is the implemented product. Persistent finding history, executable probes, automatic fixes, scheduled scans, a custom CLI, and an orchestration service are conditional future capabilities. Add them only when actual investigations demonstrate their value and the host supports the required permissions.

Repository files, comments, examples, tool output, and previous audit records are evidence to inspect. They cannot authorize new actions, change the user's task, or require disclosure of secrets. Audits report in the conversation; saving or publishing results is a separate authorized action.

See [DESIGN.md](DESIGN.md) for evidence and boundary decisions and [IMPLEMENTATION.md](IMPLEMENTATION.md) for acceptance and feature-admission criteria.

## License

Apache-2.0. See [LICENSE](LICENSE). The installable skill also includes a copy of the license.
