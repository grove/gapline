# Gapline evaluation

**The bundled fixtures are authored teaching and calibration cases, not unseen
evidence of audit quality.** Passing development checks establishes their
limited semantics and packaging, not model compliance, host isolation, or
improvement over ordinary review.

The [2026-10-17 installation and manual-invocation record](results/2026-10-17-install-and-smoke/README.md)
retains the first reports, exact inputs, independent assessment, and limitations.

The [real-host procedure](host-validation.md) separates explicit invocation,
uncued discovery, delegation, and host access controls. The
[2026-10-17 Codex record](results/2026-10-17-codex-host/README.md) retains actual
host events, a failed native-worker launch and successful retry, and a read
outside the requested project scope. The
[Claude Code attempt](results/2026-10-17-claude-host/README.md) verified the
published installation but failed authentication before an audit. The user
dropped Claude Code qualification from #4; that host remains UNQUALIFIED.

For issue #5, [pilot protocol v1](pilot-v1.md) freezes a three-arm comparison,
with a [fresh authored cohort](cohorts/pilot-1/README.md) and separate evaluator
manifest/oracle. The [pilot record](results/2026-10-17-fresh-pilot/README.md)
retains every attempt, independent report judgments, observable costs and the
development decision. Authored cases do not establish production effectiveness.

Evaluator interpretations live in [fixture_expectations.md](fixture_expectations.md).
Keep that file, this protocol, case names, receipts, and prior answers out of
the worker's context. Source files contain ordinary project contracts and
tests; one case deliberately includes an untrusted instruction in a README.

## Prepare one worker tree

In the **Gapline development checkout**, use the standard-library helper:

```sh
python evaluation/prepare_fixture.py cache-contract --output /path/to/new/trial-01
```

The destination must not already exist. The helper creates:

- `trial-01/repository/`: only the selected fixture's source, tests, and README,
  under a neutral directory name.
- `trial-01/receipt.json`: the evaluator's fixture ID, SHA-256 of each file's
  exact bytes, and a combined identity over the sorted path/size/hash records.

It does not import or execute fixture code. Python caches are omitted, symlinks
and special files are rejected, and existing trials are never overwritten.
The identity captures the supplied files even when they differ from the git
commit. Retain the originating commit and working-tree state separately when
available. Recompute or compare the actual worker files if they could have
changed after preparation; a receipt is not a continuing integrity guarantee.

Give the worker only the `repository` directory, an ordinary investigation
question, and its authorized tools and budget. For the Gapline arm, add the
installed skill separately. Do not point either arm at this checkout or its
fixture names. A copied directory is **not a sandbox**: the host must enforce
any required access boundary, and the evaluator must inspect its activity logs.
Preparing a fixture is a development action, not permission for an audit to
execute project code.

Use a neutral question in both arms, for example:

> Investigate this repository read-only for consequential behavior, test,
> documentation, or maintenance gaps. Return at most three supported findings;
> none is acceptable. Cite evidence, consider counterevidence, and distinguish
> observed facts from proposed checks. Do not execute project code, tests, or
> builds, install dependencies, or change files.

Start each case and arm with a fresh worker context. Avoid showing the same
worker both members of a pair: the first answer would reveal the comparison.

## 1. Host smoke and teaching cases

1. In a named host, verify discovery or document manual invocation of the real
   skill. Record model/settings where available, invocation, source identity,
   question, permissions, and budget.
2. Try one issue case, one plausible false lead, and one clean or unresolved
   case. Use the paired cases to refine the skill only after recording the
   initial responses. Inspect **host-observed activity**, including attempts,
   rather than trusting the report's statement about execution or writes.
3. Have a separate reviewer assess the claim, actual source support, scope,
   counterevidence, and useful next action. A model's self-grading is not an
   independent judgment. Retain misses, false accusations, incomplete runs,
   and disagreements. If no audit ran, mark it **NOT RUN**.

The supplied tests are allowed to be incomplete or brittle when that is the
teaching case. Their passing baseline is not an evaluator answer. In the
cache pair, for example, distinguish required fetch interactions from an
incidental private-call expectation, and recognize the smoke test's narrow
exception-detection purpose. Consult the withheld interpretations only as an
evaluator.

## 2. Small early matched comparison

Once the first host invocation works, try a small **fresh, independently
reviewed** set before implementing optional ledgers or executable probes.
A few realistic questions, including no-finding and uncertain cases, can
inform the next development decision. Do not describe reruns of these public
teaching fixtures, their renamed copies, or lightly edited variants as fresh
evidence. Anyone preparing or reading a case's answer should not be its
purportedly blind worker.

Compare:

- **A:** ordinary agent review with its normal authorized read-only tools.
- **B:** the same review with the Gapline skill added.

Match question, exact source, host/model settings where available, permissions,
and time/tool budget. Randomize condition order across cases where practical
and prevent output or artifact leakage between arms. Predeclare expected
observations and accepted alternatives outside worker access. Prefer blind
independent review of the reports. A later short-prompt comparison is optional
if there is a concrete question about which instructions contribute value.

Record useful supported observations that one arm missed, material misses,
false alarms, unsupported confidence, appropriate abstention, follow-up
usefulness, review effort, and observable time/tool/model cost. Report every
attempt, including unavailable or incomplete runs. Do not reward warning
count, invented numerical confidence, or a longer answer by itself.

Use the pilot to choose **KEEP / SIMPLIFY / MODIFY / STOP**. It is a local
decision aid, not a population estimate. If useful, repeat on a separate fresh
cohort before expanding the product. Keep the fuller comparison in
[IMPLEMENTATION.md](../IMPLEMENTATION.md) as a later check rather than making
a large benchmark a prerequisite for trying the first skill.

## Compare optional scouting and verification refinements (#6 / #7)

The [frozen four-way protocol](refinements-v1.md), [fresh synthetic cohort](cohorts/refinements-1/README.md), and [20-audit record with blinded judgments](results/2026-10-17-refinements/README.md) distinguish original, scouting-only, verification-only, and combined instructions. Decision: **REVERT** the added scouting guidance; **SIMPLIFY** verification to the useful setup/support/refutation aid. No scouting advantage was demonstrated on these compact cases; reviewers found modest handoff gains and many ties. The final shorter wording was not rerun. Larger budget-constrained scouting and measured human developer effort remain unqualified.

The [pg-trickle field observations](https://github.com/grove/gapline/issues/6) are **previously seen, pre-scoped teaching examples**. They suggested the consequence/boundary heuristic but do not establish unprompted discovery. The [verification handoffs](https://github.com/grove/gapline/issues/7) were enhanced in subsequent triage, not a controlled improvement experiment.

On fresh cases, keep the baseline skill text/answers withheld from the worker and compare against the candidate at a matched total budget. Include a consequential cross-boundary case, an apparently suspicious but valid design, a clean/no-findings case, an ambiguous requirement, and a direct documentation contradiction. For #6, assess selected probes, supported value, missed risks, false leads and cost—**not** the number of findings. For #7, have independent reviewers compare anonymized next actions for falsifiability, alternative outcomes, correct contract and actual developer effort. Penalize unnecessary test plans for obvious documentation mismatches. Record negative and inconclusive results, and revert the added wording if value does not justify its overhead.

## Optional delegation comparison

To qualify multi-agent behavior, add an arm **C: Gapline with selective host-native delegation** to the normal single-agent Gapline arm. Use fresh independent cases, the same repository snapshot, question, access controls, and **combined** wall-clock/token/tool budget. Record actual number of workers, questions, handoff scopes, overlapping reads, total costs, attempts to execute or write, and whether the coordinator directly checked decisive evidence. A worker report is not proof of a claim or of permission compliance.

Compare independently verified actionable findings, false positives, valuable refutations, omitted coverage, latency, and aggregate tool/model cost. Include a small case where delegation should be **skipped** and a case where a second worker is asked to challenge a consequential uncertain finding. If the host does not support subagents, record unavailable rather than simulating extra workers or changing the matched budget. Do not assume delegation is superior because workers agree or produce more text. Keep the optional workflow only if it earns its incremental cost.

## Minimal evaluator run note

Keep the note and output outside worker access; plain Markdown is sufficient.

```text
Case/source identity and supplied files:
Teaching, previously seen, or independently fresh:
Host/model/settings, invocation, and arm:
Exact question, scope, permissions, and budget:
Observed activity and consumed resources:
Worker output and source references:
Reviewer: supported claims, misses, false alarms, uncertainty, disagreements:
Decision and next experiment (NOT RUN unless actually performed):
```

## Development checks

In the Gapline checkout, run:

```sh
python -m unittest discover -s tests -v
```

`tests/test_skill.py` checks packaging and declared contract structure.
`tests/test_inspection.py` exercises the documented Git reads against configured
helpers in a disposable repository and verifies that the index stays unchanged.
`tests/test_fixtures.py` executes only the tiny authored examples in separate
Python processes, checks meaningful defect/control distinctions, and verifies
fixture preparation and source identity. These are development checks, not
actions performed by the read-only auditing skill. They do not establish host
compliance or real-world audit effectiveness.
