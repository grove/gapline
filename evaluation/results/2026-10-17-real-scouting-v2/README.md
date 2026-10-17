# Authorized 1M-token amendment: host preflight still blocked

**Decision: INCONCLUSIVE. Zero A/B audits and zero blinded reviews.** The user
explicitly approved increasing the session token ceiling to **1,000,000**.
The new launcher records and checks that limit; the legacy default remains
250,000. The amended [protocol](../../real-scouting-v2.md), runner and tests were
committed at `1e06543` **before** this fresh preflight. The 180-second and
12-inspection limits, source/skill snapshots, model, read-only sandbox, never
approvals and scope restrictions were unchanged.

The separate host-tool restriction remains unqualified. The controller stopped
after the first v2 curator, before source inspection, curator 2, all eight audits
and both reviewers. No further paid attempts or automatic retries were launched.
The [v1 record](../2026-10-17-real-scouting/README.md) remains unchanged; its failed
curator has not been retroactively accepted under the higher ceiling.

## Actual attempt

Retained: [input/arguments](curator-1-input.json), [host events](curator-1-events.jsonl),
[report](curator-1-report.md), [run receipt](curator-1-run.json),
[host context and emitted tool inventory](curator-1-host.json), and
[stderr](curator-1-stderr.txt). No adapter inspection log exists because no
inspection request occurred. [Status](status.json) lists all unlaunched roles.

| Measurement | Observed |
| --- | --- |
| Model / reasoning / CLI | `gpt-6.1-sol` / `low` / `0.163.0` |
| Actual sandbox / approvals | `read-only` / `never` |
| Model completion | Exit 0, COMPLETED; evaluator rejected the preflight |
| Wall time | 11.625 seconds of 180 |
| Source inspections | **0** of 12; stopped before reading source |
| Input tokens | 23,230, including 19,072 cached |
| Output tokens | 150 |
| Input + output | **23,380 <= 1,000,000** |
| Monetary charge | UNAVAILABLE |
| Source changes / forbidden observed calls | None |
| Timeout / authentication failure | None |

The CLI's local feature catalog declares `code_mode_only` and
`code_mode_only_strict_3p_tools`. The amended invocation enabled both and
disabled `goals`. The emitted inventory was:

```text
apply_patch
clock__curr_time
list_mcp_resource_templates
list_mcp_resources
mcp__inspection__inspect
read_mcp_resource
```

Goal lifecycle APIs disappeared compared with v1, but `apply_patch` and generic
MCP resource APIs remained. The declared inspection/clock-only inventory was
therefore **not achieved** by these flags in this host. The worker obeyed its
pre-source stop condition; the controller independently checked the exact-thread
host trace and retained the failed qualification. The flags did not remove the
remaining APIs, so do not describe them as a working access boundary.

This is evidence of **tool exposure**, not evidence that writes or broader reads
can bypass actual permissions. Those APIs were not invoked and their effective
denial/scope was not independently demonstrated. The official
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents read-only permissions, but did not establish the experimental flags'
removal behavior. Actual host evidence takes precedence over assumptions about
their names. The MCP adapter's own denial tests do not qualify other host APIs.

## What this establishes

The approved ceiling is implemented in the prompt, explicit launcher call,
numeric receipt and post-hoc budget check. [All 52 controller checks pass](prelaunch-tests.txt),
including a mocked exact-million boundary and cached-input accounting, legacy
default preservation, invocation flags, source/variant identities, adapter
access denial and rejection of a failed curator freeze. Mocked launcher calls
in the unit log are not additional paid sessions.

No independent expectations were accepted or frozen; no final audit freeze
exists. The v2 curator read no source, audit skill, earlier curator notes or
other reports. All previously selected source commits and A/B variants remain
in the [original cohort](../../cohorts/real-scouting-1/README.md). No installable
skill or reference changed; #7's shortened verification guidance remains equal
in both arms. No retrieved-project code, tests, builds or dependencies ran.

Positive process evidence: the higher limit was passed, service authentication
worked, requested model/permissions were observed, and the pre-source stop
prevented an unqualified session from collecting evidence. Negative process
evidence: the tested flag combination did not establish the specified tool
inventory. Inconclusive effectiveness evidence: there are no probe-selection,
miss, false-positive, abstention, verification-effort or A/B overhead judgments.
This is not a negative scouting-quality result and supplies no restoration
justification. Model agreement, output length and finding counts are irrelevant
to this unrun comparison.

V2 preparation overhead is one 11.625-second, 23,380-token inference session.
Together with v1's retained failed session, preparation inference totals 369,669
input-plus-output tokens and 86.064 seconds of launcher wall time. Cached input
is already included. Controller usage, controller/total wall time, monetary
charge and human verification effort are UNAVAILABLE. Audit/reviewer usage is
zero because no attempts launched; no audit reports are fabricated.

## Disposition

The budget blocker is resolved prospectively. Qualifying/removing the remaining
native APIs is still required before audits. A future controlled denial test
or a host that exposes only the adapter could establish a suitable boundary;
neither has been performed here. Do not silently weaken the protocol or retry
this preflight as an A/B run.

Keep production unchanged. Leave **#6 OPEN** because realistic matched trials
and independent judgments remain absent. Leave **#7 CLOSED**. The prior PR #13
publishes only v1 until these new local commits are separately published; its
passing CI does not validate this amendment.

Automatic approval review subsequently rejected updating the PR branch: the
user approved the 1M-token change, but publication of the amended commit needs
separate approval. No publication workaround was attempted. The amendment and
all new preflight evidence remain locally committed; see the
[publication receipt](publication-blocker.json). CI for v2 has not run.
