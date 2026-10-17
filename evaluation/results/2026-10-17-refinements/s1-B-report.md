One finding survived scrutiny.

**F1 — Published editions share mutable criteria with their drafts**  
**DEMONSTRATED source-level contradiction · High impact · Publication and assessment integrity**

- **Contract:** `README.md:6–10` promises that publication freezes criterion names and maximum points, and that later draft edits cannot change recorded assessment percentages.
- **Evidence:** `Draft.freeze()` places existing criterion objects into a tuple (`rubrics/editor.py:52–55`). Those objects remain mutable (`editor.py:4–8`), and the supported `Draft.revise()` method changes them directly (`editor.py:32–43`). `Catalog.publish()` stores that edition without another copy (`rubrics/catalog.py:6–10`). Recorded percentages subsequently read its current maxima (`rubrics/assessment.py:26–42`).
- **Consequence:** By source tracing, recording the test’s scores of 5/10 and 15/20, then revising the draft’s first maximum to 20, changes the recorded percentage from 66.67 to 50.00. Criterion name revisions likewise alter published descriptions. These consequences were **not executed**.
- **Counterevidence and test protection:** The tuple isolates additions/removals, the frozen edition protects its own fields, and `describe()` returns fresh dictionaries. Existing tests verify those protections (`tests/test_rubrics.py:23–37`), but none performs a successful criterion revision after publication. The invalid-revision checks (`tests/test_rubrics.py:39–47`) do not exercise this shared-object path. The defect requires no direct model-field mutation.
- **Next action:** Give each publication independent criterion values. **PROPOSED — NOT RUN:** Add a regression that records an assessment, revises the draft’s name and maximum, and verifies the original edition and percentage remain unchanged while a new publication reflects the revision.

**Scope and limits:** Applied `skill/SKILL.md` alone using three inspection calls: the skill read, file listing, and a batched read of `README.md`, all four exposed `rubrics` files, and `tests/test_rubrics.py`. The audit followed publication, editing, assessment calculation, and their test protection. Repository revision and working-tree identity were unavailable; no Git metadata was inspected.

**Project code, tests, and builds executed: NONE.** No files changed, delegation, network access, or other-session inspection occurred. Runtime behavior remains unverified; this single supported finding is not a completeness claim.