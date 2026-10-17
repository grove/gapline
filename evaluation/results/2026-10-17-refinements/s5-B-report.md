One finding survived inspection.

**G1 — README gives incompatible spacing units**  
**Documentation drift · DEMONSTRATED · Medium impact**

- **Expected:** The normative contract specifies whole raster pixels and explicitly excludes physical-unit conversion or DPI (`FORMAT.md:3–6`, `18–19`).
- **Observed:** The README describes `--spacing` as millimeters and promises that `--spacing 5` produces a 5 mm gap (`README.md:17–19`). The CLI instead passes the integer directly into `spacing_px` (`tileplan/cli.py:21`), which is added directly to pixel coordinates (`tileplan/layout.py:25–26`, `32–33`). Users following the README could therefore choose incorrect spacing for their intended physical output.
- **Counterevidence and test protection:** The README identifies `FORMAT.md` as normative (`README.md:5`); CLI help correctly says pixels (`tileplan/cli.py:13`). Tests explicitly assert pixel geometry for spacing 5 (`tests/test_tileplan.py:41–48`). These support the implementation and locate the contradiction in the README. Runtime behavior was not executed.
- **Next action:** Correct the README table and example to say pixels. Preserve the version 1 implementation and its existing pixel assertions.

I applied [the Gapline method](skill/SKILL.md), working alone. Used **4 of 12 inspection calls**: read the skill, listed exposed files, and read both product documents, all four exposed implementation files, and the test file. No additional consequential implementation or test-protection finding was supported.

Target: the supplied `tileplan` snapshot. Revision and working-tree identity were unavailable; no Git metadata was inspected. This was static inspection only, so runtime behavior and external renderer integration remain unverified. No files were changed; no network, credentials, or other sessions were accessed. **Project code, tests, and builds executed: NONE.**