Found one supported gap in the sampled file-storage transaction path.

**G1 — Async listener discards recovery state after storage failure**  
**Failure handling · SUPPORTED · Medium impact**

- **Expected:** The tracker’s `raise_on_error=True` policy raises storage errors and retains pending operations for recovery. Tests explicitly protect retained state after failure ([tests/unit/test_file_object.py:857](tests/unit/test_file_object.py#L857)).
- **Observed:** `AsyncFileObjectListener.after_commit()` launches an unawaited task, catches the tracker’s exception, and unconditionally removes the tracker from `session.info` ([advanced_alchemy/_listeners.py:404](advanced_alchemy/_listeners.py#L404)). The listener therefore discards the session’s recovery handle even though `commit_async()` deliberately preserves state on errors ([session_tracker.py:148](advanced_alchemy/types/file_object/session_tracker.py#L148)).
- **Consequence:** A storage failure after database commit can leave file metadata committed without its file, while the committing caller receives no storage exception and the normal session tracker is removed.
- **Counterevidence:** The tracker logs storage errors with tracebacks, so failures are observable in logs. Background execution may be intentional; this finding concerns the loss of retained recovery state and error propagation, not a claim that background execution itself is incorrect. The inspected tests exercise the tracker directly, not this listener boundary.
- **PROPOSED — NOT RUN:** Inject an async save failure with `file_object_raise_on_error=True`, invoke the listener, and wait for its task. Check caller-visible failure and whether failed operations remain recoverable. An explicit alternative recovery mechanism would weaken this concern.

**Scope and limits:** Applied `skill/SKILL.md` alone, read-only, to the supplied `litestar-org/advanced-alchemy` snapshot identified as `e051a5de1a008b70f2d67b416e236a8c59e69433`. Inspected the file-object tracker, data type, listener implementation, and selected unit tests using 12 inspection calls, including three rejected argument attempts. No Git metadata was available to independently verify snapshot or working-tree identity.

**Project code, tests, and builds executed: NONE.** No edits, network access, or delegation. Other repository behavior, full-suite protection, and runtime outcomes were not assessed.