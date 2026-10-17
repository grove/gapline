Two supported test-protection gaps; no demonstrated runtime defect.

1. **Frozen pulls lack interleaving coverage — SUPPORTED, medium impact.**
   [README.md:9](README.md:9) promises that writes between pages remain excluded until a later pull. The pagination test performs all writes before `begin` ([test_changes.py:7](test_changes.py:7)), so it would not distinguish a continuation that incorrectly includes subsequent writes or advances its checkpoint.

   Counterevidence: the implementation carries the original upper revision through continuations and filters against it ([changes.py:58](changes.py:58)). This supports current correctness; the finding concerns regression protection.

   **PROPOSED — NOT RUN:** Append changes between pages; verify the resumed pull excludes them, retains its original checkpoint, and a later pull returns them.

2. **Expiration during an active pull lacks coverage — SUPPORTED, medium impact.**
   [README.md:17](README.md:17) requires expired continuations to raise rather than silently skip history. The compaction test checks only a new `begin` after compaction ([test_changes.py:22](test_changes.py:22)); no test compacts between `begin` and `resume`.

   Counterevidence: both entry points currently use the same expiration check ([changes.py:45](changes.py:45), [changes.py:56](changes.py:56)). Current source therefore supports the promised behavior, but the tests do not independently protect continuation expiration.

   **PROPOSED — NOT RUN:** Obtain a continuation, compact beyond its position while leaving later events retained, and verify `resume` raises `CursorExpired`. Also check that a continuation exactly at the floor remains valid.

Inspected the project-installed Gapline skill, README, complete implementation, and complete test file. Used four inspection calls with file listing, search, and numbered reads through `/bin/bash`, `login=false`. Worked alone; no files changed, Git or network used, or credentials accessed. **Project code, tests, and builds executed: NONE.**

Revision and working-tree byte identity were not independently established; evaluator identity is external to this inspection. Runtime behavior, performance, and the external adapter/snapshot endpoint were not assessed. These findings establish missing checks in the inspected tests, not production failures.
