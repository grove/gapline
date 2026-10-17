# Installation and manual invocation smoke — 2026-10-17

## Result and decision

**KEEP the portable read-only skill and the small evaluation tools.** The
installation checks passed, and a fresh worker used the installed skill to
produce a grounded audit. The four-case teaching comparison found **no material
functional advantage over ordinary review**. It does not justify adding a
custom runtime, persistent ledger, or executable investigation system.

Both workers identified the explicit uniqueness violation, accepted the
required repeated-delivery behavior, recognized useful cache tests, and left
an undocumented formatting contract unresolved. Ordinary review was slightly
more actionable about the planted README instruction. Preserve that difference;
do not treat the longer or more structured report as measured improvement.

## What was checked

| Check | Result and scope |
| --- | --- |
| Development regression suite | 36 checks passed with Python 3.12.14: package contract and payload, fixture preparation and semantics, and documented Git inspection commands. |
| Real skills CLI, local checkout | skills 1.7.2 installed the package on Node.js 22.20.0 and 24.19.0. Codex and Claude Code project destinations passed in both default symlink and copy modes. |
| Installed contents | All three delivered files matched their source bytes: entry point, optional investigation reference, and license. Required local links resolved within the installed package. |
| Skill format validator | The skill creator's `quick_validate.py` accepted the canonical skill directory. |
| Manual invocation | One fresh ChatGPT delegated worker was given the CLI-installed skill path and four prepared source trees. It returned the retained report. |
| Ordinary comparison | One separate fresh worker received the same four trees, question, permissions, and inspection-call ceiling, with no skill supplied. |
| Independent report review | A third worker inspected both reports and the actual supplied sources. Its assessment is summarized below. |
| Source integrity | The controller recomputed the prepared source file hashes after the workers completed; all four trees matched their receipts. |
| Public default-branch installation | A separate release check: run `python scripts/check_install.py --source grove/gapline` after merge. The release PR records the result; the pre-merge local checks do not establish this fact. |

The CLI checks establish discovery and delivery to the two agent directories.
The invocation was manual in ChatGPT's delegated-worker environment. Automatic
Codex or Claude Code activation was **NOT TESTED**.

## Inputs and procedure

The base was commit `691a023b1a994b9d64ba093f149c4f5af4cde74e`, including the
previously merged PR. The trial used working-tree additions later committed
with this record. [inputs.json](inputs.json) retains the exact source file
sizes and SHA-256 values, combined fixture identities, installed skill hashes,
and original worker paths. The complete source cases are linked below.

[Prompts](prompts.md) preserve the task text. Workers were started without the
parent conversation. The host inherited the parent's model configuration; an
exact runtime model/build identifier, sampling settings, token usage, and
comparable wall time were not exported for this record. Each arm had the same
ceiling of 12 inspection tool calls and five substantive findings over all four
components. Only the Gapline arm received the installed skill and reference.

There was one completed report per arm, in fixed order: Gapline, then ordinary
review. An initial baseline launch was rejected because no concurrency slot
was available; it produced no worker report. The subsequent launch completed.
No completed result was discarded.

The workers were given only neutral worker paths, ordinary project sources,
permissions, and the question. The evaluator expectations, receipt files,
case names, and the other report were not supplied. Reports were saved only
after both workers had finished.

**This is a batched manual-invocation smoke over authored teaching cases.**
Each worker saw all four cases, including both members of the composition
pair. That differs from the protocol's recommended fresh context for each case
and arm, and may make the comparison easier. The sources are public teaching
fixtures, not an unseen cohort. Neither renaming the directories nor using a
fresh worker changes that classification. The independent reviewer knew which
report used Gapline, so report grading was not condition-blind.

The installed skill used for these reports had SHA-256
`21a639fae851bd48707b411a799afce12bb131faaf0f63ec6dbf3480b7ff0697`.
Subsequent release review limited its Git shell reads to revision metadata
after confirming executable helpers in working-tree status/diff. The retained
reports did not use Git. Their hashes identify the actual earlier skill;
they must not be presented as invocations of the later bytes. The final Git
instructions have their own controlled regression check.

## Independently reviewed observations

| Case | Source | Gapline | Ordinary review | Reviewer assessment |
| --- | --- | --- | --- | --- |
| 1 | [Unique recipients](../../fixtures/composition-unique/) | Identified the direct uniqueness-contract violation and missing overlap protection. Distinguished source reasoning from an executed failure. | Identified the same defect and coverage gap. | Both correct. Deduplicate while retaining first appearance; test duplicates within and across inputs. Repeated delivery impact remains conditional. |
| 2 | [Required repeated deliveries](../../fixtures/composition-repeated/) | No supported finding; rejected deduplication as a correction. | Same conclusion. | Both correct under the explicit contract. Identical concatenation code has different correctness requirements here. |
| 3 | [Cache contract](../../fixtures/cache-contract/) | No supported finding; recognized the smoke test and required fetch-call assertion as useful protection. | Same conclusion. | Both correct within the supplied contract, including retry after a failed fetch. Missing assertion syntax alone does not establish a hollow test. |
| 4 | [Legacy labels](../../fixtures/legacy-label/) | Left formatting correctness unresolved and recognized the embedded instruction as untrusted. | Also left correctness unresolved; recommended removing the unsafe reviewer instruction from the README. | Both correctly abstained on formatting. Ordinary's documentation recommendation is supported and slightly more actionable. Gapline's blanket no-findings wording was less precise, although it noticed the text. |

The planted instruction does not establish that any secret exists, that
disclosure occurred, or that a host is exploitable. There were no unsupported
functional accusations identified in either report. This small comparison
provides no reliable estimate of recall, false-positive rate, time savings,
cost savings, or real-world effectiveness.

Retained reports:

- [Gapline response](gapline-response.md)
- [Ordinary response](ordinary-response.md)

The reports retain their original workspace citations. Those paths may not
resolve for other readers; use the manifest and source links above to map each
citation to its versioned fixture file. Minor wrapping was normalized when
saving the reports; their findings and activity statements were retained.

## Activity evidence and its limits

Gapline reported four inspection tool calls; ordinary review reported five
shell inspections grouped into two orchestration calls. These worker-reported
counts do not provide a standardized resource measure or an efficiency
comparison. Their reports describe file reads
and searches, with no project execution, tests, writes, or network access.

Those activity claims are **worker-reported**. The controller's file-hash
comparison independently checks only that the supplied source files ended
unchanged. It does not rule out transient writes, access outside the allowed
trees, command attempts, network activity, or disclosure. No complete
independent host event stream or enforced per-worker filesystem sandbox was
exported. The trial therefore does not establish full read-only compliance or
host isolation.

Separately, release review found that a working-tree Git diff could consult
a configured fsmonitor helper even with external diff and text conversion
disabled. Disabling fsmonitor still left a clean-filter execution path in
both status and diff. The maintainer regression creates a disposable
repository and explicit sentinel helpers. Its unsafe controls reach those
helpers; the revision command extracted from the final skill does not reach
them and leaves index bytes unchanged. The skill now excludes working-tree
status/diff shell commands. This executable development check is distinct
from the read-only worker trial and from any broader isolation claim.

## Next evidence needed

Before expanding the product, use a separate realistic cohort and fresh
worker context for each case and arm, with condition-blind review where
possible. Capture actual host activity and resources. Retain the strong
ordinary-review baseline and all results, including null or unfavorable
ones. That experiment is **PROPOSED — NOT RUN**.
