# Case s1

## Source (numbered original lines)

### README.md

```
1: # Studio assessment rubrics
2: 
3: A small in-memory service used by an art school to draft marking rubrics,
4: publish numbered editions, and calculate assessment percentages.
5: 
6: Teachers may continue editing a draft after publishing it. Publication freezes
7: the title, criterion order, criterion names, and maximum points for that edition.
8: An assessment always uses the edition recorded when it was submitted, so an
9: already recorded assessment has the same percentage after later draft edits.
10: A new publication picks up the current draft values.
11: 
12: Scores must supply exactly one entry for every published criterion, with each
13: score between zero and its maximum. Criterion keys are unique within a draft.
14: Removing the final criterion is allowed in a draft, but an empty draft cannot be
15: published. The service uses integral points and rounds percentages to two digits.
16: 
17: `rubrics/editor.py` handles authoring, `rubrics/catalog.py` stores editions, and
18: `rubrics/assessment.py` records and calculates results. All storage is local to
19: one service instance. Callers use these methods rather than mutating model fields.
20: 
21: Run the checks with `python3 -m unittest discover -s tests -v` from this directory.
```

### rubrics/__init__.py

```

```

### rubrics/assessment.py

```
1: from dataclasses import dataclass
2: from decimal import Decimal, ROUND_HALF_UP
3: 
4: 
5: @dataclass(frozen=True)
6: class Assessment:
7:     student: str
8:     edition: int
9:     scores: tuple[tuple[str, int], ...]
10: 
11: 
12: class Assessments:
13:     def __init__(self, catalog):
14:         self.catalog = catalog
15:         self._records = {}
16: 
17:     def record(self, reference, student, edition, scores):
18:         if reference in self._records:
19:             raise ValueError('assessment already exists')
20:         if not student.strip():
21:             raise ValueError('student is required')
22:         snapshot = tuple(scores.items())
23:         self._percentage(edition, dict(snapshot))
24:         self._records[reference] = Assessment(student, edition, snapshot)
25: 
26:     def _percentage(self, number, scores):
27:         criteria = self.catalog.get(number).criteria
28:         if set(scores) != {row.key for row in criteria}:
29:             raise ValueError('scores do not match edition')
30:         for row in criteria:
31:             value = scores[row.key]
32:             if type(value) is not int or not 0 <= value <= row.maximum:
33:                 raise ValueError('score outside criterion range')
34:         total = sum(scores.values())
35:         maximum = sum(row.maximum for row in criteria)
36:         return (Decimal(total) * 100 / maximum).quantize(
37:             Decimal('0.01'), rounding=ROUND_HALF_UP
38:         )
39: 
40:     def percentage(self, reference):
41:         record = self._records[reference]
42:         return self._percentage(record.edition, dict(record.scores))
```

### rubrics/catalog.py

```
1: class Catalog:
2:     def __init__(self):
3:         self._editions = {}
4:         self._next_number = 1
5: 
6:     def publish(self, draft):
7:         edition = draft.freeze(self._next_number)
8:         self._editions[edition.number] = edition
9:         self._next_number += 1
10:         return edition.number
11: 
12:     def get(self, number):
13:         return self._editions[number]
14: 
15:     def describe(self, number):
16:         edition = self.get(number)
17:         return {
18:             'number': number,
19:             'title': edition.title,
20:             'criteria': [
21:                 {'key': row.key, 'name': row.name, 'maximum': row.maximum}
22:                 for row in edition.criteria
23:             ],
24:         }
```

### rubrics/editor.py

```
1: from dataclasses import dataclass
2: 
3: 
4: @dataclass
5: class Criterion:
6:     key: str
7:     name: str
8:     maximum: int
9: 
10: 
11: @dataclass(frozen=True)
12: class Edition:
13:     number: int
14:     title: str
15:     criteria: tuple[Criterion, ...]
16: 
17: 
18: class Draft:
19:     def __init__(self, title):
20:         if not title.strip():
21:             raise ValueError('title is required')
22:         self.title = title
23:         self._criteria = []
24: 
25:     def add(self, key, name, maximum):
26:         if not key or not name.strip() or type(maximum) is not int or maximum <= 0:
27:             raise ValueError('invalid criterion')
28:         if any(item.key == key for item in self._criteria):
29:             raise ValueError('duplicate criterion')
30:         self._criteria.append(Criterion(key, name, maximum))
31: 
32:     def revise(self, key, *, name=None, maximum=None):
33:         item = next((item for item in self._criteria if item.key == key), None)
34:         if item is None:
35:             raise KeyError(key)
36:         if name is not None and not name.strip():
37:             raise ValueError('name is required')
38:         if maximum is not None and (type(maximum) is not int or maximum <= 0):
39:             raise ValueError('maximum must be a positive integer')
40:         if name is not None:
41:             item.name = name
42:         if maximum is not None:
43:             item.maximum = maximum
44: 
45:     def remove(self, key):
46:         for index, item in enumerate(self._criteria):
47:             if item.key == key:
48:                 del self._criteria[index]
49:                 return
50:         raise KeyError(key)
51: 
52:     def freeze(self, number):
53:         if not self._criteria:
54:             raise ValueError('cannot publish an empty rubric')
55:         return Edition(number, self.title, tuple(self._criteria))
```

### tests/test_rubrics.py

```
1: import unittest
2: from decimal import Decimal
3: from rubrics.editor import Draft
4: from rubrics.catalog import Catalog
5: from rubrics.assessment import Assessments
6: 
7: 
8: class RubricTests(unittest.TestCase):
9:     def setUp(self):
10:         self.draft = Draft('Observational drawing')
11:         self.draft.add('shape', 'Shape', 10)
12:         self.draft.add('tone', 'Tone', 20)
13:         self.catalog = Catalog()
14:         self.number = self.catalog.publish(self.draft)
15:         self.results = Assessments(self.catalog)
16: 
17:     def test_weighted_percentage_and_score_copy(self):
18:         scores = {'shape': 5, 'tone': 15}
19:         self.results.record('a', 'Rae', self.number, scores)
20:         scores['shape'] = 0
21:         self.assertEqual(self.results.percentage('a'), Decimal('66.67'))
22: 
23:     def test_adding_removing_and_title_edits_leave_edition_structure(self):
24:         self.draft.title = 'Composition'
25:         self.draft.remove('shape')
26:         self.draft.add('space', 'Space', 15)
27:         description = self.catalog.describe(self.number)
28:         self.assertEqual(description['title'], 'Observational drawing')
29:         self.assertEqual([row['key'] for row in description['criteria']], ['shape', 'tone'])
30:         second = self.catalog.publish(self.draft)
31:         self.assertEqual(second, self.number + 1)
32:         self.assertEqual(self.catalog.describe(second)['title'], 'Composition')
33: 
34:     def test_description_does_not_allow_external_changes(self):
35:         view = self.catalog.describe(self.number)
36:         view['criteria'][0]['maximum'] = 1000
37:         self.assertEqual(self.catalog.describe(self.number)['criteria'][0]['maximum'], 10)
38: 
39:     def test_validation_preserves_draft(self):
40:         for maximum in (0, -1, True, 2.5):
41:             with self.assertRaises(ValueError):
42:                 self.draft.revise('shape', maximum=maximum)
43:         with self.assertRaises(ValueError):
44:             self.draft.revise('shape', name=' ')
45:         self.assertEqual(self.catalog.describe(self.number)['criteria'][0]['maximum'], 10)
46:         with self.assertRaises(KeyError):
47:             self.draft.revise('unknown', maximum=10)
48:         with self.assertRaises(KeyError):
49:             self.draft.remove('unknown')
50: 
51:     def test_bad_scores_and_duplicate_records(self):
52:         for scores in ({'shape': 1}, {'shape': 11, 'tone': 0},
53:                        {'shape': True, 'tone': 0}, {'shape': -1, 'tone': 0}):
54:             with self.assertRaises(ValueError):
55:                 self.results.record('bad', 'Rae', self.number, scores)
56:         self.results.record('ok', 'Rae', self.number, {'shape': 10, 'tone': 20})
57:         with self.assertRaises(ValueError):
58:             self.results.record('ok', 'Rae', self.number, {'shape': 0, 'tone': 0})
59: 
60:     def test_empty_and_duplicate_criteria(self):
61:         with self.assertRaises(ValueError):
62:             self.catalog.publish(Draft('Empty'))
63:         with self.assertRaises(ValueError):
64:             self.draft.add('shape', 'Again', 1)
65:         with self.assertRaises(ValueError):
66:             self.draft.add('x', 'X', 0)
67: 
68: 
69: if __name__ == '__main__':
70:     unittest.main()
```

## Frozen evaluator interpretation (nonexhaustive; challenge if wrong)

{
  "contracts": [
    {
      "path": "README.md",
      "exact": "Publication freezes\nthe title, criterion order, criterion names, and maximum points for that edition.",
      "start_line": 6
    },
    {
      "path": "README.md",
      "exact": "An assessment always uses the edition recorded when it was submitted, so an\nalready recorded assessment has the same percentage after later draft edits.",
      "start_line": 8
    },
    {
      "path": "README.md",
      "exact": "A new publication picks up the current draft values.",
      "start_line": 10
    }
  ],
  "expected_interpretation": "Draft.freeze freezes only the criteria container, retaining mutable Criterion objects. Draft.revise mutates those shared objects. Catalog editions therefore change and Assessments.percentage recomputes old results using changed maxima. A 10/10 recorded result becomes 50 percent after raising the draft maximum to 20. Renaming a draft criterion also changes the published edition.",
  "accepted_alternatives": [
    "One root-cause finding about shallow publication and mutable criteria, substantiated by the downstream assessment effect.",
    "One result-stability finding tracing editor -> catalog -> assessment with criterion aliasing identified as its cause.",
    "A repair suggestion to copy or immutably snapshot each criterion at publication, with a regression that edits a published draft and rereads an existing result."
  ],
  "criteria": {
    "useful_probes": [
      "Trace freeze -> Catalog.publish/get -> Assessments.percentage, not just frozen dataclass syntax.",
      "Distinguish add/remove list stability from element-field stability.",
      "Use a public draft revision after recording an assessment as a concrete trigger."
    ],
    "false_positives": [
      "Claiming that adding/removing criteria or changing the title already mutates an edition.",
      "Claiming caller mutation of Catalog.describe or the original score dict changes stored data.",
      "Presenting the deliberately unsupported direct model-field mutation as a separate critical exposure."
    ],
    "uncertainty": "The immutability/result-stability contract is explicit; do not downgrade this to an unspecified policy question.",
    "verification": "Static alias tracing is sufficient; a reproducer may show 100.00 -> 50.00. Do not claim public tests already cover Draft.revise after publication."
  }
}

## Report r06

One finding survived scrutiny.

**F1 — Published editions share mutable criteria with their drafts**  
**DEMONSTRATED source-level contradiction · High impact · Publication and assessment integrity**

- **Contract:** `README.md:6–10` promises that publication freezes criterion names and maximum points, and that later draft edits cannot change recorded assessment percentages.
- **Evidence:** `Draft.freeze()` places existing criterion objects into a tuple (`rubrics/editor.py:52–55`). Those objects remain mutable (`editor.py:4–8`), and the supported `Draft.revise()` method changes them directly (`editor.py:32–43`). `Catalog.publish()` stores that edition without another copy (`rubrics/catalog.py:6–10`). Recorded percentages subsequently read its current maxima (`rubrics/assessment.py:26–42`).
- **Consequence:** By source tracing, recording the test’s scores of 5/10 and 15/20, then revising the draft’s first maximum to 20, changes the recorded percentage from 66.67 to 50.00. Criterion name revisions likewise alter published descriptions. These consequences were **not executed**.
- **Counterevidence and test protection:** The tuple isolates additions/removals, the frozen edition protects its own fields, and `describe()` returns fresh dictionaries. Existing tests verify those protections (`tests/test_rubrics.py:23–37`), but none performs a successful criterion revision after publication. The invalid-revision checks (`tests/test_rubrics.py:39–47`) do not exercise this shared-object path. The defect requires no direct model-field mutation.
- **Next action:** Give each publication independent criterion values. **PROPOSED — NOT RUN:** Add a regression that records an assessment, revises the draft’s name and maximum, and verifies the original edition and percentage remain unchanged while a new publication reflects the revision.

[Telemetry line withheld for blind review.]

**Project code, tests, and builds executed: NONE.** No files changed, delegation, network access, or other-session inspection occurred. Runtime behavior remains unverified; this single supported finding is not a completeness claim.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "rubrics/assessment.py", "rubrics/catalog.py", "rubrics/editor.py", "rubrics/__init__.py", "tests/test_rubrics.py"]}

### Public investigation notes before final report

I’ll read the audit method, then inspect the documented contracts, implementation, and tests within the 12-call limit. I’ll work alone and leave all files unchanged.

## Report r08

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

[Telemetry line withheld for blind review.]

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "rubrics/assessment.py", "rubrics/catalog.py", "rubrics/editor.py", "rubrics/__init__.py", "tests/test_rubrics.py"]}

### Public investigation notes before final report

I’ll read the audit skill, then trace documented contracts through implementation and test coverage using only the inspection tool. I’ll keep the audit read-only and report at most three evidence-backed findings.

The audit trace found one source-level contradiction: publication copies the criterion container but retains mutable criterion objects. Draft revisions can therefore change published editions and previously recorded percentages. The tests cover structural edits and copied descriptions, but do not exercise a valid criterion revision after publication.

## Report r19

Applied the audit method. **One finding: publication does not freeze criterion values.**

[Telemetry line withheld for blind review.]

**F1 — Published editions share mutable criteria with the draft**  
**DEMONSTRATED source-level contradiction · High impact · Publication integrity**

- **Contract:** `README.md:6–10` promises that publication freezes criterion names and maximum points, and that recorded assessment percentages remain unchanged after later draft edits.
- **Implementation:** `rubrics/editor.py:52–55` wraps the draft’s existing criteria in a tuple without copying them. `Criterion` remains mutable (`editor.py:4–8`), and the supported `Draft.revise()` method changes those same objects (`editor.py:32–43`). The frozen `Edition` dataclass prevents field reassignment but does not freeze its contained criteria (`editor.py:11–15`).
- **Consequence:** `Catalog.describe()` reads these shared values (`rubrics/catalog.py:15–23`). Recorded percentages also read the edition’s current criteria on every calculation (`rubrics/assessment.py:26–37,40–42`). Thus an ordinary draft revision changes a published edition and can change an existing assessment’s percentage—or make its previously valid scores fail validation.

For example, using the test fixture’s maxima of 10 and 20 and scores of 5 and 15 (`tests/test_rubrics.py:10–21`), revising the draft’s `shape` maximum to 40 leads the calculation to use a denominator of 60 instead of 30: **33.33 instead of 66.67**. This is a source-derived prediction, not an executed result.

**Counterevidence and protection:** The tuple preserves criterion membership and order when draft entries are added or removed; the tests check that behavior (`tests/test_rubrics.py:23–32`). Description dictionaries also resist external mutation (`:34–37`), and submitted scores are copied (`:17–21`). Those protections do not isolate criterion objects. The inspected tests exercise rejected revisions (`:39–49`), but never a successful revision after publication. No caller field mutation is needed to trigger this gap, so the caller restriction in `README.md:19` does not resolve it.

**Next action:** Copy criterion values into immutable publication records when freezing. **PROPOSED — NOT RUN:** Record the fixture assessment, revise the draft’s criterion name and maximum, and publish again. Assert that the original description and percentage remain unchanged while the new edition reflects the revisions. An unchanged original would refute the predicted effect.

**Limits:** This was static inspection of the exposed implementation and tests. Runtime behavior, external callers, and deployment context were not assessed. No additional supported findings are reported.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "rubrics/__init__.py", "rubrics/assessment.py", "rubrics/catalog.py", "rubrics/editor.py", "tests/test_rubrics.py"]}

### Public investigation notes before final report

I’ll read the audit skill, then inspect the repository within the 12-call limit. I’ll work alone, make no changes, and report only gaps supported by the exposed files.

## Report r20

One finding survived review.

**G1 — Published editions share mutable criteria with their draft**  
**DEMONSTRATED source-level contract contradiction · High impact · Publication isolation**

- **Expected:** Publication freezes criterion names and maxima; recorded percentages remain unchanged after draft edits ([README.md:6–10](README.md)).
- **Evidence:** `Draft.freeze()` wraps existing criterion objects in a tuple without copying them (`rubrics/editor.py:52–55`). Those objects are mutable (`editor.py:4–8`), and the supported `revise()` method changes their names and maxima in place (`editor.py:32–43`). The catalog retains that edition (`rubrics/catalog.py:6–8`), while every percentage lookup recalculates using its current criterion objects (`rubrics/assessment.py:26–37,40–42`).
- **Consequence:** Revising a published draft’s maximum can change an already recorded percentage—or make retrieval reject a previously valid score. Revising a name also changes the published description. This follows from the source; no runtime failure was reproduced.
- **Counterevidence and test gap:** The tuple protects criterion membership/order, and `describe()` returns fresh dictionaries. Existing tests verify add/remove isolation and returned-description isolation (`tests/test_rubrics.py:23–37`), but never successfully revise a criterion after publication. The invalid-revision tests (`tests/test_rubrics.py:39–49`) do not exercise this path. The documented restriction against callers mutating model fields does not prevent the issue: `Draft.revise()` is a service method.
- **Next action — PROPOSED — NOT RUN:** Record scores of 5/10 and 15/20, then revise the draft’s first name and maximum to 20. Assert the original edition retains its name and maximum and the recorded percentage remains `66.67`; a new edition should reflect the revisions. Copy criterion values when freezing to remove the shared state.

**Scope and limits:** Applied `[supplied method]` using only the inspection tool: **[call count withheld]**, comprising the skill read, file listing, and reads of README, all four exposed package files, and the sole exposed test file. Worked alone; changed no files. **Project code, tests, and builds executed: NONE.** No shell, network, credentials, or other sessions were accessed.

Target was the supplied repository snapshot. Revision and working-tree identity were unavailable because no Git metadata was supplied. Runtime behavior and environment-dependent effects were not assessed; the finding is based on static evidence.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "rubrics/assessment.py", "rubrics/catalog.py", "rubrics/editor.py", "rubrics/__init__.py", "tests/test_rubrics.py"]}

### Public investigation notes before final report

I’ll read the audit skill, then inspect the repository’s contracts, implementation, and tests within the 12-call limit. I’ll work alone and won’t execute code or change files.

