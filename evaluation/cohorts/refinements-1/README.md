# Fresh synthetic audit cohort

These five small repositories were independently specified and written for this
cohort on 2026-10-17. They are new synthetic programs, not excerpts from the Gapline
repository or reports. Their domains, requirements, implementations, and public
tests were created together before audit workers were launched. The curator did
not read the parent repository, run Gapline, invoke a paid Codex audit, or inspect
any audit report. Only filesystem/shell tools and standard-library Python were
used. No external source or real customer data supplied the case contents.

Only one `cases/sN` directory should be exposed to a worker. `manifest.json`, this
README, and `oracle.py` are evaluator-only and must not be included in worker
repositories, prompts, search roots, or report context. Workers receive the same
neutral question recorded in the manifest. The manifest records the complete
inventory, byte lengths, SHA-256 hashes, exact contract excerpts, and expected
interpretations. Hashes freeze the cases; any edit invalidates this cohort.

During prelaunch source review, the parent evaluator identified that the initial
sensor sketch accepted unbounded finite magnitudes: Fahrenheit conversion and
multi-reading summation could overflow. No audit workers had launched. The curator
then specified an explicit sensor range (-273.15 to 1000 C, equivalent F bounds),
validated it before arithmetic (including arbitrary-size integer rejection), and
added public and evaluator controls. This correction is part of the final frozen
cases; the original unbounded sketch was not a valid clean control. No audit
report informed this correction.

All public tests were executed by the curator using `python3 -B -m unittest
discover -s tests -v`. The evaluator oracle confirms the designed cross-boundary
behavior, controls, unresolved requirement, documentation discrepancy, and hashes.
It deliberately asserts the observable faulty behavior in the affected case; it
does not repair code. Its documentation check is static and needs no runtime
execution of that case.

Limitations: these are compact, single-process, in-memory synthetic systems. They
sample five evidence-interpretation situations, not prevalence in real projects,
security assurance, production concurrency, or the full variety of audits. Passing
supplied tests establishes the explicit controls used here, not universal absence
of defects. Neither a useful uncertainty report nor a documentation-only finding
must produce a code edit. Extra findings are judged against their exact evidence,
public API scope, and material consequences rather than automatically rejected.
