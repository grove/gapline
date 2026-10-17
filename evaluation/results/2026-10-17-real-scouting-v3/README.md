# V3 first-curator prompt refusal — retained, not accepted

The adopted capability gate passed the first session: CLI/binary, OS, launcher,
adapter, invocation, model/effort/permission profile and visible capabilities
matched qualification, and no forbidden API was invoked. The worker nevertheless
refused source inspection because the common prompt said "qualified native patch
APIs" without explicitly identifying `apply_patch` as already qualified.

This is a controller prompt ambiguity and an incomplete curator, **not a new host
blocker**. No host investigation or canary test was restarted. No expectations
were accepted or frozen. All later eleven sessions remained NOT RUN. The v1
curator's exposed interpretations were not reused.

Retained: [setup and exact prompts](setup.json), [input](curator-1-input.json),
[CLI activity](curator-1-events.jsonl), [native host activity](curator-1-host-events.jsonl),
[passing capability-gate receipt](curator-1-host.json), [output](curator-1-report.md),
[run receipt](curator-1-run.json), [stderr](curator-1-stderr.txt), and
[57 passing prelaunch checks](prelaunch-tests.txt).

The model completed in **13.970 seconds**, using **24,058 input tokens**
(17,664 cached, already included) and **240 output tokens**: **24,298 total**.
It made zero inspection calls, changed no supplied file and invoked no forbidden
tool. Monetary charges are unavailable. No adapter log exists because no
inspection occurred. Do not fabricate audit reports or call this a negative
scouting-quality result.

The controller stopped as the frozen no-retry protocol requires. A prospective
[exact-name clarification](../../real-scouting-v3.1.md) preserves all actual
permissions and budgets. One replacement requires separate usage approval;
its extra consumed session/tokens must remain in aggregate costs. Production
and #7 are unchanged; no issue closure is justified by this record.
