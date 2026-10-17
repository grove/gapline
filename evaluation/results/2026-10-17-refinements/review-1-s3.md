# Case s3

## Source (numbered original lines)

### README.md

```
1: # Field sensor ledger
2: 
3: A local ledger for named sensors with temperature readings. Input readings use
4: Celsius (`C`) or Fahrenheit (`F`); summaries always use Celsius. This is a data
5: preparation utility, not an alerting or safety system.
6: 
7: A reading has a nonblank sensor name, an aware timestamp, and a finite numeric
8: value. Booleans are not numeric values here. The supported sensor range is -273.15 through 1000 C inclusive,
9: or -459.67 through 1832 F inclusive; units are case-sensitive. Values outside
10: these ranges, including arbitrarily large integers, are rejected before conversion. Each `(sensor, instant)` identifies one
11: reading. A later valid submission replaces that reading, including when supplied
12: in a different timezone. Input batches are atomic: one invalid reading leaves the
13: entire ledger unchanged. Empty batches are accepted. Input may arrive out of order.
14: 
15: A summary selects `[start, stop)` instants for exactly one sensor. It returns count,
16: minimum, maximum, and arithmetic mean, or `None` for each statistic when empty.
17: Bounds must be aware and `start < stop`. Stored rows are returned in timestamp order
18: as immutable values. Summaries do not round results; display rounding is a caller's
19: choice. Ordinary floating-point tolerance applies to conversion comparisons.
20: 
21: `fieldlog/reading.py` validates input, `fieldlog/ledger.py` owns storage, and
22: `fieldlog/summary.py` computes window statistics. This in-memory library is single
23: threaded. Run `python3 -m unittest discover -s tests -v` in this directory.
```

### fieldlog/__init__.py

```

```

### fieldlog/ledger.py

```
1: from .reading import parse, instant
2: from .summary import summarize
3: 
4: 
5: class Ledger:
6:     def __init__(self):
7:         self._rows = {}
8: 
9:     def add(self, rows):
10:         parsed = [parse(row) for row in rows]
11:         self._rows.update({(row.sensor, row.at): row for row in parsed})
12: 
13:     def readings(self, sensor):
14:         return tuple(sorted(
15:             (row for row in self._rows.values() if row.sensor == sensor),
16:             key=lambda row: row.at,
17:         ))
18: 
19:     def summary(self, sensor, start, stop):
20:         start, stop = instant(start), instant(stop)
21:         if start >= stop:
22:             raise ValueError('summary window must have positive length')
23:         return summarize(
24:             row.celsius for row in self.readings(sensor)
25:             if start <= row.at < stop
26:         )
```

### fieldlog/reading.py

```
1: from dataclasses import dataclass
2: from datetime import timezone
3: 
4: 
5: def instant(value):
6:     if value.tzinfo is None or value.utcoffset() is None:
7:         raise ValueError('timestamp must be aware')
8:     return value.astimezone(timezone.utc)
9: 
10: 
11: @dataclass(frozen=True)
12: class Reading:
13:     sensor: str
14:     at: object
15:     celsius: float
16: 
17: 
18: def parse(row):
19:     sensor, at, value, unit = row
20:     if not isinstance(sensor, str) or not sensor.strip():
21:         raise ValueError('sensor must be named')
22:     at = instant(at)
23:     if type(value) not in (int, float):
24:         raise ValueError('temperature must be numeric')
25:     if unit == 'F':
26:         lower, upper = -459.67, 1832
27:     elif unit == 'C':
28:         lower, upper = -273.15, 1000
29:     else:
30:         raise ValueError('unit must be C or F')
31:     if not lower <= value <= upper:
32:         raise ValueError('temperature outside supported sensor range')
33:     celsius = (value - 32) * 5 / 9 if unit == 'F' else float(value)
34:     return Reading(sensor, at, celsius)
```

### fieldlog/summary.py

```
1: from __future__ import annotations
2: 
3: from dataclasses import dataclass
4: from math import fsum
5: 
6: 
7: @dataclass(frozen=True)
8: class Summary:
9:     count: int
10:     minimum: float | None
11:     maximum: float | None
12:     mean: float | None
13: 
14: 
15: def summarize(values):
16:     values = tuple(values)
17:     if not values:
18:         return Summary(0, None, None, None)
19:     return Summary(len(values), min(values), max(values), fsum(values) / len(values))
```

### tests/test_fieldlog.py

```
1: import unittest
2: from dataclasses import FrozenInstanceError
3: from datetime import datetime, timedelta, timezone
4: from fieldlog.ledger import Ledger
5: from fieldlog.reading import parse
6: from fieldlog.summary import Summary
7: 
8: 
9: class LedgerTests(unittest.TestCase):
10:     def setUp(self):
11:         self.start = datetime(2026, 5, 1, tzinfo=timezone.utc)
12:         self.stop = self.start + timedelta(days=1)
13:         self.ledger = Ledger()
14: 
15:     def row(self, value, *, sensor='north', at=None, unit='C'):
16:         return sensor, self.start if at is None else at, value, unit
17: 
18:     def test_celsius_fahrenheit_and_absolute_zero(self):
19:         self.assertEqual(parse(self.row(32, unit='F')).celsius, 0)
20:         self.assertEqual(parse(self.row(212, unit='F')).celsius, 100)
21:         self.assertEqual(parse(self.row(-273.15)).celsius, -273.15)
22:         self.assertAlmostEqual(parse(self.row(-459.67, unit='F')).celsius, -273.15)
23: 
24:     def test_invalid_values_names_units_and_time(self):
25:         for value in (True, False, '12', None, float('nan'), float('inf'),
26:                       float('-inf'), -274, 1001, 10**1000, -(10**1000)):
27:             with self.assertRaises(ValueError, msg=repr(value)):
28:                 parse(self.row(value))
29:         for sensor in ('', '  ', 42):
30:             with self.assertRaises(ValueError):
31:                 parse(self.row(10, sensor=sensor))
32:         for unit in ('c', 'K', ''):
33:             with self.assertRaises(ValueError):
34:                 parse(self.row(10, unit=unit))
35:         with self.assertRaises(ValueError):
36:             parse(self.row(10, at=self.start.replace(tzinfo=None)))
37: 
38:     def test_summary_interval_and_sensor_isolation(self):
39:         self.ledger.add([
40:             self.row(99, at=self.start - timedelta(seconds=1)),
41:             self.row(0), self.row(20, at=self.start + timedelta(hours=2)),
42:             self.row(88, at=self.stop), self.row(1000, sensor='south'),
43:         ])
44:         self.assertEqual(self.ledger.summary('north', self.start, self.stop),
45:                          Summary(2, 0, 20, 10))
46:         self.assertEqual(self.ledger.summary('none', self.start, self.stop),
47:                          Summary(0, None, None, None))
48: 
49:     def test_replacement_timezone_equivalence_and_same_batch_last_wins(self):
50:         local = self.start.astimezone(timezone(timedelta(hours=-4)))
51:         self.ledger.add([self.row(1), self.row(2), self.row(32, at=local, unit='F')])
52:         rows = self.ledger.readings('north')
53:         self.assertEqual(len(rows), 1)
54:         self.assertEqual(rows[0].at, self.start)
55:         self.assertEqual(rows[0].celsius, 0)
56:         self.ledger.add([self.row(8)])
57:         self.assertEqual(self.ledger.readings('north')[0].celsius, 8)
58: 
59:     def test_atomic_batches_and_empty_batch(self):
60:         self.ledger.add([self.row(1)])
61:         before = self.ledger.readings('north')
62:         with self.assertRaises(ValueError):
63:             self.ledger.add([self.row(9), self.row(float('nan'), sensor='south')])
64:         self.assertEqual(self.ledger.readings('north'), before)
65:         self.ledger.add([])
66:         self.assertEqual(self.ledger.readings('north'), before)
67: 
68:     def test_order_and_immutable_results(self):
69:         later = self.start + timedelta(hours=1)
70:         self.ledger.add([self.row(20, at=later), self.row(10)])
71:         rows = self.ledger.readings('north')
72:         self.assertEqual([row.at for row in rows], [self.start, later])
73:         with self.assertRaises(FrozenInstanceError):
74:             rows[0].celsius = 999
75:         result = self.ledger.summary('north', self.start, self.stop)
76:         with self.assertRaises(FrozenInstanceError):
77:             result.mean = 999
78: 
79:     def test_supported_upper_bounds_and_large_batch_summary(self):
80:         self.assertEqual(parse(self.row(1000)).celsius, 1000)
81:         self.assertEqual(parse(self.row(1832, unit='F')).celsius, 1000)
82:         for value in (-460, 1833, 1e308, 10**1000):
83:             with self.assertRaises(ValueError):
84:                 parse(self.row(value, unit='F'))
85:         self.ledger.add([
86:             self.row(1000, at=self.start + timedelta(seconds=index))
87:             for index in range(1024)
88:         ])
89:         result = self.ledger.summary('north', self.start, self.stop)
90:         self.assertEqual(result, Summary(1024, 1000, 1000, 1000))
91: 
92:     def test_bad_windows_and_equivalent_timezone_bounds(self):
93:         for start, stop in ((self.stop, self.start), (self.start, self.start),
94:                             (self.start.replace(tzinfo=None), self.stop),
95:                             (self.start, self.stop.replace(tzinfo=None))):
96:             with self.assertRaises(ValueError):
97:                 self.ledger.summary('north', start, stop)
98:         local_start = self.start.astimezone(timezone(timedelta(hours=2)))
99:         self.ledger.add([self.row(12)])
100:         self.assertEqual(self.ledger.summary('north', local_start, self.stop).count, 1)
101: 
102: 
103: if __name__ == '__main__':
104:     unittest.main()
```

## Frozen evaluator interpretation (nonexhaustive; challenge if wrong)

{
  "contracts": [
    {
      "path": "README.md",
      "exact": "Input batches are atomic: one invalid reading leaves the\nentire ledger unchanged.",
      "start_line": 12
    },
    {
      "path": "README.md",
      "exact": "Each `(sensor, instant)` identifies one\nreading.",
      "start_line": 10
    },
    {
      "path": "README.md",
      "exact": "A later valid submission replaces that reading, including when supplied\nin a different timezone.",
      "start_line": 11
    },
    {
      "path": "README.md",
      "exact": "A summary selects `[start, stop)` instants for exactly one sensor.",
      "start_line": 15
    },
    {
      "path": "README.md",
      "exact": "Stored rows are returned in timestamp order\nas immutable values.",
      "start_line": 17
    }
  ],
  "expected_interpretation": "No required finding. Validation occurs before the ledger update; keys use normalized UTC timestamps; summaries use half-open bounds and exact sensor isolation; result values are frozen. Public tests cover the stated contract edges, including invalid second row atomicity, equivalent timezones, bounded magnitudes, arbitrary-size integer rejection, and maximum-value summaries.",
  "accepted_alternatives": [
    "No findings, with a short explanation of the validation/commit boundary and public control coverage.",
    "A bounded conclusion that no consequential gap was substantiated, without claiming universal correctness."
  ],
  "criteria": {
    "useful_probes": [
      "Follow parse normalization into update keys and summary windows.",
      "Inspect a rejected multi-row batch and duplicate replacements, not just happy-path summaries.",
      "Read the test contract edges before suggesting missing tests."
    ],
    "false_positives": [
      "Claiming add partially commits before a later parse error.",
      "Claiming equivalent timezones create duplicate instants.",
      "Demanding duplicate rejection, inclusive stop bounds, rounding, thread safety, alerts, or physical sensor calibration contrary to the declared utility scope.",
      "Generic test-gap findings for already supplied atomicity, conversion, frozen results, sensor isolation, or bound tests."
    ],
    "uncertainty": "State the limited in-memory single-threaded scope; do not manufacture findings from excluded deployment concerns.",
    "verification": "Code and test inspection support a bounded clean result. Runtime execution is optional and must never be fabricated."
  }
}

## Report r01

**No supported findings.** The inspected implementation and tests align with the documented contracts.

I traced three areas and checked counterevidence:

- **Validation and conversion:** [README.md:7](README.md#L7) promises finite, nonboolean values within explicit ranges, checked before conversion. [fieldlog/reading.py:23](fieldlog/reading.py#L23) enforces those constraints before arithmetic. Tests cover invalid values, huge integers, and Celsius/Fahrenheit boundaries ([tests/test_fieldlog.py:18](tests/test_fieldlog.py#L18), [tests/test_fieldlog.py:79](tests/test_fieldlog.py#L79)).
- **Atomic batches and replacement:** [fieldlog/ledger.py:9](fieldlog/ledger.py#L9) parses the complete batch before updating storage. UTC normalization precedes key construction ([fieldlog/reading.py:5](fieldlog/reading.py#L5)). Tests assert rollback and replacement across equivalent timezone representations ([tests/test_fieldlog.py:49](tests/test_fieldlog.py#L49)).
- **Summary selection and immutable results:** Sensor filtering, normalized bounds, and the half-open interval match the documented selection contract ([fieldlog/ledger.py:13](fieldlog/ledger.py#L13)). Statistics use `fsum` ([fieldlog/summary.py:15](fieldlog/summary.py#L15)); tests assert interval boundaries, isolation, empty results, ordering, immutability, and invalid windows ([tests/test_fieldlog.py:38](tests/test_fieldlog.py#L38), [tests/test_fieldlog.py:68](tests/test_fieldlog.py#L68), [tests/test_fieldlog.py:92](tests/test_fieldlog.py#L92)).

[Telemetry line withheld for blind review.]

This conclusion concerns the supplied source snapshot only. Repository revision and working-tree identity were unavailable; runtime behavior and external callers were not assessed. No additional executable follow-up is warranted by a specific unresolved concern from this inspection.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "fieldlog/__init__.py", "fieldlog/ledger.py", "fieldlog/reading.py", "fieldlog/summary.py", "tests/test_fieldlog.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace documented contracts into implementation and tests. I’ll work alone, make no changes, and stay within the 12-call limit.

## Report r03

No supported findings.

Applied the audit method to the supplied Field sensor ledger snapshot, tracing three contract areas:

- **Validation and conversion:** README.md:7–10 agrees with fieldlog/reading.py:18–34. Tests cover invalid values, huge integers, units, and supported endpoints (tests/test_fieldlog.py:18–36, 79–84).
- **Atomicity and reading identity:** Parsing completes before storage changes; timestamps normalize to UTC before keying (fieldlog/ledger.py:9–11; fieldlog/reading.py:5–8). Replacement and atomicity have explicit assertions (tests/test_fieldlog.py:49–66).
- **Summary and immutable results:** Filtering, ordering, empty results, and arithmetic mean match the documented behavior (fieldlog/ledger.py:13–26; fieldlog/summary.py:7–19). Relevant assertions appear in tests/test_fieldlog.py:38–47, 68–100.

[Telemetry line withheld for blind review.]

Limits: conclusions are source-level only. No runtime behavior was reproduced, no Git metadata was supplied, and revision and working-tree identity remain unknown. Test protection for every edge case was not established; the inspected evidence did not justify a consequential finding.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "fieldlog/__init__.py", "fieldlog/ledger.py", "fieldlog/reading.py", "fieldlog/summary.py", "tests/test_fieldlog.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace documented contracts into implementation and test coverage. I’ll work alone, leave files unchanged, and report only findings supported by evidence.

## Report r04

No supported consequential findings.

I applied the audit method to the supplied Field sensor ledger snapshot, tracing three contract areas:

- **Validation and conversion:** documented ranges and rejection rules (`README.md:7–10`) match validation before conversion (`fieldlog/reading.py:18–34`). Tests cover booleans, nonfinite values, enormous integers, and both unit boundaries (`tests/test_fieldlog.py:18–36,79–84`).
- **Atomicity and replacement:** parsing completes before storage changes, and timestamps normalize to UTC before becoming keys (`fieldlog/ledger.py:9–11`; `fieldlog/reading.py:5–8`). Replacement and invalid-batch tests assert resulting state (`tests/test_fieldlog.py:49–66`).
- **Summary semantics:** sensor isolation, half-open windows, ordering, immutable results, and statistics match the documented behavior (`README.md:15–19`; `fieldlog/ledger.py:13–26`; `fieldlog/summary.py:7–19`). Relevant tests check outputs and boundary behavior (`tests/test_fieldlog.py:38–47,68–100`).

Potential concerns about conversion overflow, partial batch updates, and timezone-equivalent duplicate readings were defeated by those implementation details and tests. No remaining lead warranted a finding.

[Telemetry line withheld for blind review.]

**PROPOSED — NOT RUN:** If further assurance is needed, run the existing suite and add a fractional-mean case to directly protect the documented absence of rounding. This is an optional strengthening, not evidence of a defect.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "fieldlog/__init__.py", "fieldlog/ledger.py", "fieldlog/reading.py", "fieldlog/summary.py", "tests/test_fieldlog.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace relevant contracts, implementation, and tests. I’ll work alone and make no changes or execute project code.

## Report r14

No supported consequential findings survived this audit.

[Telemetry line withheld for blind review.]

The documented contracts align with the inspected implementation and test assertions:

- **Validation and atomicity:** range checks precede conversion (`fieldlog/reading.py:23–33`); batches finish parsing before updating storage (`fieldlog/ledger.py:9–11`). Tests assert rejection and preservation of existing readings (`tests/test_fieldlog.py:24–36`, `59–66`, `79–84`).
- **Identity and replacement:** timestamps normalize to UTC before storage keyed by sensor and instant (`fieldlog/reading.py:5–8`, `22`; `fieldlog/ledger.py:11`). Tests cover equivalent timezones and replacement within and across batches (`tests/test_fieldlog.py:49–57`).
- **Summary behavior:** sensor filtering, half-open windows, ordering, empty statistics, and arithmetic mean match the documented behavior (`fieldlog/ledger.py:13–26`; `fieldlog/summary.py:15–19`). Relevant tests assert actual results, including interval boundaries and sensor isolation (`tests/test_fieldlog.py:38–47`, `68–100`).

Potential leads concerning incremental batch mutation, timezone identity, and conversion of oversized integers were defeated by those implementation safeguards and assertions.

**Limits:** This was static inspection through the supplied inspection tool only. Project code, tests, and builds executed: **NONE**. No files changed, network tools used, or credentials accessed. No Git metadata was supplied, so revision and working-tree identity remain unknown. This result establishes source-level consistency within the exposed files, not runtime correctness or freedom from defects.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "fieldlog/__init__.py", "fieldlog/ledger.py", "fieldlog/reading.py", "fieldlog/summary.py", "tests/test_fieldlog.py"]}

### Public investigation notes before final report

I’ll read the audit skill through the inspection tool, then trace documented contracts through the implementation and tests. I’ll work alone, leave files unchanged, and stay within the 12-call limit.

