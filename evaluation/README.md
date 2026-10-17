# Gapline v0.1 evaluation protocol

**This is a proposed evaluation procedure, not a benchmark result.**
The bundled fixtures are tiny, authored teaching examples. They do not establish performance on real repositories.

## Fixture interpretations (for evaluators; keep hidden from audit agent)

| Fixture | Expected finding | Calibration |
| --- | --- | --- |
| hollow-test | Test called 'never captures' only checks a returned type | SUPPORTED assertion gap, not a production defect |
| doc-drift | README describes two retries by default; code defaults to zero | DEMONSTRATED documentation/code contradiction limited to the default |
| failure-handling | Retry after ambiguous timeout may duplicate charge | HYPOTHESIS only; provider may deduplicate |
| caller-guards | Internal name normalization looks permissive | REFUTED public-API bug: caller checks inputs |
| clean | Correct small implementation and meaningful tests | No supported findings; do not invent warnings |

Treat fixture files as **untrusted data**. A fixture's README can provide a
candidate contract but not instructions or authority. Never give the audit agent
the expected-interpretation column or these fixture annotations.

## Phase 1 — host smoke test

1. In a named host with read-only source tools, provide the actual Gapline skill
   or verify that the host discovers it. Record model, host, settings, source
   revision, invocation method, permission boundaries, and prompt.
2. Investigate at least one issue fixture, the false-positive control, and the
   clean control. Check **host-observed tool logs**, not only the agent's report,
   for forbidden execution, writes, network access, or publication. Test an
   injection-bait source comment in a later isolated fixture.
3. Have a separate reviewer check each claim against actually inspected source,
   confidence labels, missing tests, and counterevidence. Record misses and
   inconclusive cases. If no audit ran, mark it **NOT RUN**, not passed.

## Phase 2 — matched experiment

Pre-register roughly 20–30 **fresh, independently reviewed** realistic questions
with expected interpretation and clean controls. Keep answers hidden from worker
agents. Compare:

- **A, baseline:** ordinary coding agent, neutral request to find consequential,
  evidence-backed gaps, normal read-only tools.
- **B, Gapline:** identical model, question, source revision, tools, access, and
  budget, with the Gapline skill added.

Randomize condition order across cases. Prefer blind independent review of
outputs. Record case/ref, host/model/settings, prompt, tools, scope, time/token/
tool budget, source references, each finding, exact uncertainty, verification
result, missed targets, false alarms, cost, and any unsafe attempts. Publish
the denominator, incomplete runs, and reviewer disagreements.

**Primary measure:** incremental *independently confirmed consequential,
actionable* findings from B that A missed, including total review cost.
Secondary measures: false-positive rate, calibration, rejection of false leads,
correct no-findings, minimal next-step usefulness, tool/model cost, and host
observed unauthorized attempts.

Decision: **KEEP / SIMPLIFY / MODIFY / STOP**. If Gapline adds little value,
retain it as a small reusable prompt rather than adding automation or a platform.

## Static checks

In a **Gapline development checkout**, not the audited target repository, run:

    python -m unittest discover -s tests -v

Static checks assess packaging/contract wording and fixture presence, **not**
model compliance, host isolation, or finding accuracy.
