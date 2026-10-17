"""Recompute descriptive costs/activity; never invokes a model or project code."""

import hashlib
import json
from pathlib import Path
import sys

OUTPUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUTPUT.parents[1]))
from run_pilot import identity
from run_refinements import skill_variants


def main():
    variants = skill_variants()
    cohort = OUTPUT.parents[1] / "cohorts/refinements-1/cases"
    totals = {arm: {"elapsed_seconds": 0, "inspection_calls": 0, "input_tokens": 0,
                    "cached_input_tokens": 0, "output_tokens": 0} for arm in "ABCD"}
    records = []
    for path in sorted(OUTPUT.glob("*-run.json")):
        run = json.loads(path.read_text())
        events = [json.loads(line) for line in (OUTPUT / f"{run['id']}-events.jsonl").read_text().splitlines()]
        calls = [json.loads(line) for line in (OUTPUT / f"{run['id']}-inspections.jsonl").read_text().splitlines()]
        run["adapter_errors"] = [call for call in calls if call["result"].get("isError")]
        run["event_errors"] = [event["item"] for event in events if event.get("item", {}).get("type") == "error"]
        run["tool_types"] = sorted({event["item"]["type"] for event in events if event.get("type") == "item.completed"})
        run["project_inspections"] = [call["params"]["arguments"] for call in calls
                                      if any(not path.startswith("skill/") for path in call["params"]["arguments"].get("paths", []))]
        run["tool_servers"] = sorted({event["item"].get("server", "") for event in events if event.get("item", {}).get("type") == "mcp_tool_call"})
        if run["id"].startswith("s"):
            case, arm = run["id"].split("-")
            expected = identity(cohort / case)
            for name, content in variants[arm].items():
                data = content.encode()
                expected[f"skill/{name}"] = {"sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}
            run["matches_frozen_inputs"] = run["before"] == expected
            for key in totals[arm]:
                totals[arm][key] += run.get(key, run["usage"].get(key, 0))
        run["observed_settings"] = "UNAVAILABLE"
        # Only these exact experiment thread IDs; never export unrelated sessions,
        # global instruction bodies, private reasoning, or authentication material.
        matches = list((Path.home() / ".codex/sessions").glob(f"**/*{run['thread_id']}.jsonl"))
        if len(matches) == 1:
            contexts = []
            with matches[0].open() as stream:
                for line in stream:
                    item = json.loads(line)
                    if item.get("type") == "turn_context":
                        contexts.append({key: item["payload"][key] for key in
                                         ("model", "effort", "approval_policy", "sandbox_policy") if key in item["payload"]})
            run["observed_settings"] = contexts
        records.append({key: run[key] for key in ("id", "status", "elapsed_seconds", "inspection_calls", "usage", "thread_id",
                        "token_budget_met", "forbidden_activity", "adapter_errors", "event_errors", "tool_types", "tool_servers",
                        "observed_settings", "project_inspections")} | {
                            "unchanged": run["before"] == run["after"],
                            "matches_frozen_inputs": run.get("matches_frozen_inputs", "review inputs separately frozen"),
                            "report_bytes": (OUTPUT / f"{run['id']}-report.md").stat().st_size})
    for total in totals.values():
        total["elapsed_seconds"] = round(total["elapsed_seconds"], 3)
    audits = [run for run in records if run["id"].startswith("s")]
    assert len(audits) == 20 and all(sum(run["id"].endswith("-" + arm) for run in audits) == 5 for arm in "ABCD"), "retain all scheduled audit attempts"
    assert all(run["usage"]["cached_input_tokens"] <= run["usage"]["input_tokens"] for run in records), "cached tokens are a subset of input"
    (OUTPUT / "measurements.json").write_text(json.dumps({"arms": totals, "runs": records}, indent=2) + "\n")
    rows = ["| Run | Seconds | Inspections | Input | Cached subset | Output | Report |", "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for run in records:
        usage = run["usage"]
        rows.append(f"| {run['id']} | {run['elapsed_seconds']:.3f} | {run['inspection_calls']} | {usage['input_tokens']:,} | {usage['cached_input_tokens']:,} | {usage['output_tokens']:,} | [report]({run['id']}-report.md) |")
    (OUTPUT / "measurements.md").write_text("\n".join(rows) + "\n")
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
