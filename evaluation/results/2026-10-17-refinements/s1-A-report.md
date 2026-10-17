**One finding: published editions share mutable criteria with drafts.**

**G1 — High impact · DEMONSTRATED source-level contradiction · Publication and assessment integrity**

The documented contract freezes criterion names and maximum points on publication and promises stable percentages for recorded assessments (`README.md:6–10`).

However:

- `Draft.freeze` wraps existing criteria in a tuple without copying them (`rubrics/editor.py:52–55`).
- `Draft.revise` mutates those same criterion objects (`rubrics/editor.py:32–43`).
- `Catalog` stores the resulting edition directly (`rubrics/catalog.py:6–9`).
- Assessments recalculate percentages from the edition’s current criteria (`rubrics/assessment.py:26–37,40–42`).

Consequently, an authorized draft revision changes previously published names or maxima. From the inspected source, the assessment fixture’s scores of 5 and 15 initially yield 66.67%; revising the draft’s `shape` maximum from 10 to 30 makes the recorded assessment calculate as 40.00%. This is a source-derived consequence, **not an executed observation**. Lowering a maximum below a recorded score can instead make percentage retrieval raise `ValueError`.

**Counterevidence and test protection:** `Edition` is frozen, but its contained `Criterion` objects are mutable (`rubrics/editor.py:4–15`). Structural edits are isolated by the tuple, and `describe` constructs fresh dictionaries (`rubrics/catalog.py:15–24`). Tests protect those properties (`tests/test_rubrics.py:23–37`), but do not perform a successful criterion revision after publication. The revision test exercises rejected inputs only (`tests/test_rubrics.py:39–49`). The documented caller restriction does not resolve this: the problematic path uses `Draft.revise`, without directly mutating model fields.

**Next action:** Copy criterion values into independent, preferably immutable published records. **PROPOSED — NOT RUN:** Add a regression check that records an assessment, successfully revises draft names and maxima, and verifies that the old edition and percentage remain unchanged while a new publication reflects the edits.

**Scope and limits:** Applied `skill/SKILL.md` alone, using three inspection calls: skill read, file listing, and batched reads of `README.md`, all four exposed `rubrics` files, and `tests/test_rubrics.py`. No delegation, changes, network access, or credential access. **Project code, tests, and builds executed: NONE.** The target was the supplied repository snapshot; no Git revision or working-tree identity was available. Runtime behavior and integration context were not assessed. No additional supported findings emerged from the inspected scope.