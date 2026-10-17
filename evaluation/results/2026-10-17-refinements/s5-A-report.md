One supported finding: the README gives spacing units that contradict the normative format and implementation.

**G1 — Incorrect spacing units in user documentation**  
**Category:** documentation drift. **Evidence:** DEMONSTRATED source contradiction. **Impact:** Medium; users following the README can produce an unintended physical gap.

- **Expected:** [README.md:17](README.md#L17) describes spacing in millimeters; [README.md:19](README.md#L19) explicitly promises that `--spacing 5` leaves a 5 mm gap.
- **Observed in source:** [FORMAT.md:3–6](FORMAT.md#L3) establishes the normative contract: spacing is whole raster pixels, with no DPI conversion. [cli.py:13](tileplan/cli.py#L13) labels the option in pixels, [cli.py:21](tileplan/cli.py#L21) passes it directly into `Options`, and [layout.py:32–33](tileplan/layout.py#L32) uses it directly in coordinate arithmetic.
- **Counterevidence and test protection:** [test_tileplan.py:41–48](tests/test_tileplan.py#L41) explicitly checks pixel geometry: spacing 5 produces a second tile at x=15 for a 10-pixel thumbnail. This supports the implementation and normative contract. The defect is the README’s physical-unit promise, not missing conversion in the implementation.
- **Uncertainty:** No runtime failure or downstream renderer behavior was observed.
- **Next action:** Correct the README table and example to say pixels, preserving version 1 geometry.

**Scope and actual actions:** Applied `skill/SKILL.md` alone using three inspection-tool calls: one skill read, one file listing, and one batched source/document/test read. Inspected `README.md`, `FORMAT.md`, `tileplan/{__init__,cli,layout,options}.py`, and `tests/test_tileplan.py`. Source review found no additional supported discrepancy in validation, ordering, canvas formulas, defaults, or empty-plan handling.

**Limits:** Target was the supplied Tile plan snapshot; revision and working-tree identity are unknown because no Git metadata was supplied. Project code, tests, and builds executed: **NONE**. No files changed, delegation, shell commands, credential access, or network activity. Runtime behavior and downstream integration remain unassessed.