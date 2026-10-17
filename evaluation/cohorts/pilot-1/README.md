# Pilot 1 evaluator material

This cohort was freshly authored for the 2026-10-17 pilot. It is synthetic,
not sampled from real repositories. Fresh authorship is not evidence of
pretraining novelty or real-world audit quality. The curator read the existing
teaching fixture names and expectations to avoid reproducing those cases;
the curator did not run audits or inspect pilot worker reports.

Only the three files inside one `cases/qN/` directory are worker input. Copy
them to a neutral `repository/` directory for each fresh trial. Keep this
README, the manifest, the oracle, all case IDs, and other cases outside worker
access. Copied paths alone provide no host isolation. The manifest records
the exact bytes to be reviewed and a neutral question for each case. Questions
are identical to avoid revealing expected outcome. Any later source change
requires a new identity and must be recorded before another review.

`manifest.json` predeclares the intended interpretations and acceptable
alternatives. Judge consequential, supported reasoning rather than demanding
an exact finding count or a particular phrase. Plausible new observations
need independent source review; this oracle does not rule out every other
defect. q1 includes a specific first-publication interruption defect; q2
deliberately retains completed operation identities; q3 has no planted defect.

Run each case's public tests in its own directory. Run the evaluator checks:

```sh
python -m unittest discover -s evaluation/cohorts/pilot-1 -p oracle_test.py -v
```

Expected oracle result is seven tests, with one declared expected failure.
That failing contract assertion and a separate positive witness establish
q1's exact observed consequence. This is an evaluator's execution of trusted
locally authored source, never execution attributed to a read-only worker.
The q2/q3 checks exercise intentional behavior and frozen-page/expiry limits.

This small cohort supports a local KEEP / SIMPLIFY / MODIFY / STOP decision,
not population estimates. It does not establish operating-system durability,
unbounded workload performance, adversarial API safety, or host compliance.
