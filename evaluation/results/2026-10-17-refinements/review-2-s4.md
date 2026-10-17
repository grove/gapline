# Case s4

## Source (numbered original lines)

### POLICY.md

```
1: # Workshop worksheet policy
2: 
3: Status: approved product requirements, edition 3.
4: 
5: 1. Only a supervisor-approved template is available for worksheet generation.
6: 2. When a supervisor approves revised task wording, the revised wording must
7:    appear on the next shift worksheet.
8: 3. Supervisors may prepare morning and evening worksheets several days ahead.
9: 4. Each generated worksheet records its template revision. Completed worksheets
10:    are retained as historical records with their original wording and check marks.
11: 5. Only the currently approved revision is offered for new worksheet generation.
12: 6. There may be at most one worksheet for a given date and shift. Generating an
13:    existing date and shift returns that worksheet without erasing operator marks.
14: 7. Approval of an empty template, duplicate task keys, and unknown shift names
15:    must fail without changing existing records.
16: 
17: The desk is used by one supervisor at a time. External identity and long-term
18: storage are supplied by the embedding application.
```

### README.md

```
1: # Shift worksheet desk
2: 
3: An assembly workshop maintains approved inspection templates and generates dated
4: worksheets for morning and evening shifts. Supervisors can prepare worksheets in
5: advance. Operators tick tasks and keep the completed worksheet as the shift record.
6: 
7: The governing product requirements are in `POLICY.md`. `desk/templates.py` stores
8: approved revisions, `desk/worksheets.py` owns generated sheets, and `desk/service.py`
9: coordinates approval and generation. Storage is in memory for a single desk.
10: Public APIs accept ISO date objects, shift names `morning` and `evening`, and named
11: tasks. Generated references are sequential local identifiers. A template's task
12: keys are unique, and worksheets expose task text and revision for operators.
13: 
14: Run `python3 -m unittest discover -s tests -v` from this directory.
```

### desk/__init__.py

```

```

### desk/service.py

```
1: from .templates import Templates
2: from .worksheets import Worksheets
3: 
4: 
5: class Desk:
6:     def __init__(self):
7:         self.templates = Templates()
8:         self.worksheets = Worksheets()
9: 
10:     def approve(self, tasks):
11:         return self.templates.approve(tasks)
12: 
13:     def prepare(self, day, shift):
14:         return self.worksheets.generate(day, shift, self.templates.current())
15: 
16:     def mark(self, day, shift, task):
17:         self.worksheets.mark(day, shift, task)
18: 
19:     def finish(self, day, shift):
20:         self.worksheets.finish(day, shift)
21: 
22:     def view(self, day, shift):
23:         return self.worksheets.view(day, shift)
```

### desk/templates.py

```
1: from dataclasses import dataclass
2: 
3: 
4: @dataclass(frozen=True)
5: class Template:
6:     revision: int
7:     tasks: tuple[tuple[str, str], ...]
8: 
9: 
10: class Templates:
11:     def __init__(self):
12:         self._approved = None
13:         self._next_revision = 1
14: 
15:     def approve(self, tasks):
16:         tasks = tuple((key, text) for key, text in tasks)
17:         if not tasks or any(not key.strip() or not text.strip() for key, text in tasks):
18:             raise ValueError('named tasks are required')
19:         if len({key for key, text in tasks}) != len(tasks):
20:             raise ValueError('duplicate task key')
21:         self._approved = Template(self._next_revision, tasks)
22:         self._next_revision += 1
23:         return self._approved.revision
24: 
25:     def current(self):
26:         if self._approved is None:
27:             raise ValueError('no approved template')
28:         return self._approved
```

### desk/worksheets.py

```
1: from dataclasses import dataclass, field
2: 
3: 
4: @dataclass
5: class Worksheet:
6:     reference: int
7:     day: object
8:     shift: str
9:     revision: int
10:     tasks: tuple[tuple[str, str], ...]
11:     checked: set[str] = field(default_factory=set)
12:     complete: bool = False
13: 
14: 
15: class Worksheets:
16:     def __init__(self):
17:         self._items = {}
18: 
19:     def generate(self, day, shift, template):
20:         if shift not in ('morning', 'evening'):
21:             raise ValueError('unknown shift')
22:         key = (day, shift)
23:         if key not in self._items:
24:             self._items[key] = Worksheet(
25:                 len(self._items) + 1, day, shift, template.revision, template.tasks
26:             )
27:         return self.view(day, shift)
28: 
29:     def mark(self, day, shift, task):
30:         sheet = self._items[(day, shift)]
31:         if sheet.complete:
32:             raise ValueError('worksheet is complete')
33:         if task not in dict(sheet.tasks):
34:             raise KeyError(task)
35:         sheet.checked.add(task)
36: 
37:     def finish(self, day, shift):
38:         sheet = self._items[(day, shift)]
39:         if sheet.checked != set(dict(sheet.tasks)):
40:             raise ValueError('worksheet has unchecked tasks')
41:         sheet.complete = True
42: 
43:     def view(self, day, shift):
44:         sheet = self._items[(day, shift)]
45:         return {
46:             'reference': sheet.reference, 'day': day, 'shift': shift,
47:             'revision': sheet.revision, 'tasks': sheet.tasks,
48:             'checked': frozenset(sheet.checked), 'complete': sheet.complete,
49:         }
```

### tests/test_desk.py

```
1: import unittest
2: from datetime import date, timedelta
3: from desk.service import Desk
4: 
5: 
6: class DeskTests(unittest.TestCase):
7:     def setUp(self):
8:         self.day = date(2026, 6, 9)
9:         self.desk = Desk()
10:         self.revision = self.desk.approve([('guard', 'Inspect guard'), ('lamp', 'Check lamp')])
11: 
12:     def test_generation_uses_approved_revision(self):
13:         sheet = self.desk.prepare(self.day, 'morning')
14:         self.assertEqual(sheet['revision'], self.revision)
15:         self.assertEqual(sheet['tasks'][0], ('guard', 'Inspect guard'))
16:         self.assertEqual(sheet['checked'], frozenset())
17:         self.assertFalse(sheet['complete'])
18: 
19:     def test_future_generation_uses_updated_wording(self):
20:         revision = self.desk.approve([('guard', 'Inspect and latch guard')])
21:         sheet = self.desk.prepare(self.day + timedelta(days=1), 'morning')
22:         self.assertEqual(sheet['revision'], revision)
23:         self.assertEqual(sheet['tasks'], (('guard', 'Inspect and latch guard'),))
24: 
25:     def test_repeat_generation_keeps_marks_and_distinct_shifts(self):
26:         first = self.desk.prepare(self.day, 'morning')
27:         self.desk.mark(self.day, 'morning', 'guard')
28:         again = self.desk.prepare(self.day, 'morning')
29:         evening = self.desk.prepare(self.day, 'evening')
30:         self.assertEqual(first['reference'], again['reference'])
31:         self.assertEqual(again['checked'], frozenset({'guard'}))
32:         self.assertNotEqual(first['reference'], evening['reference'])
33:         self.assertFalse(evening['checked'])
34: 
35:     def test_completion_preserves_history(self):
36:         original = self.desk.prepare(self.day, 'morning')
37:         with self.assertRaises(ValueError):
38:             self.desk.finish(self.day, 'morning')
39:         for task in ('guard', 'lamp'):
40:             self.desk.mark(self.day, 'morning', task)
41:         self.desk.finish(self.day, 'morning')
42:         self.desk.approve([('guard', 'New wording')])
43:         historical = self.desk.view(self.day, 'morning')
44:         self.assertEqual(historical['tasks'], original['tasks'])
45:         self.assertEqual(historical['revision'], original['revision'])
46:         with self.assertRaises(ValueError):
47:             self.desk.mark(self.day, 'morning', 'guard')
48: 
49:     def test_invalid_actions_do_not_change_approval(self):
50:         for tasks in ([], [('x', '')], [('x', 'A'), ('x', 'B')]):
51:             with self.assertRaises(ValueError):
52:                 self.desk.approve(tasks)
53:         self.assertEqual(self.desk.prepare(self.day, 'morning')['revision'], self.revision)
54:         with self.assertRaises(ValueError):
55:             self.desk.prepare(self.day, 'night')
56:         with self.assertRaises(KeyError):
57:             self.desk.mark(self.day, 'morning', 'unknown')
58:         with self.assertRaises(ValueError):
59:             Desk().prepare(self.day, 'morning')
60: 
61: 
62: if __name__ == '__main__':
63:     unittest.main()
```

## Frozen evaluator interpretation (nonexhaustive; challenge if wrong)

{
  "contracts": [
    {
      "path": "POLICY.md",
      "exact": "When a supervisor approves revised task wording, the revised wording must\n   appear on the next shift worksheet.",
      "start_line": 6
    },
    {
      "path": "POLICY.md",
      "exact": "Supervisors may prepare morning and evening worksheets several days ahead.",
      "start_line": 8
    },
    {
      "path": "POLICY.md",
      "exact": "Only the currently approved revision is offered for new worksheet generation.",
      "start_line": 11
    },
    {
      "path": "POLICY.md",
      "exact": "Generating an\n   existing date and shift returns that worksheet without erasing operator marks.",
      "start_line": 12
    }
  ],
  "expected_interpretation": "Observed: worksheets snapshot a template at generation; later approval updates only the current template, so an already prepared upcoming worksheet keeps older wording, while a newly generated worksheet gets the new revision. POLICY item 2 does not define whether next means next chronological shift (including a prepared sheet) or next newly generated worksheet. Items 3, 5, and 6 do not conclusively settle whether uncompleted prepared sheet wording should refresh. Preserve the ambiguity and seek that decision before declaring a runtime fix.",
  "accepted_alternatives": [
    "An explicitly conditional finding describing the prepare -> approve -> next shift scenario and the two plausible readings, with a focused clarification request.",
    "A requirement gap or uncertainty note rather than a confirmed implementation bug.",
    "No confirmed runtime finding with an explanation that the prepared-sheet interpretation is unresolved."
  ],
  "criteria": {
    "useful_probes": [
      "Connect Templates.approve, Desk.prepare, Worksheets.generate, and the stored revision/tasks.",
      "Read all seven policy clauses, including advance preparation, historical completion, and idempotent existing-sheet generation.",
      "Ask whether revised wording must refresh already prepared but uncompleted upcoming worksheets and how operator marks are preserved."
    ],
    "false_positives": [
      "Unequivocally declaring stale upcoming sheets a bug without acknowledging next is undefined.",
      "Claiming policy unambiguously requires every prepared sheet to retain old wording.",
      "Proposing rewriting completed historical records.",
      "Treating the existing future-generation test as proof that approvals refresh previously prepared sheets."
    ],
    "uncertainty": "Required: separate proven snapshot behavior from uncertain intended approval scope. Do not resolve it by assuming unstated requirements.",
    "verification": "A prepare-before-approve sequence proves behavior, not authorial intent. The oracle deliberately does not assert either requirement interpretation is correct."
  }
}

## Report r02

One supported finding.

[Telemetry line withheld for blind review.]

**Project code, tests, and builds executed: NONE.** No files changed, credentials read, or network tools used.

### F1 — Prepared upcoming worksheets retain superseded wording

**SUPPORTED · Medium impact · Contract/implementation and test-protection gap**

**Expected:** Revised wording must appear on the next shift worksheet (`POLICY.md:6–7`), while supervisors may prepare worksheets several days ahead (`POLICY.md:8`).

**Source-observed behavior:** Approval only replaces the current template (`desk/service.py:10–11`, `desk/templates.py:21–23`). Worksheets capture wording and revision when first generated; generating an existing date/shift never updates either (`desk/worksheets.py:19–27`). Consequently, preparing tomorrow’s worksheet, approving revised wording, and preparing tomorrow’s worksheet again returns the earlier wording. Approval also leaves that worksheet unchanged when viewed directly.

**Test protection:** `tests/test_desk.py:19–23` approves revised wording **before** creating the future worksheet. Repeat-generation assertions cover references and marks (`tests/test_desk.py:25–33`), but do not introduce an intervening approval. Neither protects the interaction above.

**Counterevidence and uncertainty:** Policy requires repeat generation to preserve the worksheet and operator marks (`POLICY.md:12–13`), and completed records must retain original wording (`POLICY.md:9–10`); the historical-wording test supports that distinction (`tests/test_desk.py:35–47`). Those requirements constrain any refresh mechanism. The policy does not explicitly define how approval affects unfinished, already-prepared worksheets, especially partially checked ones. Thus, the stale-wording path is established by source inspection; its intended resolution needs clarification. No runtime failure was reproduced.

**Next action:** Define how the “next shift” promise applies to prepared worksheets, preserving completed history and existing marks.

**PROPOSED — NOT RUN:** Prepare an untouched future worksheet under revision 1, approve revision 2 with the same task key and changed wording, then view and prepare that date/shift again. The source predicts revision 1 wording throughout. If the next-shift promise includes prepared worksheets, assert revision 2 wording while retaining the reference; document any intended exception.

**Limits and outcome:** One finding survives review. All supplied application and test source was inspected, but embedding-application behavior, persistence, and runtime behavior were not assessed. No broader claim of correctness or test coverage is implied.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "POLICY.md", "desk/service.py", "desk/templates.py", "desk/worksheets.py", "desk/__init__.py", "tests/test_desk.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace documented contracts through implementation and tests. I’ll work alone and won’t change files or execute project code.

The main gap is at the approval/preparation boundary: approval replaces the current template, but worksheets prepared ahead retain their old wording. The tests cover revised wording on a newly created worksheet and preservation of completed history; they don’t cover approval after a future worksheet has already been prepared. I’m treating the policy’s “next shift worksheet” wording as the relevant promise, while noting that it leaves the treatment of partially checked worksheets unclear.

## Report r11

One supported gap emerged: approving revised wording leaves already prepared upcoming worksheets on the old revision. Whether that violates the intended policy needs clarification.

**F1 — Advance preparation can prevent revised wording from reaching the next shift.**  
Category: contract integration and test protection. Evidence: **SUPPORTED**, source inspection only. Impact: operators may receive outdated inspection instructions.

- **Expected:** `POLICY.md:6–8` requires revised wording on the next shift worksheet and permits preparing worksheets several days ahead.
- **Implementation:** `Desk.approve()` only updates the approved template (`desk/service.py:10–11`, `desk/templates.py:21–22`). Although `Desk.prepare()` passes the current template (`desk/service.py:13–14`), `Worksheets.generate()` uses it only when the date/shift has no existing worksheet (`desk/worksheets.py:22–27`). Thus, preparing an upcoming shift, approving revised wording, and preparing that shift again retains its original wording and revision.
- **Test protection:** `tests/test_desk.py:19–23` checks revised wording only for a newly generated worksheet. Repeat generation is tested without an intervening approval (`tests/test_desk.py:25–33`). Neither covers this interaction.
- **Counterevidence and uncertainty:** `POLICY.md:12–13` explicitly requires returning an existing worksheet without erasing marks; the implementation satisfies that rule. Completed records must also retain original wording (`POLICY.md:9–10`), and `tests/test_desk.py:35–47` protects their wording and revision. The policy does not resolve how revised wording should affect an existing, incomplete worksheet. This supports an unresolved contract interaction, rather than an unqualified implementation defect.
- **Next action:** clarify whether approval must update already prepared, incomplete worksheets, including how marks survive task changes. **PROPOSED — NOT RUN:** add a regression covering prepare → approve revised wording → prepare the same upcoming shift, asserting the agreed wording, revision, reference, and mark behavior.

[Telemetry line withheld for blind review.]

The target was the supplied repository snapshot. No Git metadata was supplied, so revision and working-tree identity remain unknown. Runtime behavior and embedding-application guarantees were not assessed. This bounded source audit produced **one supported finding**, not a repository-wide correctness conclusion.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "POLICY.md", "desk/service.py", "desk/templates.py", "desk/worksheets.py", "desk/__init__.py", "tests/test_desk.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace documented contracts through the implementation and tests. I’ll work alone, make no changes, and report only findings supported by concrete evidence.

## Report r17

Audited the supplied “Shift worksheet desk” snapshot using `[supplied method]`. **One supported finding** survived review.

**F1 — Revised wording does not reach an already prepared next-shift worksheet**  
**SUPPORTED · Medium impact · Cross-operation contract gap**

- **Expected:** `POLICY.md:6–8` requires approved revised wording on the next shift worksheet and permits preparing worksheets days ahead.
- **Source behavior:** Approval only replaces the current template (`desk/service.py:10–11`, `desk/templates.py:21–23`). Existing worksheets retain their captured revision and tasks: `desk/worksheets.py:23–27` only initializes absent date/shift keys. Consequently, preparing tomorrow’s worksheet, approving revised wording, then preparing tomorrow’s worksheet again returns the old wording. No inspected path refreshes it.
- **Consequence:** Operators could receive superseded instructions on the next shift despite supervisor approval.
- **Test protection:** `tests/test_desk.py:19–23` checks revised wording only when generation happens after approval. The repeat-generation test (`25–33`) exercises no intervening approval. Neither protects the advance-preparation sequence.
- **Counterevidence and uncertainty:** `POLICY.md:12–13` requires returning an existing worksheet while preserving marks, and `9–10` protects completed history. These requirements justify preserving identity, marks, and completed records; they do not explicitly resolve wording changes on unfinished, advance-prepared sheets. The implementation’s behavior is supported by source inspection, but the intended reconciliation needs clarification. No runtime failure was reproduced.
- **Next action:** Define how approval affects unfinished worksheets prepared in advance, including partially checked ones. **PROPOSED — NOT RUN:** Prepare tomorrow’s morning worksheet under revision A, approve revision B with the same task keys and revised wording, then prepare and view that worksheet. Check wording, revision, reference, and marks against the clarified policy. The inspected implementation predicts A remains; automatic refresh or explicit invalidation would refute that prediction.

Other examined leads did not support additional findings: template validation precedes approval-state changes (`desk/templates.py:16–22`), and completed worksheets retain captured wording while rejecting further marks (`desk/worksheets.py:25`, `31–32`).

[Telemetry line withheld for blind review.]

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "POLICY.md", "desk/service.py", "desk/worksheets.py", "desk/templates.py", "desk/__init__.py", "tests/test_desk.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace a few consequential contracts through implementation and tests. I’ll work alone, make no changes, and stay within the 12-call limit.

## Report r18

Found one supported gap, with a policy ambiguity that affects the remedy.

[Telemetry line withheld for blind review.]

**Project code, tests, and builds executed: NONE.** No files changed; no network access used.

**F1 — Revised wording does not reach an already-prepared next-shift worksheet**  
**SUPPORTED · Medium impact · Contract/implementation and test protection**

- **Expected:** [POLICY.md:6](POLICY.md#L6) requires revised wording on the next shift worksheet, while [POLICY.md:8](POLICY.md#L8) permits preparing worksheets several days ahead.
- **Source behavior:** Approval only replaces the current template ([desk/templates.py:21](desk/templates.py#L21)). Although preparation passes that template to generation ([desk/service.py:14](desk/service.py#L14)), an existing date/shift bypasses worksheet creation and returns its stored revision and wording ([desk/worksheets.py:23](desk/worksheets.py#L23), [desk/worksheets.py:47](desk/worksheets.py#L47)). Thus, the source path “prepare tomorrow → approve revised wording → prepare tomorrow again” retains the old wording, even when the sheet is unfinished and unmarked.
- **Test gap:** The future-wording test approves before first preparing the sheet ([tests/test_desk.py:19](tests/test_desk.py#L19)). Repeat-generation coverage checks marks without an intervening approval ([tests/test_desk.py:25](tests/test_desk.py#L25)). Neither distinguishes this sequence.
- **Counterevidence and uncertainty:** [POLICY.md:12](POLICY.md#L12) requires returning the existing worksheet without erasing marks, and completed records must retain original wording ([POLICY.md:9](POLICY.md#L9)); completed-history preservation is tested. These constrain any fix. The policy does not explicitly resolve whether “next shift worksheet” includes one already prepared. Retaining old wording is established by source inspection; declaring it unconditionally incorrect would overstate the requirement.
- **Next action:** Resolve how approval should affect unfinished, pre-generated sheets, including marked sheets. **PROPOSED — NOT RUN:** Add a regression scenario that prepares a future sheet, revises its wording, then prepares/views it again and checks the agreed wording, revision, identity, and mark-preservation behavior.

No additional supported findings emerged. This review covered all exposed application and test source, but assessed neither runtime behavior nor the embedding application’s identity/storage guarantees. The result does not establish that the repository is defect-free.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "POLICY.md", "desk/service.py", "desk/templates.py", "desk/worksheets.py", "desk/__init__.py", "tests/test_desk.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace documented contracts into implementation and test coverage. I’ll work alone, leave files unchanged, and stay within the inspection limits.
The main gap concerns worksheets prepared ahead of time: approval changes the current template, but existing worksheets retain their old wording. The tests cover future worksheets created after approval and preservation of completed records; they do not cover an unfinished worksheet prepared before approval. I’m weighing that against the policy requiring repeat generation to preserve the existing worksheet and its marks.
