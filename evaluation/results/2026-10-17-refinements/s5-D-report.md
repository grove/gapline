One supported finding: the README gives the wrong spacing units. The implementation and inspected tests agree with the normative pixel contract.

**G1 — README promises millimeters for a pixel-only option**  
**DEMONSTRATED · Documentation drift · Medium impact**

- **Expected:** [FORMAT.md:4](FORMAT.md#L4) specifies whole raster pixels, and lines 5–6 explicitly exclude physical-unit conversion and DPI.
- **Contradiction:** [README.md:17](README.md#L17) labels spacing as millimeters; line 19 promises that `--spacing 5` produces a 5 mm gap. Users following that guidance can produce unintended geometry.
- **Implementation evidence:** [tileplan/cli.py:13](tileplan/cli.py#L13) describes pixels and passes the value directly into `Options` at line 21. [tileplan/layout.py:25](tileplan/layout.py#L25) and lines 32–33 use it directly in raster dimensions and coordinates.
- **Counterevidence and uncertainty:** This supports a documentation defect, not a conversion defect. The README itself identifies `FORMAT.md` as normative. [tests/test_tileplan.py:41](tests/test_tileplan.py#L41) explicitly checks that spacing 5 yields width 25 and the second tile’s x-coordinate 15 for two 10-pixel tiles.
- **Next action:** Change the README’s spacing units and example to pixels, preserving the version 1 implementation. No runtime experiment is needed to establish this contradiction.

**Scope and actions:** Applied `skill/SKILL.md` alone using **3 of 12 permitted inspection calls**: read the skill, listed exposed files, and read README, FORMAT, all four `tileplan` modules, and the test file. Traced geometry, defaults, validation, serialization, and inspected test assertions. No other consequential finding survived this source review.

**Limits:** Repository target was the supplied `repository` snapshot; revision and working-tree identity were unavailable. Runtime behavior and external renderer integration were not assessed. No delegation, file changes, shell commands, network access, or credential access occurred. **Project code, tests, and builds executed: NONE.**