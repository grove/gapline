# Worker prompts

These are the task-local prompts for the two completed workers. Each began
without the parent conversation. Common host/developer instructions still
applied; this file does not claim to reproduce the full runtime context.

## Gapline

```text
Use gapline-audit at /workspace/scratch/4fb9d73ce3bf/gapline-trials/installed/.agents/skills/gapline-audit/SKILL.md to review these four components for consequential behavior, test, documentation, or architecture problems:
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-1/repository
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-2/repository
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-3/repository
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-4/repository
You may read only these repository directories and the installed gapline-audit directory, including its reference file. Use the available host file tools or bounded read-only shell inspection. Do not read surrounding directories, other agent messages/artifacts, or other sources. Do not run project code/tests, import project modules, write files, access the network, or invoke additional agents. Use at most 12 inspection tool calls. Return a concise report for each component with grounded findings or an honest no-supported-findings result; at most five substantive findings overall. Cite exact inspected paths/lines and distinguish source observations from unverified runtime behavior. Include the inspection commands/facilities actually used in a short activity note. Return the report here; do not save it.
```

## Ordinary review

```text
Review these four components for consequential behavior, test, documentation, or architecture problems:
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-1/repository
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-2/repository
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-3/repository
- /workspace/scratch/4fb9d73ce3bf/gapline-trials/case-4/repository
You may read only these repository directories. Use the available host file tools or bounded read-only shell inspection. Do not read surrounding directories, other agent messages/artifacts, or other sources. Do not run project code/tests, import project modules, write files, access the network, or invoke additional agents. Use at most 12 inspection tool calls. Return a concise report for each component with grounded findings or an honest no-supported-findings result; at most five substantive findings overall. Cite exact inspected paths/lines and distinguish source observations from unverified runtime behavior. Include the inspection commands/facilities actually used in a short activity note. Return the report here; do not save it.
```
