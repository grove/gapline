# Incremental-value pilot protocol v1

Frozen before workers launch for [issue #5](https://github.com/grove/gapline/issues/5).
This is a small decision experiment, not a benchmark or a quality score.

## Cohort and separation

Use [pilot-1](cohorts/pilot-1/manifest.json): three newly authored, independently
specified repository snapshots. The curator sees the old teaching expectations
to avoid copies, but does not audit the new cases or grade worker reports.
Include a consequential defect, a legitimate design resembling a defect, and a
clean or unresolved case. These are fresh **authored** cases, not production
repositories, randomly sampled defects, or proven absent from model training.
Once published they are teaching cases; never describe reruns as unseen.

Freeze the curator's contracts, evaluator expectations, accepted alternatives,
and executable oracle before launching workers. Retain all files with hashes.
The evaluator oracle is a separate development check, never an audit action.
Workers receive only one case's source, public contract/tests, and neutral
question. No manifest, oracle, sibling case, previous report, or issue text is
supplied. Each arm gets a new session and identical source bytes. A directory
copy and a prompt do not enforce read isolation; inspect host activity for leaks.

## Arms and budgets

- **A:** ordinary agent, no Gapline, no delegation.
- **B:** same host with the exact Gapline payload, no delegation.
- **C:** same payload with selective native delegation available. Scout first;
  skip workers when uneconomical. A worker may challenge a consequential lead.
  Never force a spawn. An unavailable facility stays UNAVAILABLE.

Use the same question, source bytes, model/reasoning settings, tool access, and
limits: 180 seconds elapsed per arm, at most 12 aggregate inspection calls and
250,000 aggregate model tokens. Skill reads and worker inspections consume the
same budget. Wall time is enforced by the launcher; tool/token ceilings are
instructions, not host-enforced caps. Label exceeded or unverifiable budgets.
Do not silently exclude such runs. C has at most two workers and depth one.
Record requested settings and observed settings separately.

Randomize arm order independently for each case with `random.Random(5)`, before
any outputs are read. Run sequentially to avoid concurrent load from other
pilot arms; latency still includes uncontrolled host/server load. No retries
replace attempts. A retry must get a new ID and retain its cause and predecessor.
All arms use persisted sessions because the earlier host smoke found ephemeral
worker launches unavailable. This holds persistence constant across arms.

## Capture and review

The small [launcher](run_pilot.py) copies the frozen sources and skill bytes,
records exact prompts/arguments and pre/post identities, saves stdout JSONL,
stderr, report, elapsed time, exit status and coordinator usage. It never
imports candidate modules. Network access is for the host's model connection;
workers are forbidden network tools, project execution, writes, dependency
installation, credential access, or inspection beyond supplied paths.

Inspect observed commands and selected **own** native-worker activity, if
available, outside the audit. Export only these trial sessions, excluding
credentials, account metadata, global instruction bodies and private reasoning.
Record child usage separately; do not add duplicated inherited parent history
or assert that coordinator usage is aggregate. Missing child costs, monetary
cost, process/network telemetry and permission decisions are UNAVAILABLE.
Unchanged source hashes do not prove absence of writes elsewhere.

Give a separate reviewer the frozen contracts, oracle, source and neutralized
reports in a randomized order. Withhold arm mapping, host costs and the
controller's opinion until judgments are frozen. Do not remove substantive
content; skill-specific report structure may reveal origin, so call this
**origin-masked, imperfect blinding**. The reviewer neither authored the cases
nor ran the audits. A separate model context is independent process review,
not independent human or cross-model replication. Retain its exact input,
output, disagreements and time; no self-grading by audit workers.

Judge every completed report, including zero findings, on supported substantive
claims, important misses, false alarms, unsupported certainty, correct
dismissals/abstention, useful next actions and developer effort to verify.
Use qualitative per-case judgments, not a numerical quality score. Name absent
or uncertain outcomes explicitly. An evaluator oracle can independently witness
a mechanism without converting a worker's unrun check into a runtime result.

## Decision rule and reporting

Publish all nine scheduled attempts and their status, not only successes.
Compare within each case: what useful supported observation did B add to A,
and C to B, and at what observable cost? Warning count and report length are
not value. Preserve false alarms, misses, unavailable runs and budget limits.
No difference means no demonstrated incremental benefit, not equivalence.
Skipped delegation measures the selective configuration, not delegated review.

Choose **KEEP / SIMPLIFY / MODIFY / STOP** and one concrete next experiment.
KEEP requires useful evidence worth its observed overhead; SIMPLIFY is
appropriate when the longer method adds no useful result; MODIFY requires a
specific observed weakness; STOP is appropriate when cost or false alarms
outweigh the observed value. This judgment applies to this cohort only. Missing
aggregate cost or production sampling prevents broader effectiveness claims.
