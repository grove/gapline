# Larger real-repository scouting comparison v2 (#6)

This is a prospective amendment to [v1](real-scouting-v1.md), approved after
the user explicitly raised the session token ceiling to **1,000,000**. All v1
raw artifacts and its failed preflight remain unchanged. Do not reinterpret
the v1 curator as valid or count it as an audit. PR #13 publishes that history.

The source snapshots, A/B skill text, common question, single-agent method,
sequential counterbalanced order, model (`gpt-6.1-sol`, low), read-only sandbox,
never approvals, and **180 seconds / 12 inspections per session** remain as in
v1. The ceiling means cumulative **input plus output tokens**, including cached
input once, not a larger context window. It remains an instruction ceiling
validated after completion, not a host-enforced token cutoff. Monetary cost
remains UNAVAILABLE unless the host supplies it.

The old shared launcher's default stays 250,000 for historical protocols;
this cohort explicitly requests 1,000,000 and records it. Freeze the amendment,
runner, source/variant identities and tests before further paid sessions.

## Qualify the unresolved host restriction

The installed CLI 0.163.0 declares `code_mode_only` and
`code_mode_only_strict_3p_tools` features. Enable both, and disable `goals`, for
every v2 role through explicit invocation overrides. Their presence in the
local feature catalog does **not** establish their behavior. Official
[configuration documentation](https://learn.chatgpt.com/docs/config-file/config-reference)
does not establish that these experimental switches remove the extra APIs.
The first v2 curator must emit the actual `ALL_TOOLS` names **before reading
repository files** and stop immediately if any tool other than the inspection
adapter and clock facilities is present. The controller must verify the exact
host-emitted inventory and settings; no audit may launch on an assumed flag
effect. Native host orchestration computation is permitted, never execution of
repository code. The existing adapter remains the only supplied source channel.

If that fails, retain the attempt and stop. Do not weaken the available-tool
restriction, substitute prompt compliance for host permissions, or change
controls mid-comparison. No dangerous sandbox mode, credential extraction,
additional write/network tools, or new framework is authorized or needed.

## Fresh roles and evidence separation

Authorize the original planned eight audits and two blinded reviewers, preceded
by two fresh v2 curator sessions. Restarting preflight is the direct consequence
of the approved budget revision, not an extra A/B retry. No audits previously
ran, so no case/arm audit is repeated. New curators receive only source; they
do not receive v1 curator notes. Each paid role gets the same revised ceiling
and host controls; fresh processes and neutral trees remain mandatory.

Use new output `results/2026-10-17-real-scouting-v2/` and work directory
`/private/tmp/gapline-scout-real-v2/workers`. Keep v1 outputs immutable. Put new
expectations in the v2 output and freeze them with the protocol, runner, host
receipts, archive/variant identities and question before audits. Reviewer inputs
must be frozen before either review; judgments before costs are unmasked.

The four snapshots were prepared but **never audited**. r1/r2 source and v1
curator notes are now published. Their reuse is disclosed preparation exposure,
not a claim of unseen public data. New workers/reviewers see neither those notes
nor prior results. Independent expectations remain nonexhaustive process-role
model judgments, not maintainer ground truth. No controller source interpretations
are supplied to workers. If actual session leakage is observed, stop.

All v1 retention, no-retry/stop conditions, masking, independent judgment,
positive/negative/inconclusive evidence, decision and issue-closure criteria
otherwise remain. No production skill change precedes the evaluation. #7 stays
closed and its shortened verification wording remains identical in both arms.
