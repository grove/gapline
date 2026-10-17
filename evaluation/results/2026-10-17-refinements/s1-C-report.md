Applied the Gapline method. **One finding: publication does not freeze criterion values.**

**Target and inspection:** Supplied repository snapshot; revision and working-tree identity unavailable. I worked alone and used 3 inspection calls: skill read, file listing, and a batch read of README, all exposed implementation files, and the test file. No files changed; no network or credential access. **Project code, tests, and builds executed: NONE.**

**F1 — Published editions share mutable criteria with the draft**  
**DEMONSTRATED source-level contradiction · High impact · Publication integrity**

- **Contract:** `README.md:6–10` promises that publication freezes criterion names and maximum points, and that recorded assessment percentages remain unchanged after later draft edits.
- **Implementation:** `rubrics/editor.py:52–55` wraps the draft’s existing criteria in a tuple without copying them. `Criterion` remains mutable (`editor.py:4–8`), and the supported `Draft.revise()` method changes those same objects (`editor.py:32–43`). The frozen `Edition` dataclass prevents field reassignment but does not freeze its contained criteria (`editor.py:11–15`).
- **Consequence:** `Catalog.describe()` reads these shared values (`rubrics/catalog.py:15–23`). Recorded percentages also read the edition’s current criteria on every calculation (`rubrics/assessment.py:26–37,40–42`). Thus an ordinary draft revision changes a published edition and can change an existing assessment’s percentage—or make its previously valid scores fail validation.

For example, using the test fixture’s maxima of 10 and 20 and scores of 5 and 15 (`tests/test_rubrics.py:10–21`), revising the draft’s `shape` maximum to 40 leads the calculation to use a denominator of 60 instead of 30: **33.33 instead of 66.67**. This is a source-derived prediction, not an executed result.

**Counterevidence and protection:** The tuple preserves criterion membership and order when draft entries are added or removed; the tests check that behavior (`tests/test_rubrics.py:23–32`). Description dictionaries also resist external mutation (`:34–37`), and submitted scores are copied (`:17–21`). Those protections do not isolate criterion objects. The inspected tests exercise rejected revisions (`:39–49`), but never a successful revision after publication. No caller field mutation is needed to trigger this gap, so the caller restriction in `README.md:19` does not resolve it.

**Next action:** Copy criterion values into immutable publication records when freezing. **PROPOSED — NOT RUN:** Record the fixture assessment, revise the draft’s criterion name and maximum, and publish again. Assert that the original description and percentage remain unchanged while the new edition reflects the revisions. An unchanged original would refute the predicted effect.

**Limits:** This was static inspection of the exposed implementation and tests. Runtime behavior, external callers, and deployment context were not assessed. No additional supported findings are reported.