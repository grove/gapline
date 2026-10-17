"""Prepare origin-masked inputs and run exactly two authorized Codex reviews."""

import argparse
import hashlib
import json
from pathlib import Path
import random
import re

from run_pilot import identity
from run_refinements import ROOT, launch, schedule


def mask(text):
    text = re.sub(r"/private/tmp/gapline-refinement-workers/trial-\d+/repository/", "", text)
    text = re.sub(r"(?mi)^.*(?:budget|inspection calls|tool calls|calls used|elapsed|tokens).*$", "[Telemetry line withheld for blind review.]", text)
    text = re.sub(r"\b\d+\s+(?:inspection|tool)\s+calls?\b", "[inspection count withheld]", text, flags=re.I)
    text = re.sub(r"\b\d+\s+calls?\b", "[call count withheld]", text, flags=re.I)
    text = re.sub(r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+(?:inspection|tool)\s+calls?\b", "[inspection count withheld]", text, flags=re.I)
    text = text.replace("skill/SKILL.md", "[supplied method]").replace("Gapline", "audit")
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    cohort = ROOT / "evaluation/cohorts/refinements-1"
    manifest = json.loads((cohort / "manifest.json").read_text())
    runs = [f"{case}-{arm}" for case, arm in schedule()]
    if any(not (args.output / f"{run}-run.json").is_file() for run in runs):
        raise ValueError("all 20 audit attempts must be retained before review")
    random.Random(67).shuffle(runs)
    mapping = {f"r{index:02d}": run for index, run in enumerate(runs, 1)}
    (args.output / "review-mapping.json").write_text(json.dumps(mapping, indent=2) + "\n")
    records = []
    for reviewer, cases in ((1, ("s1", "s2", "s3")), (2, ("s4", "s5"))):
        project = args.work / f"review-{reviewer}" / "repository"
        project.mkdir(parents=True)
        for case_id in cases:
            case = next(case for case in manifest["cases"] if case["id"] == case_id)
            public = cohort / "cases" / case_id
            text = f"# Case {case_id}\n\n## Source (numbered original lines)\n\n"
            for name in identity(public):
                text += f"### {name}\n\n```\n"
                text += "\n".join(f"{number}: {line}" for number, line in enumerate((public / name).read_text().splitlines(), 1))
                text += "\n```\n\n"
            expected = {key: case[key] for key in ("contracts", "expected_interpretation", "accepted_alternatives", "criteria")}
            text += "## Frozen evaluator interpretation (nonexhaustive; challenge if wrong)\n\n" + json.dumps(expected, indent=2) + "\n\n"
            for label, run in mapping.items():
                if not run.startswith(case_id + "-"):
                    continue
                text += f"## Report {label}\n\n" + mask((args.output / f"{run}-report.md").read_text()) + "\n\n"
                text += "### Source inspection choices in observed order (method reads omitted)\n\n"
                for line in (args.output / f"{run}-inspections.jsonl").read_text().splitlines():
                    call = json.loads(line)
                    arguments = call["params"]["arguments"].copy()
                    if "paths" in arguments:
                        arguments["paths"] = [path for path in arguments["paths"] if not path.startswith("skill/")]
                        if not arguments["paths"]:
                            continue
                    if arguments["operation"] == "list":
                        text += "- Listed supplied project files.\n"
                    else:
                        text += "- " + json.dumps(arguments) + "\n"
                events = [json.loads(line) for line in (args.output / f"{run}-events.jsonl").read_text().splitlines()]
                messages = [event["item"]["text"] for event in events if event.get("type") == "item.completed"
                            and event.get("item", {}).get("type") == "agent_message"]
                if len(messages) > 1:
                    text += "\n### Public investigation notes before final report\n\n" + mask("\n".join(messages[:-1])) + "\n"
            (project / f"{case_id}.md").write_text(text)
        prompt = (
            "You are a fresh independent report reviewer, not a case author or audit worker. Work alone. "
            "Use only the inspection MCP tool to read the supplied case bundles (list files, then read one bundle per call to avoid truncation). "
            "Do not execute any code/tests/builds, edit, use network, access other sessions or files, or use audit skills. "
            "You have 180 seconds, 12 inspection calls and 250000 input-plus-output tokens. "
            "Reports are origin-masked and randomly labeled; arm identities, time/token costs and controller preferences are withheld. "
            "Do not infer methods. Judge against exact source and authoritative contracts, not agreement with the nonexhaustive evaluator interpretation. "
            "For EVERY report label, assess correctness, material misses/false positives, useful probe selection, refuted leads, "
            "appropriate no-findings/uncertainty, misleading certainty, and next-action usefulness. For consequential unresolved claims, "
            "check starting conditions/trigger, observable oracle, supporting and refuting outcomes, assumptions/alternatives, and avoidable developer effort. "
            "Reward concise useful distinctions, not finding count, field count or verbosity. Documentation contradictions should permit direct correction; "
            "missing requirements should prompt clarification, not invented expectations. Executable follow-ups must remain PROPOSED — NOT RUN. "
            "Compare all four reports within each case: identify material gains, ties, unnecessary complexity, and the cheapest adequate handoff. "
            "Record disagreement with evaluator expectations and report any residual method disclosure. "
            "Do not resolve the product decision or claim independent human validation. Return your frozen judgments in the final response.\n"
        )
        records.append({"reviewer": reviewer, "files": identity(project), "prompt": prompt})
    # Freeze both input sets before either reviewer sees a report.
    (args.output / "review-inputs.json").write_text(json.dumps(records, indent=2) + "\n")
    for record in records:
        reviewer = record["reviewer"]
        project = args.work / f"review-{reviewer}" / "repository"
        for path in project.iterdir():
            (args.output / f"review-{reviewer}-{path.name}").write_bytes(path.read_bytes())
        result = launch(f"review-{reviewer}", project, args.output, record["prompt"])
        if result["status"] != "COMPLETED" or result["forbidden_activity"]:
            raise RuntimeError("review attempt incomplete; no automatic retry")
        report = args.output / f"review-{reviewer}-report.md"
        (args.output / f"review-{reviewer}-frozen.sha256").write_text(hashlib.sha256(report.read_bytes()).hexdigest() + "\n")


if __name__ == "__main__":
    main()
