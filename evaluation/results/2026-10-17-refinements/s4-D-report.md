One supported finding.

**Target and inspection.** Read-only audit of the supplied “Shift worksheet desk” snapshot. Inspected `skill/SKILL.md`, `README.md`, `POLICY.md`, all four `desk/` files, and `tests/test_desk.py` using three inspection calls, including the file listing. Worked alone. Revision and working-tree identity were unavailable; no Git metadata was supplied.

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