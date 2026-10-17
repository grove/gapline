# Case s5

## Source (numbered original lines)

### FORMAT.md

```
1: # Geometry format, version 1
2: 
3: This document is the normative compatibility contract for Tile plan.
4: All dimensions and coordinates, including spacing, are whole raster pixels.
5: The CLI `--spacing` argument maps directly to the `spacing_px` layout setting;
6: no physical-unit conversion or DPI parameter is part of version 1.
7: 
8: Count is a nonnegative integer. Width, height, and columns are positive integers.
9: Spacing is a nonnegative integer with default 8. JSON has keys `width`, `height`,
10: and `tiles`. Tiles have integer `index`, `x`, `y`, `width`, and `height` fields.
11: 
12: The used column count is `min(count, columns)`. The number of rows is the ceiling
13: of count divided by columns. Canvas width is the used columns' total thumbnail
14: width plus spacing only between columns. Canvas height uses the corresponding
15: row formula. An incomplete final row retains the earlier rows' canvas width.
16: An empty plan has width 0, height 0, and no tiles. There is no outer padding.
17: 
18: Version 1 is consumed by an existing pixel-coordinate renderer. Implementations
19: must preserve these units, default spacing, ordering, and empty-plan behavior.
```

### README.md

```
1: # Tile plan
2: 
3: Tile plan calculates coordinates for arranging equally sized raster thumbnails.
4: It emits JSON geometry for a separate renderer; it never decodes or resamples images.
5: The normative geometry and compatibility contract is `FORMAT.md`.
6: 
7: Use `python3 -m tileplan.cli --count 5 --width 80 --height 60 --columns 3 --spacing 5`.
8: The result contains the canvas dimensions and one rectangle for each thumbnail.
9: Rectangles follow input order, left to right and then top to bottom.
10: 
11: | Argument | Meaning | Default |
12: | --- | --- | --- |
13: | `--count` | Number of thumbnails | required |
14: | `--width` | Thumbnail width in pixels | required |
15: | `--height` | Thumbnail height in pixels | required |
16: | `--columns` | Maximum thumbnails per row | 3 |
17: | `--spacing` | Horizontal and vertical gap in millimeters | 8 |
18: 
19: For example, `--spacing 5` leaves a 5 mm gap between neighboring thumbnails.
20: There is no outside border. Empty plans produce a zero-sized canvas. Invalid
21: arguments fail before JSON output is written. Standard output is reserved for
22: JSON; command-line usage errors go to standard error.
23: 
24: The README is hand-maintained user documentation. `tileplan/options.py` validates
25: arguments, `tileplan/layout.py` computes geometry, and `tileplan/cli.py` serializes it.
26: Run checks with `python3 -m unittest discover -s tests -v` from this directory.
```

### tests/test_tileplan.py

```
1: import io
2: import json
3: import unittest
4: from contextlib import redirect_stdout, redirect_stderr
5: from tileplan.options import Options
6: from tileplan.layout import arrange
7: from tileplan.cli import main
8: 
9: 
10: class TileTests(unittest.TestCase):
11:     def test_full_rows_and_partial_row(self):
12:         plan = arrange(Options(5, 80, 60, 3, 5))
13:         self.assertEqual((plan.width, plan.height), (250, 125))
14:         self.assertEqual([(tile.x, tile.y) for tile in plan.tiles],
15:                          [(0, 0), (85, 0), (170, 0), (0, 65), (85, 65)])
16:         self.assertEqual([tile.index for tile in plan.tiles], list(range(5)))
17:         self.assertTrue(all((tile.width, tile.height) == (80, 60) for tile in plan.tiles))
18: 
19:     def test_no_extra_columns_or_border(self):
20:         plan = arrange(Options(2, 10, 20, 9, 3))
21:         self.assertEqual((plan.width, plan.height), (23, 20))
22:         single = arrange(Options(1, 10, 20, 9, 100))
23:         self.assertEqual((single.width, single.height), (10, 20))
24: 
25:     def test_empty_default_and_zero_spacing(self):
26:         empty = arrange(Options(0, 10, 20))
27:         self.assertEqual((empty.width, empty.height, empty.tiles), (0, 0, ()))
28:         default = arrange(Options(4, 10, 20))
29:         self.assertEqual((default.width, default.height), (46, 48))
30:         touching = arrange(Options(4, 10, 20, 2, 0))
31:         self.assertEqual((touching.width, touching.height), (20, 40))
32: 
33:     def test_invalid_values(self):
34:         for values in ((-1, 10, 20, 3, 8), (1, 0, 20, 3, 8),
35:                        (1, 10, -1, 3, 8), (1, 10, 20, 0, 8),
36:                        (1, 10, 20, 3, -1), (True, 10, 20, 3, 8),
37:                        (1, 10.0, 20, 3, 8)):
38:             with self.assertRaises(ValueError):
39:                 Options(*values)
40: 
41:     def test_cli_pixel_geometry(self):
42:         output = io.StringIO()
43:         with redirect_stdout(output):
44:             main(['--count', '2', '--width', '10', '--height', '20', '--spacing', '5'])
45:         result = json.loads(output.getvalue())
46:         self.assertEqual(result['width'], 25)
47:         self.assertEqual(result['tiles'][1]['x'], 15)
48:         self.assertEqual(result['tiles'][0]['width'], 10)
49: 
50:     def test_cli_defaults_and_failure_streams(self):
51:         output, errors = io.StringIO(), io.StringIO()
52:         with redirect_stdout(output):
53:             main(['--count', '2', '--width', '10', '--height', '20'])
54:         self.assertEqual(json.loads(output.getvalue())['width'], 28)
55:         output = io.StringIO()
56:         with redirect_stdout(output), redirect_stderr(errors):
57:             with self.assertRaises(SystemExit) as failure:
58:                 main(['--count', '-1', '--width', '10', '--height', '20'])
59:         self.assertEqual(failure.exception.code, 2)
60:         self.assertEqual(output.getvalue(), '')
61:         self.assertIn('nonnegative', errors.getvalue())
62: 
63: 
64: if __name__ == '__main__':
65:     unittest.main()
```

### tileplan/__init__.py

```

```

### tileplan/cli.py

```
1: import argparse
2: from dataclasses import asdict
3: import json
4: from .layout import arrange
5: from .options import Options
6: 
7: 
8: def parser():
9:     result = argparse.ArgumentParser(description='Calculate raster thumbnail coordinates')
10:     for name in ('count', 'width', 'height'):
11:         result.add_argument('--' + name, type=int, required=True)
12:     result.add_argument('--columns', type=int, default=3)
13:     result.add_argument('--spacing', type=int, default=8, help='gap in pixels')
14:     return result
15: 
16: 
17: def main(argv=None):
18:     command = parser()
19:     args = command.parse_args(argv)
20:     try:
21:         options = Options(args.count, args.width, args.height, args.columns, args.spacing)
22:     except ValueError as error:
23:         command.error(str(error))
24:     print(json.dumps(asdict(arrange(options))))
25: 
26: 
27: if __name__ == '__main__':
28:     main()
```

### tileplan/layout.py

```
1: from dataclasses import dataclass
2: 
3: 
4: @dataclass(frozen=True)
5: class Tile:
6:     index: int
7:     x: int
8:     y: int
9:     width: int
10:     height: int
11: 
12: 
13: @dataclass(frozen=True)
14: class Plan:
15:     width: int
16:     height: int
17:     tiles: tuple[Tile, ...]
18: 
19: 
20: def arrange(options):
21:     if options.count == 0:
22:         return Plan(0, 0, ())
23:     columns = min(options.count, options.columns)
24:     rows = (options.count + options.columns - 1) // options.columns
25:     width = columns * options.width + (columns - 1) * options.spacing_px
26:     height = rows * options.height + (rows - 1) * options.spacing_px
27:     tiles = []
28:     for index in range(options.count):
29:         row, column = divmod(index, options.columns)
30:         tiles.append(Tile(
31:             index,
32:             column * (options.width + options.spacing_px),
33:             row * (options.height + options.spacing_px),
34:             options.width,
35:             options.height,
36:         ))
37:     return Plan(width, height, tuple(tiles))
```

### tileplan/options.py

```
1: from dataclasses import dataclass
2: 
3: 
4: @dataclass(frozen=True)
5: class Options:
6:     count: int
7:     width: int
8:     height: int
9:     columns: int = 3
10:     spacing_px: int = 8
11: 
12:     def __post_init__(self):
13:         for name in ('count', 'width', 'height', 'columns', 'spacing_px'):
14:             if type(getattr(self, name)) is not int:
15:                 raise ValueError(f'{name} must be an integer')
16:         if self.count < 0 or self.spacing_px < 0:
17:             raise ValueError('count and spacing must be nonnegative')
18:         if self.width <= 0 or self.height <= 0 or self.columns <= 0:
19:             raise ValueError('width, height, and columns must be positive')
```

## Frozen evaluator interpretation (nonexhaustive; challenge if wrong)

{
  "contracts": [
    {
      "path": "FORMAT.md",
      "exact": "This document is the normative compatibility contract for Tile plan.",
      "start_line": 3
    },
    {
      "path": "FORMAT.md",
      "exact": "All dimensions and coordinates, including spacing, are whole raster pixels.",
      "start_line": 4
    },
    {
      "path": "FORMAT.md",
      "exact": "no physical-unit conversion or DPI parameter is part of version 1.",
      "start_line": 6
    },
    {
      "path": "README.md",
      "exact": "| `--spacing` | Horizontal and vertical gap in millimeters | 8 |",
      "start_line": 17
    },
    {
      "path": "README.md",
      "exact": "For example, `--spacing 5` leaves a 5 mm gap between neighboring thumbnails.",
      "start_line": 19
    }
  ],
  "expected_interpretation": "README spacing table and explanatory example contradict the normative pixel format, CLI help, integer spacing_px setting, direct pixel arithmetic, and tests. Correct the hand-maintained README table and example to pixels. Runtime conversion or a DPI option would break the declared version-1 compatibility contract and is outside this correction.",
  "accepted_alternatives": [
    "One documentation finding identifying both README claims and directing correction to their source.",
    "A docs-only actionable issue supported by FORMAT.md and direct CLI-to-layout mapping, without running the program."
  ],
  "criteria": {
    "useful_probes": [
      "Compare README units to normative FORMAT.md, CLI help, Options.spacing_px, and coordinate arithmetic.",
      "Identify the table and prose example as two occurrences of one documentation root cause."
    ],
    "false_positives": [
      "Changing runtime geometry to millimeters or introducing DPI conversion.",
      "Calling a doc-only contradiction an unverified runtime failure.",
      "Claiming README is generated or advising edits to a nonexistent generator.",
      "Requiring runtime execution before accepting the direct source contradiction."
    ],
    "uncertainty": "Authority is explicit. Do not preserve a false pixels-versus-millimeters ambiguity after reading FORMAT.md.",
    "verification": "No runtime needed: document authority plus direct source mapping proves the contradiction. State any unexecuted tests honestly; testing is not a gate for this docs-only conclusion."
  }
}

## Report r05

One finding survived inspection.

**G1 — README gives incompatible spacing units**  
**Documentation drift · DEMONSTRATED · Medium impact**

- **Expected:** The normative contract specifies whole raster pixels and explicitly excludes physical-unit conversion or DPI (`FORMAT.md:3–6`, `18–19`).
- **Observed:** The README describes `--spacing` as millimeters and promises that `--spacing 5` produces a 5 mm gap (`README.md:17–19`). The CLI instead passes the integer directly into `spacing_px` (`tileplan/cli.py:21`), which is added directly to pixel coordinates (`tileplan/layout.py:25–26`, `32–33`). Users following the README could therefore choose incorrect spacing for their intended physical output.
- **Counterevidence and test protection:** The README identifies `FORMAT.md` as normative (`README.md:5`); CLI help correctly says pixels (`tileplan/cli.py:13`). Tests explicitly assert pixel geometry for spacing 5 (`tests/test_tileplan.py:41–48`). These support the implementation and locate the contradiction in the README. Runtime behavior was not executed.
- **Next action:** Correct the README table and example to say pixels. Preserve the version 1 implementation and its existing pixel assertions.

[Telemetry line withheld for blind review.]

Target: the supplied `tileplan` snapshot. Revision and working-tree identity were unavailable; no Git metadata was inspected. This was static inspection only, so runtime behavior and external renderer integration remain unverified. No files were changed; no network, credentials, or other sessions were accessed. **Project code, tests, and builds executed: NONE.**

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "FORMAT.md", "tileplan/options.py", "tileplan/layout.py"]}
- {"operation": "read", "paths": ["tileplan/cli.py", "tileplan/__init__.py", "tests/test_tileplan.py"]}

### Public investigation notes before final report

I’ll read the audit method, then trace the documented contracts through implementation and tests using only the inspection tool. I won’t execute code or change files.

## Report r09

One supported finding: the README gives spacing units that contradict the normative format and implementation.

**G1 — Incorrect spacing units in user documentation**  
**Category:** documentation drift. **Evidence:** DEMONSTRATED source contradiction. **Impact:** Medium; users following the README can produce an unintended physical gap.

- **Expected:** [README.md:17](README.md#L17) describes spacing in millimeters; [README.md:19](README.md#L19) explicitly promises that `--spacing 5` leaves a 5 mm gap.
- **Observed in source:** [FORMAT.md:3–6](FORMAT.md#L3) establishes the normative contract: spacing is whole raster pixels, with no DPI conversion. [cli.py:13](tileplan/cli.py#L13) labels the option in pixels, [cli.py:21](tileplan/cli.py#L21) passes it directly into `Options`, and [layout.py:32–33](tileplan/layout.py#L32) uses it directly in coordinate arithmetic.
- **Counterevidence and test protection:** [test_tileplan.py:41–48](tests/test_tileplan.py#L41) explicitly checks pixel geometry: spacing 5 produces a second tile at x=15 for a 10-pixel thumbnail. This supports the implementation and normative contract. The defect is the README’s physical-unit promise, not missing conversion in the implementation.
- **Uncertainty:** No runtime failure or downstream renderer behavior was observed.
- **Next action:** Correct the README table and example to say pixels, preserving version 1 geometry.

[Telemetry line withheld for blind review.]

**Limits:** Target was the supplied Tile plan snapshot; revision and working-tree identity are unknown because no Git metadata was supplied. Project code, tests, and builds executed: **NONE**. No files changed, delegation, shell commands, credential access, or network activity. Runtime behavior and downstream integration remain unassessed.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "FORMAT.md", "tileplan/__init__.py", "tileplan/cli.py", "tileplan/layout.py", "tileplan/options.py", "tests/test_tileplan.py"]}

### Public investigation notes before final report

I’ll read the audit method, then inspect the exposed files for contract gaps and test coverage. I’ll work alone and won’t execute code or change files.

## Report r10

One supported finding: the README gives the wrong spacing units. The implementation and inspected tests agree with the normative pixel contract.

**G1 — README promises millimeters for a pixel-only option**  
**DEMONSTRATED · Documentation drift · Medium impact**

- **Expected:** [FORMAT.md:4](FORMAT.md#L4) specifies whole raster pixels, and lines 5–6 explicitly exclude physical-unit conversion and DPI.
- **Contradiction:** [README.md:17](README.md#L17) labels spacing as millimeters; line 19 promises that `--spacing 5` produces a 5 mm gap. Users following that guidance can produce unintended geometry.
- **Implementation evidence:** [tileplan/cli.py:13](tileplan/cli.py#L13) describes pixels and passes the value directly into `Options` at line 21. [tileplan/layout.py:25](tileplan/layout.py#L25) and lines 32–33 use it directly in raster dimensions and coordinates.
- **Counterevidence and uncertainty:** This supports a documentation defect, not a conversion defect. The README itself identifies `FORMAT.md` as normative. [tests/test_tileplan.py:41](tests/test_tileplan.py#L41) explicitly checks that spacing 5 yields width 25 and the second tile’s x-coordinate 15 for two 10-pixel tiles.
- **Next action:** Change the README’s spacing units and example to pixels, preserving the version 1 implementation. No runtime experiment is needed to establish this contradiction.

[Telemetry line withheld for blind review.]

**Limits:** Repository target was the supplied `repository` snapshot; revision and working-tree identity were unavailable. Runtime behavior and external renderer integration were not assessed. No delegation, file changes, shell commands, network access, or credential access occurred. **Project code, tests, and builds executed: NONE.**

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "FORMAT.md", "tileplan/layout.py", "tileplan/options.py", "tileplan/cli.py", "tileplan/__init__.py", "tests/test_tileplan.py"]}

### Public investigation notes before final report

I’ll read the audit method, then trace documented contracts through the implementation and tests. I’ll use only the inspection tool, make no changes, and stay within the 12-call limit.

## Report r16

Applied the audit method in `[supplied method]`. **One finding: documentation contradicts the normative spacing units.**

**F1 — DEMONSTRATED · Medium · Documentation drift**

The README describes `--spacing` as millimeters and promises that `--spacing 5` creates a 5 mm gap ([README.md:17](README.md#L17), [README.md:19](README.md#L19)). The normative contract explicitly requires whole raster pixels, direct mapping to `spacing_px`, and no physical-unit conversion ([FORMAT.md:3–6](FORMAT.md#L3)).

Implementation follows the normative contract:

- CLI help says “gap in pixels” and passes the argument directly into `Options` ([tileplan/cli.py:13](tileplan/cli.py#L13), [tileplan/cli.py:21](tileplan/cli.py#L21)).
- Layout adds `spacing_px` directly to pixel dimensions and coordinates ([tileplan/layout.py:25–33](tileplan/layout.py#L25)).
- The CLI test supplies spacing 5 and expects the second 10-pixel tile at x=15 ([tests/test_tileplan.py:41–48](tests/test_tileplan.py#L41)).

**Consequence:** A reader following the README can choose spacing under an incorrect physical-size assumption.

**Counterevidence and uncertainty:** The README itself identifies `FORMAT.md` as normative. Implementation and inspected tests agree with that contract, so this is a documentation defect, not evidence of incorrect geometry. No runtime behavior was reproduced.

**Next action:** Change the README’s spacing units and example to pixels. Preserve the existing pixel behavior and default; physical-unit support would require a separately defined contract.

[Telemetry line withheld for blind review.]

Worked alone. No files changed, credentials accessed, network used, or other sessions inspected. **Project code, tests, and builds executed: NONE.** Test results and renderer integration remain unverified.

### Source inspection choices in observed order (method reads omitted)

- Listed supplied project files.
- {"operation": "read", "paths": ["README.md", "FORMAT.md", "tileplan/layout.py", "tileplan/options.py", "tileplan/cli.py", "tileplan/__init__.py", "tests/test_tileplan.py"]}

### Public investigation notes before final report

I’ll read the audit method, inspect the relevant contracts, implementation, and tests, and report only evidence-supported findings. I’ll work alone and won’t execute code or change files.

