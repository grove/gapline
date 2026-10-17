Applied the Gapline method in `skill/SKILL.md`. **One finding: documentation contradicts the normative spacing units.**

**F1 — DEMONSTRATED · Medium · Documentation drift**

The README describes `--spacing` as millimeters and promises that `--spacing 5` creates a 5 mm gap ([README.md:17](README.md#L17), [README.md:19](README.md#L19)). The normative contract explicitly requires whole raster pixels, direct mapping to `spacing_px`, and no physical-unit conversion ([FORMAT.md:3–6](FORMAT.md#L3)).

Implementation follows the normative contract:

- CLI help says “gap in pixels” and passes the argument directly into `Options` ([tileplan/cli.py:13](tileplan/cli.py#L13), [tileplan/cli.py:21](tileplan/cli.py#L21)).
- Layout adds `spacing_px` directly to pixel dimensions and coordinates ([tileplan/layout.py:25–33](tileplan/layout.py#L25)).
- The CLI test supplies spacing 5 and expects the second 10-pixel tile at x=15 ([tests/test_tileplan.py:41–48](tests/test_tileplan.py#L41)).

**Consequence:** A reader following the README can choose spacing under an incorrect physical-size assumption.

**Counterevidence and uncertainty:** The README itself identifies `FORMAT.md` as normative. Implementation and inspected tests agree with that contract, so this is a documentation defect, not evidence of incorrect geometry. No runtime behavior was reproduced.

**Next action:** Change the README’s spacing units and example to pixels. Preserve the existing pixel behavior and default; physical-unit support would require a separately defined contract.

**Scope and limits:** Inspected the supplied Tile plan snapshot using **3 inspection calls**: the skill, exposed-file listing, README, format contract, all four package files, and the test file. Reviewed geometry, validation, serialization, and nearby test assertions; no other supported findings emerged. Repository revision and working-tree identity were unavailable; no Git metadata was inspected.

Worked alone. No files changed, credentials accessed, network used, or other sessions inspected. **Project code, tests, and builds executed: NONE.** Test results and renderer integration remain unverified.