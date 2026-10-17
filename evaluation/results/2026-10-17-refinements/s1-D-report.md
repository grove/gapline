One finding survived review.

**G1 — Published editions share mutable criteria with their draft**  
**DEMONSTRATED source-level contract contradiction · High impact · Publication isolation**

- **Expected:** Publication freezes criterion names and maxima; recorded percentages remain unchanged after draft edits ([README.md:6–10](README.md)).
- **Evidence:** `Draft.freeze()` wraps existing criterion objects in a tuple without copying them (`rubrics/editor.py:52–55`). Those objects are mutable (`editor.py:4–8`), and the supported `revise()` method changes their names and maxima in place (`editor.py:32–43`). The catalog retains that edition (`rubrics/catalog.py:6–8`), while every percentage lookup recalculates using its current criterion objects (`rubrics/assessment.py:26–37,40–42`).
- **Consequence:** Revising a published draft’s maximum can change an already recorded percentage—or make retrieval reject a previously valid score. Revising a name also changes the published description. This follows from the source; no runtime failure was reproduced.
- **Counterevidence and test gap:** The tuple protects criterion membership/order, and `describe()` returns fresh dictionaries. Existing tests verify add/remove isolation and returned-description isolation (`tests/test_rubrics.py:23–37`), but never successfully revise a criterion after publication. The invalid-revision tests (`tests/test_rubrics.py:39–49`) do not exercise this path. The documented restriction against callers mutating model fields does not prevent the issue: `Draft.revise()` is a service method.
- **Next action — PROPOSED — NOT RUN:** Record scores of 5/10 and 15/20, then revise the draft’s first name and maximum to 20. Assert the original edition retains its name and maximum and the recorded percentage remains `66.67`; a new edition should reflect the revisions. Copy criterion values when freezing to remove the shared state.

**Scope and limits:** Applied `skill/SKILL.md` using only the inspection tool: **3 calls**, comprising the skill read, file listing, and reads of README, all four exposed package files, and the sole exposed test file. Worked alone; changed no files. **Project code, tests, and builds executed: NONE.** No shell, network, credentials, or other sessions were accessed.

Target was the supplied repository snapshot. Revision and working-tree identity were unavailable because no Git metadata was supplied. Runtime behavior and environment-dependent effects were not assessed; the finding is based on static evidence.