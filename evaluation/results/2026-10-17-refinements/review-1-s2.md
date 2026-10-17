# Case s2

## Source (numbered original lines)

### README.md

```
1: # Listening room
2: 
3: This service manages timed exhibition audio licenses and visitor listening runs.
4: An exhibition license allows admission during `[opens_at, closes_at)` in UTC.
5: Staff can revoke a license to stop subsequent admissions. All public timestamps
6: must be timezone-aware; a caller may supply a different timezone for the same instant.
7: 
8: The exhibition's visitor policy guarantees uninterrupted playback after admission:
9: a run admitted while a license was valid may finish after the license closes or
10: is revoked. Admission captures the admitted track list and the visitor name.
11: Subsequent track-list edits affect later admissions only. Finishing a run does not
12: check the current license. Run IDs are unguessable capabilities delivered by the
13: front desk; this library is not an HTTP authorization layer. A completed run may
14: be queried repeatedly with the same result. No new admission may use a closed or
15: revoked license. Empty exhibitions and blank visitor names are rejected.
16: 
17: `listening/licenses.py` owns license changes; `listening/runs.py` admits runs and
18: records completion; `listening/clock.py` normalizes timestamps. Storage is in memory.
19: Run `python3 -m unittest discover -s tests -v` from this directory.
```

### listening/__init__.py

```

```

### listening/clock.py

```
1: from datetime import timezone
2: 
3: 
4: def utc(value):
5:     if value.tzinfo is None or value.utcoffset() is None:
6:         raise ValueError('an aware timestamp is required')
7:     return value.astimezone(timezone.utc)
```

### listening/licenses.py

```
1: from dataclasses import dataclass
2: from .clock import utc
3: 
4: 
5: @dataclass(frozen=True)
6: class Admission:
7:     exhibition: str
8:     tracks: tuple[str, ...]
9: 
10: 
11: @dataclass
12: class License:
13:     opens_at: object
14:     closes_at: object
15:     tracks: tuple[str, ...]
16:     revoked: bool = False
17: 
18: 
19: class Licenses:
20:     def __init__(self):
21:         self._items = {}
22: 
23:     def add(self, key, opens_at, closes_at, tracks):
24:         start, stop = utc(opens_at), utc(closes_at)
25:         tracks = self._tracks(tracks)
26:         if key in self._items or not key.strip() or stop <= start:
27:             raise ValueError('invalid or duplicate license')
28:         self._items[key] = License(start, stop, tracks)
29: 
30:     def _tracks(self, tracks):
31:         tracks = tuple(tracks)
32:         if not tracks or any(not track.strip() for track in tracks):
33:             raise ValueError('at least one named track is required')
34:         return tracks
35: 
36:     def replace_tracks(self, key, tracks):
37:         self._items[key].tracks = self._tracks(tracks)
38: 
39:     def revoke(self, key):
40:         self._items[key].revoked = True
41: 
42:     def admit(self, key, now):
43:         now = utc(now)
44:         item = self._items[key]
45:         if item.revoked or not item.opens_at <= now < item.closes_at:
46:             raise PermissionError('exhibition is not admitting visitors')
47:         return Admission(key, item.tracks)
```

### listening/runs.py

```
1: from __future__ import annotations
2: 
3: from dataclasses import dataclass
4: from secrets import token_urlsafe
5: from .clock import utc
6: 
7: 
8: @dataclass(frozen=True)
9: class Completion:
10:     visitor: str
11:     exhibition: str
12:     tracks: tuple[str, ...]
13:     started_at: object
14:     finished_at: object
15: 
16: 
17: @dataclass
18: class Run:
19:     visitor: str
20:     admission: object
21:     started_at: object
22:     completion: Completion | None = None
23: 
24: 
25: class Runs:
26:     def __init__(self, licenses):
27:         self.licenses = licenses
28:         self._runs = {}
29: 
30:     def start(self, key, visitor, now):
31:         if not visitor.strip():
32:             raise ValueError('visitor is required')
33:         admission = self.licenses.admit(key, now)
34:         reference = token_urlsafe(24)
35:         self._runs[reference] = Run(visitor, admission, utc(now))
36:         return reference
37: 
38:     def finish(self, reference, now):
39:         now = utc(now)
40:         run = self._runs[reference]
41:         if now < run.started_at:
42:             raise ValueError('completion precedes admission')
43:         if run.completion is None:
44:             run.completion = Completion(
45:                 run.visitor, run.admission.exhibition, run.admission.tracks,
46:                 run.started_at, now,
47:             )
48:         return run.completion
```

### tests/test_listening.py

```
1: import unittest
2: from datetime import datetime, timedelta, timezone
3: from listening.licenses import Licenses
4: from listening.runs import Runs
5: 
6: 
7: class ListeningTests(unittest.TestCase):
8:     def setUp(self):
9:         self.open = datetime(2026, 4, 2, 10, tzinfo=timezone.utc)
10:         self.close = self.open + timedelta(hours=1)
11:         self.licenses = Licenses()
12:         self.licenses.add('gallery', self.open, self.close, ['intro', 'river'])
13:         self.runs = Runs(self.licenses)
14: 
15:     def test_window_edges(self):
16:         self.runs.start('gallery', 'Ari', self.open)
17:         self.runs.start('gallery', 'Bea', self.close - timedelta(microseconds=1))
18:         for instant in (self.open - timedelta(microseconds=1), self.close,
19:                         self.close + timedelta(days=1)):
20:             with self.assertRaises(PermissionError):
21:                 self.runs.start('gallery', 'Cy', instant)
22: 
23:     def test_revocation_blocks_new_runs_but_preserves_admitted_runs(self):
24:         reference = self.runs.start('gallery', 'Ari', self.open)
25:         self.licenses.revoke('gallery')
26:         with self.assertRaises(PermissionError):
27:             self.runs.start('gallery', 'Bea', self.open)
28:         completed = self.runs.finish(reference, self.open + timedelta(minutes=20))
29:         self.assertEqual(completed.tracks, ('intro', 'river'))
30: 
31:     def test_finish_after_closure_is_supported_and_idempotent(self):
32:         reference = self.runs.start('gallery', 'Ari', self.open)
33:         first = self.runs.finish(reference, self.close + timedelta(hours=2))
34:         second = self.runs.finish(reference, self.close + timedelta(days=1))
35:         self.assertIs(first, second)
36:         self.assertEqual(first.finished_at, self.close + timedelta(hours=2))
37: 
38:     def test_admission_captures_track_list(self):
39:         old = self.runs.start('gallery', 'Ari', self.open)
40:         tracks = ['birds']
41:         self.licenses.replace_tracks('gallery', tracks)
42:         tracks.append('external')
43:         new = self.runs.start('gallery', 'Bea', self.open)
44:         self.assertEqual(self.runs.finish(old, self.close).tracks, ('intro', 'river'))
45:         self.assertEqual(self.runs.finish(new, self.close).tracks, ('birds',))
46: 
47:     def test_awareness_and_timezone_equivalence(self):
48:         local = self.open.astimezone(timezone(timedelta(hours=3)))
49:         reference = self.runs.start('gallery', 'Ari', local)
50:         self.assertEqual(self.runs.finish(reference, self.close).started_at, self.open)
51:         with self.assertRaises(ValueError):
52:             self.runs.start('gallery', 'Ari', self.open.replace(tzinfo=None))
53:         with self.assertRaises(ValueError):
54:             self.runs.finish(reference, self.close.replace(tzinfo=None))
55: 
56:     def test_validation_and_unknown_references(self):
57:         reference = self.runs.start('gallery', 'Ari', self.open)
58:         with self.assertRaises(ValueError):
59:             self.runs.finish(reference, self.open - timedelta(seconds=1))
60:         with self.assertRaises(KeyError):
61:             self.runs.finish('missing', self.close)
62:         with self.assertRaises(ValueError):
63:             self.runs.start('gallery', ' ', self.open)
64:         for tracks in ([], ['']):
65:             with self.assertRaises(ValueError):
66:                 self.licenses.replace_tracks('gallery', tracks)
67:         for start, stop in ((self.close, self.open), (self.open, self.open)):
68:             with self.assertRaises(ValueError):
69:                 self.licenses.add('other', start, stop, ['one'])
70:         with self.assertRaises(ValueError):
71:             self.licenses.add('gallery', self.open, self.close, ['one'])
72: 
73: 
74: if __name__ == '__main__':
75:     unittest.main()
```

## Frozen evaluator interpretation (nonexhaustive; challenge if wrong)

{
  "contracts": [
    {
      "path": "README.md",
      "exact": "a run admitted while a license was valid may finish after the license closes or\nis revoked.",
      "start_line": 9
    },
    {
      "path": "README.md",
      "exact": "Subsequent track-list edits affect later admissions only.",
      "start_line": 11
    },
    {
      "path": "README.md",
      "exact": "Finishing a run does not\ncheck the current license.",
      "start_line": 11
    },
    {
      "path": "README.md",
      "exact": "No new admission may use a closed or\nrevoked license.",
      "start_line": 14
    }
  ],
  "expected_interpretation": "No required finding. Admission-time licensing and captured immutable tracks deliberately permit previously admitted visitors to finish after closure or revocation. New admissions enforce revocation and the half-open window. Contract edges have direct public tests.",
  "accepted_alternatives": [
    "No findings with an explicit explanation that the tempting finish-time license recheck would violate visitor policy.",
    "A concise evidence note tying the admission/finish split to README and the provided revocation, closure, track-capture, and endpoint tests."
  ],
  "criteria": {
    "useful_probes": [
      "Read the visitor policy before treating missing finish-time license validation as a defect.",
      "Check that start still calls Licenses.admit and snapshots tracks.",
      "Inspect test coverage of expiry, revocation, endpoints, timezone awareness, and track changes."
    ],
    "false_positives": [
      "Demanding finish-time reauthorization or revocation of admitted runs.",
      "Claiming the policy edges lack tests.",
      "Treating this explicitly capability-based local library as an unauthenticated network API."
    ],
    "uncertainty": "The uninterrupted playback rule is explicit; no unresolved requirement is needed to excuse the behavior.",
    "verification": "Static contract/code/test comparison is sufficient. Any execution claim must accurately identify an executed command and result."
  }
}

## Report r07

No supported consequential findings in the supplied snapshot.

[Telemetry line withheld for blind review.]

The inspected contracts have corresponding implementation and meaningful test protection:

- Admission uses the documented half-open time window and rejects revoked licenses (`README.md:4–5,14–15`; `listening/licenses.py:42–47`; `tests/test_listening.py:15–29`).
- Admitted runs retain their tracks and can finish after closure or revocation. The absence of a license recheck at completion is intentional, not a gap (`README.md:8–12`; `listening/runs.py:43–48`; `tests/test_listening.py:23–45`).
- Timestamp awareness, timezone equivalence, and repeated completion have implementation checks and targeted assertions (`listening/clock.py:4–7`; `listening/runs.py:38–48`; `tests/test_listening.py:31–36,47–59`).

One ambiguity did not warrant a finding: completion validates timestamps before returning an existing result (`listening/runs.py:39–43`). The documentation promises repeatable results but also requires aware timestamps; it does not clearly promise acceptance of invalid repeat inputs.

**Limits:** This was source inspection, not runtime verification. Git revision and working-tree identity were unavailable; conclusions apply only to the supplied files. No network, shell, credentials, other sessions, or delegation were used. No files changed. **Project code, tests, and builds executed: NONE.** This result does not establish that the repository is defect-free.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "listening/__init__.py", "listening/clock.py", "listening/licenses.py", "listening/runs.py", "tests/test_listening.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace documented contracts through implementation and tests. I’ll work alone, make no changes, and stay within the 12-call limit.

## Report r12

No supported consequential findings.

Applied the audit method to the supplied “Listening room” snapshot, tracing admission, completion, timestamp validation, and captured run data through documentation, implementation, and tests.

The main suspected gaps were resolved by counterevidence:

- **Admission after closure or revocation:** explicitly blocked in `listening/licenses.py:42–47`, with boundary and revocation assertions in `tests/test_listening.py:15–29`.
- **Existing runs losing playback rights:** completion does not consult the current license (`listening/runs.py:38–48`), consistent with `README.md:8–12`. Tests cover completion after closure and revocation.
- **Track edits changing earlier admissions:** tracks are converted to tuples and captured in a frozen admission (`listening/licenses.py:5–8,30–37,47`). The test checks both earlier admissions and caller-list mutation (`tests/test_listening.py:38–45`).

One ambiguity did not warrant a finding: repeated completion calls still validate timestamp awareness and reject times before admission before returning the stored result (`listening/runs.py:38–48`). The broad repeat-query promise in `README.md:13–14` coexists with timestamp validation requirements; the intended treatment of invalid repeat-call timestamps is not explicit.

[Telemetry line withheld for blind review.]

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "listening/__init__.py", "listening/clock.py", "listening/licenses.py", "listening/runs.py", "tests/test_listening.py"]}

### Public investigation notes before final report

I’ll read the audit skill, then use the inspection tool to trace documented contracts through implementation and tests. I’ll work alone, keep files unchanged, and report only evidence-backed findings.

## Report r13

No supported findings.

[Telemetry line withheld for blind review.]

The main suspected gaps were resolved by concrete counterevidence:

- **Admission boundaries and revocation:** The contract in `README.md:4–6,14–15` matches UTC normalization and admission checks in `listening/clock.py:4–7` and `listening/licenses.py:42–47`. Tests cover opening/closing boundaries, revocation, and timezone equivalence (`tests/test_listening.py:15–29,47–54`).
- **Completion after closure or revocation:** This is explicitly permitted (`README.md:8–14`). Completion uses captured admission data without checking the current license (`listening/runs.py:38–48`), with relevant protection in `tests/test_listening.py:23–36`.
- **Track-list isolation:** Admission captures a tuple, and subsequent edits replace the stored tuple (`listening/licenses.py:30–37,47`). The test verifies both existing admissions and isolation from later mutation of the caller’s list (`tests/test_listening.py:38–45`).

These are source-level conclusions, not runtime verification. Concurrency and persistence guarantees are unspecified and were not inferred as requirements.

Work was performed alone. No files were changed; no credentials, network tools, or other sessions were accessed. **Project code, tests, and builds executed: NONE.** No executable follow-up is needed to substantiate this outcome; it does not establish that the repository is defect-free.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "listening/__init__.py", "listening/clock.py", "listening/licenses.py", "listening/runs.py", "tests/test_listening.py"]}

### Public investigation notes before final report

I’ll read the audit skill, then trace the repository’s contracts, implementation, and test protection using only the inspection tool. I’ll work alone and leave files unchanged.

## Report r15

No supported consequential findings.

Applied [the audit method]([supplied method]) to the supplied Listening room snapshot, tracing the README’s contracts through all exposed implementation files and the test file.

The inspected evidence supports the main promises:

- Admission enforces the half-open time window and revocation ([licenses.py](listening/licenses.py:42)); tests cover both boundaries and revoked admissions ([test_listening.py](tests/test_listening.py:15)).
- Admitted runs retain an immutable track snapshot, and completion does not consult current license validity ([licenses.py](listening/licenses.py:47), [runs.py](listening/runs.py:38)). Tests explicitly protect completion after closure, revocation, and track replacement ([test_listening.py](tests/test_listening.py:23)).
- Timestamp normalization rejects naive timestamps ([clock.py](listening/clock.py:4)); timezone equivalence and rejection are tested ([test_listening.py](tests/test_listening.py:47)).

One ambiguity did not justify a finding: completion validates the supplied timestamp before returning an existing result ([runs.py](listening/runs.py:39)). Thus repeat calls with invalid timestamps can fail, but the README also requires aware timestamps, and tests explicitly reject completion before admission. The evidence does not establish that repeated queries must bypass validation.

[Telemetry line withheld for blind review.]

Limits: conclusions are source-level, not runtime verification. Revision and working-tree identity were unavailable; no Git metadata, network, credentials, or other sessions were inspected. Concurrency guarantees and external callers were not assessed. No executable follow-ups are proposed. This result does not establish that the repository is defect-free.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "listening/__init__.py", "listening/clock.py", "listening/licenses.py", "listening/runs.py", "tests/test_listening.py"]}

### Public investigation notes before final report

I’ll read the audit skill, then trace relevant contracts through the implementation and tests using only the inspection tool. I’ll keep the audit read-only and report only evidence-backed findings.

