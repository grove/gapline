"""Replay retained receipts and costs; never launches a model session."""

import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "evaluation"))
from run_real_scouting import SCHEDULE, accept_host, check_freeze, normalize_argv, qualified_reference


def main():
    setup, frozen = check_freeze()
    rows = []
    for name in ["curator-1", "curator-2"] + [f"{case}-{arm}" for case, arm in SCHEDULE] + ["review-1", "review-2"]:
        path = HERE / f"{name}-run.json"
        if not path.exists():
            assert name in {"r3-B", "r3-A", "r4-A", "r4-B", "review-1", "review-2"}
            rows.append({"id": name, "status": "NOT RUN", "reason": "Stopped after r2-A timeout; no retries"})
            continue
        run = json.loads(path.read_text())
        original = json.loads((HERE / f"{name}-input.json").read_text())
        host = json.loads((HERE / f"{name}-host.json").read_text())
        calls = [json.loads(line) for line in (HERE / f"{name}-inspections.jsonl").read_text().splitlines()]
        accept_host(host, qualified_reference())
        assert run["status"] == "COMPLETED" or name == "r2-A" and run["status"] == "TIMEOUT"
        assert run["before"] == run["after"] == original["before"]
        assert run["stdin"] == original["stdin"] == setup["prompts"][name]
        assert normalize_argv(run["argv"]) == setup["boundary"]["normalized_argv"]
        assert run["token_limit"] == 1000000
        assert 0 < len(calls) == run["inspection_calls"] == len(host["mcp_calls"]) <= 12
        assert not run["forbidden_activity"]
        assert all(host[key] == value for key, value in frozen["host_instructions"].items())
        if run["status"] == "TIMEOUT":
            assert run["usage"] == run["token_budget_met"] == "UNAVAILABLE"
            assert run["elapsed_seconds"] >= 180 and not (HERE / f"{name}-report.md").exists()
            rows.append({"id": name, "status": "TIMEOUT", "seconds": run["elapsed_seconds"], "calls": len(calls),
                         "errors": sum(bool(call["result"].get("isError")) for call in calls),
                         "input": None, "cached": None, "output": None, "total": None})
            continue
        assert run["exit_code"] == 0 and run["token_budget_met"] is True and run["elapsed_seconds"] <= 180
        usage = run["usage"]
        assert 0 <= usage["cached_input_tokens"] <= usage["input_tokens"]
        rows.append({"id": name, "status": "COMPLETED", "seconds": run["elapsed_seconds"], "calls": len(calls),
                     "errors": sum(bool(call["result"].get("isError")) for call in calls),
                     "input": usage["input_tokens"], "cached": usage["cached_input_tokens"],
                     "output": usage["output_tokens"], "total": usage["input_tokens"] + usage["output_tokens"]})
        if name.startswith("review-"):
            assert hashlib.sha256((HERE / f"{name}-report.md").read_bytes()).hexdigest() == (HERE / f"{name}-frozen.sha256").read_text().strip()
    totals = {}
    for group, selected in {"A": [r for r in rows if r["id"].endswith("-A")],
                            "B": [r for r in rows if r["id"].endswith("-B")],
                            "curators": rows[:2], "reviewers": rows[-2:], "all_attempted": rows}.items():
        selected = [r for r in selected if r["status"] != "NOT RUN"]
        totals[group] = {"attempts": len(selected), "complete": sum(r["status"] == "COMPLETED" for r in selected)}
        totals[group].update({key: round(sum(r[key] or 0 for r in selected), 3)
                              for key in ("seconds", "calls", "errors", "input", "cached", "output", "total")})
        totals[group]["usage_complete"] = all(r["total"] is not None for r in selected)
    history = []
    for directory, name in (("2026-10-17-real-scouting", "curator-1"),
                            ("2026-10-17-real-scouting-v2", "curator-1"),
                            ("2026-10-17-host-capabilities", "probe"),
                            ("2026-10-17-real-scouting-v3", "curator-1")):
        run = json.loads((HERE.parent / directory / f"{name}-run.json").read_text())
        history.append({"directory": directory, "seconds": run["elapsed_seconds"],
                        "input": run["usage"]["input_tokens"], "cached": run["usage"]["cached_input_tokens"],
                        "output": run["usage"]["output_tokens"],
                        "total": run["usage"]["input_tokens"] + run["usage"]["output_tokens"]})
    assert len(rows) == 12 and totals["all_attempted"]["attempts"] == 6
    result = {"decision": "INCONCLUSIVE", "runs": rows, "totals": totals, "historical_preparation": history,
              "monetary_cost": "UNAVAILABLE", "controller_usage": "UNAVAILABLE"}
    (HERE / "measurements.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = ["# Retained session measurements", "", "Input includes cached input once. Reasoning output is included in output.",
             "Errors are rejected inspection requests, included in calls. Seconds are session elapsed, not active work.",
             "Monetary charges and controller usage are unavailable. Group token sums include known usage only; r2-A final usage is unavailable.",
             "This replay makes no model calls. See r2-A-partial-usage.json for separately retained partial counters.", "",
             "| Session | Status | Seconds | Calls | Errors | Input | Cached subset | Output | Total |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in rows:
        label = "[" + row["id"] + "](" + row["id"] + "-report.md)" if row["status"] == "COMPLETED" else row["id"]
        lines.append("| " + label + " | " + row["status"] + " | " + " | ".join(
            str(row[key]) if row.get(key) is not None else "UNAVAILABLE" for key in
            ("seconds", "calls", "errors", "input", "cached", "output", "total")) + " |")
    (HERE / "measurements.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
