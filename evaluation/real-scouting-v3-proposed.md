# Prospective capability boundary amendment — PROPOSED, NO AUDITS AUTHORIZED

This proposal supersedes only the tool-inventory condition in
[v2](real-scouting-v2.md), based on the retained
[capability qualification](results/2026-10-17-host-capabilities/README.md).
It is not an audit freeze, an accepted expectation set or authority to launch
the eight A/B audits. The current runtime gate remains closed pending adoption
and a complete pre-audit freeze.

## Required effective boundary

Retain the exact tested Codex CLI binary/version, read-only permission profile,
never approvals, disabled shell/network-facing tools, hooks/apps/plugins,
memories, delegation, automatic project instructions and host skill discovery.
Retain `--ignore-user-config`, `--ignore-rules`, and the single explicit
`inspection` server running the byte-pinned `inspect_server.py`. Freeze the
complete invocation, server allowlist, adapter/launcher hashes and host settings
alongside source/skill identities and independent expectations.

Qualify native `apply_patch` by actual canary write denials, ordinary writable
file modes, host tool outcomes and unchanged controller-observed disk hashes.
Tool visibility alone neither grants write permission nor establishes denial.
Audits still may not invoke it. A write attempt during an audit stops that run
and is retained, even if denied.

Qualify generic MCP resource APIs by the effective configured-server boundary:
the sole server advertises tools only and rejects `resources/list`,
`resources/templates/list` and `resources/read` as unsupported. Actual outside
file/traversal URI and unknown-server probes must return no content. Permitted
adapter reads must succeed, and adapter outside-path reads must fail. This
qualifies **absence of a resource-reading channel**, not a filesystem allowlist
inside the generic MCP client. A resource-enabled, additional or changed server
invalidates this qualification and requires its own positive/negative access
tests before adoption. No arbitrary URI proxy may be enabled by this amendment.

Known visible native patch/resource APIs may therefore coexist with the frozen
effective boundary. Continue retaining inventory and actual tool calls; any
new or unqualified capability fails closed pending investigation. Do not replace
capability validation with prompt compliance. Clock and trusted host orchestration
remain available, never execution of repository code.

## Evidence validity and next freeze

The qualification receipt must reference actual tool calls/results, host
settings, fixture modes/hashes, exact CLI binary and OS, server/launcher bytes,
and the user-authorized diagnostic plan. A passing report without those receipts
is insufficient. Requalify after relevant host, binary, configuration, server,
permissions or adapter changes. Check frozen identities before every run and
record observed model/effort/permissions and activity afterward.

Retain 1M cumulative input-plus-output tokens, 180 seconds and 12 inspections
per audit/reviewer, equal A/B access, fresh sessions, counterbalanced order,
withheld expectations and two independent blinded reviews. Generic resource
APIs and patch writes remain forbidden audit activity. Freeze expectations and
the adopted protocol/host boundary before any audit; do not rehabilitate either
failed preflight retrospectively. Keep all prior failures and limitations.

No production skill change is proposed. Keep #7 closed and its shortened
verification text identical in both arms. Host qualification is not scouting
effectiveness evidence and cannot satisfy #6's matched-trial acceptance gap.
