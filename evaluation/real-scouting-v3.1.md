# Prospective v3 prompt clarification and one replacement

The first v3 curator refused before any source inspection because the prompt
referred generically to qualified native patch APIs. It interpreted `apply_patch`
as unqualified. Controller receipts show all boundary checks passed: this was
a prompt ambiguity, not a host security or source-integrity failure. Retain
the attempt unchanged in `results/2026-10-17-real-scouting-v3/`.

Clarify the common constraints before any successful curator or audit: enumerate
the six already-qualified visible API names, explicitly say their presence must
not cause a stop, and continue forbidding native patch/resource use. Unknown
capabilities still fail closed. No host flags, qualification, source/variant
bytes, substantive question, budget or review criteria change. Do not rerun
host probes. All [v3 requirements](real-scouting-v3.md) otherwise remain.

The user explicitly approved one replacement after reviewing this correction
and its aggregate ceilings; v3 originally froze twelve attempts with no retries.
Run exactly two fresh curators, eight audits and two reviewers under new neutral
`-v3.1` work/output roots, without old curator interpretations. This is twelve
remaining sessions plus the retained 13.970-second, 24,298-token failed attempt:
at most **13 attempts / 12,024,298 cumulative tokens / 2,173.970 session seconds**.
No further retries are implied. Monetary charges remain unavailable.

Freeze corrected exact prompts, host/source identities and authorization before
replacement curators, then accepted independent expectations before audits.
The original failed attempt is never accepted retrospectively or excluded from
cost reporting. No A/B audit has yet run, so no arm result is repeated.
