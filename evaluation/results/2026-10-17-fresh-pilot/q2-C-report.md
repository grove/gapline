Found **one supported test gap**; no implementation defect established.

**F1 — Expired leases are not tested before reassignment**
**Medium impact · Tests · SUPPORTED**

The contract says a lease expires exactly at its deadline and only an unexpired lease may finish ([README.md:16](README.md#L16)). The implementation enforces this with `now >= job["deadline"]` ([leases.py:60](leases.py#L60)).

However, the expiry test first reassigns the job, then rejects the old worker using its stale token ([test_leases.py:22](test_leases.py#L22)). That rejection remains protected by the token comparison even if `finish` loses its deadline check. Every other tested completion occurs before its deadline. Thus, the inspected assertions do not independently protect against accepting expired work when no replacement worker has reserved it.

Counterevidence: the current implementation correctly checks expiry, and the existing test meaningfully protects stale-token fencing. This is a regression-protection gap, not an observed runtime failure.

**PROPOSED — NOT RUN:** Add checks that completion succeeds just before the deadline but returns `False` exactly at and after it, without intervening reassignment; verify rejected completion preserves state and result.

Audit scope and limits: inspected the complete `README.md`, `leases.py`, `test_leases.py`, and project-installed Gapline `SKILL.md` using two shell inspection calls (`/bin/bash`, `login=false`; file listing and numbered reads). Delegation was skipped because this small, coupled implementation did not justify its cost. Revision and working-tree identity were not independently established; Git was not invoked.

**Project code, tests, and builds executed: NONE.** No files changed, dependencies installed, network tools used, or credentials accessed. Runtime behavior and external adapter guarantees were not assessed.
