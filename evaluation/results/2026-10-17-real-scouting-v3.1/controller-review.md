# Controller review of PR #13

What this change does: It retains qualification of the existing read-only host,
adopts a capability-based acceptance gate, and runs one fixed real-repository
cohort through the existing launcher and adapter. It preserves earlier failures
and the new timeout, without changing the production skill.

Reviewed the branch changes, shared launcher and its existing callers,
inspection server and canary diagnostic, retained qualification replay,
cohort extraction/identity checks, curator freeze, matched worker setup,
reviewer masking and input isolation, result summaries and regression tests.
Assumed load is one controller running this fixed, sequential cohort. No new
agent framework or production runtime is introduced. Legacy launcher defaults
remain unchanged; the approved ceiling/strict flags are explicit opt-ins.

No concrete must-fix defect was established for this stopped cohort. Actual
host acceptance and source/expectation freezes replay successfully; all 58
regressions pass. The timeout correctly prevents subsequent audits/reviews.
The cost replay retains unavailable final usage rather than treating it as zero.
Production bytes match the main baseline and both variants preserve #7.

Known limits are explicit: interpreter path rather than an independently pinned
Python binary hash; code-mode activity parsing plus host events rather than a
general isolation proof; post-hoc token accounting; malformed requests may not
advance the adapter's internal counter but every request advances the controller
count; one killed session has no final usage; no reviewer judgments completed.
These are not certified away by passing development tests. The helper's paid
phases must not be invoked as a replay or without fresh effect/run authorization.

Verdict: Ship the infrastructure/evidence after exact-candidate CI passes and
separate merge approval. This is not approval to resume paid sessions, restore
scouting or close #6. The effectiveness decision remains INCONCLUSIVE.

Not checked: General host isolation, arbitrary/resource-enabled MCP servers,
human developer effort, upstream runtime behavior, or model quality on the
unrun cases. No independent external PR reviewer is claimed.
