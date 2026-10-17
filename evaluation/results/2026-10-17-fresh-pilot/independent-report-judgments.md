# Frozen origin-masked report judgments

Judgments are frozen before receipt of any arm mapping, cost data, or controller opinion. Reports were read in the randomized index order: r01, r02, r03, r04, r05, r06, r07, r08, r09. Only the supplied cohort and review-directory materials were inspected. Formatting and method mentions imperfectly mask origin; no arm identity was inferred or used. This is process-independent model review, not human or cross-model replication.

The frozen sources and explicit contracts control these judgments. The manifest is a useful predeclared interpretation, not an exhaustive answer key: a clean scoped case may still have a supported test gap or qualified performance concern. The earlier source assessment and actual evaluator oracle execution remain separate from the workers' static suggestions. All nine reports label their proposed checks as not run; none supplies a runtime reproduction. Their inspection/compliance statements are self-reports, not independently verified host traces.

## r01 — q3

**Judgment: two supported, narrowly scoped test-protection findings; no demonstrated runtime defect.**

- Supported substance: the public pagination test writes everything before begin and never interleaves an append (`test_changes.py:7-20`). The compaction test calls begin after compaction, never resume on a preexisting continuation (`:22-29`). These omissions match the two explicit contracts and the suggested checks directly exercise them.
- Correct dismissal/abstention: the report explicitly recognizes that the current upper-bound propagation and shared expiration guard support correctness (`changes.py:45-66`). It does not assert lost changes, retained invalid continuations, or a defective snapshot adapter.
- Important misses: no material implementation defect was independently established for this case. The potential repeated-scan cost discussed under r09 is absent, but its practical importance is unestablished. This is not an obligatory missed defect.
- False positives or unsupported certainty: no factual false positive. Calling both gaps medium impact is prioritization judgment, not proof of material user harm. Shared `_page` code already reduces the chance of resume diverging, so the continuation-expiry gap should remain a modest regression concern rather than an implied current failure.
- Useful next actions and verification effort: inexpensive. Read the single public test file and common page helper, then add the two short interleaving scenarios. The floor-equality continuation check is a useful adjacent boundary. These are suggested tests; the worker did not execute them. The evaluator previously ran its own frozen-pull and continuation-expiry oracle checks successfully.

## r02 — q1

**Judgment: correctly identifies the consequential first-publication recovery defect and its missing boundary test.**

- Supported substance: the pointer replacement is the documented commit point (`README.md:14-19`); complete generation files precede it (`artifacts.py:61-65`); absent CURRENT causes recovery to promote the latest complete generation (`:42-49`). Reopening can therefore expose a publication whose replacement failed.
- Correct dismissal/abstention: the existing-commit early return and public test are accurately acknowledged. The report does not generalize to overwriting an existing commit or invoke excluded concurrency, corruption, or power-loss behavior.
- Important misses: none material within this scope. The intermediate read returning None could be stated more explicitly, but its omission does not obscure the consequence.
- False positives or unsupported certainty: none consequential. “Recovery needs evidence of commitment beyond a complete generation” is acceptable as a principle that completeness cannot establish commitment; preserving absent CURRENT as empty is also sufficient and need not introduce a new durable mechanism.
- Useful next actions and verification effort: inexpensive, deterministic. The empty-store replacement-failure/reopen check directly distinguishes the bug from the passing public test. The additionally suggested interruption point is substantially the same boundary, so a separate test may add little. Source reasoning was not a worker reproduction; the independent evaluator's positive witness already confirmed the exact consequence.

## r03 — q3

**Judgment: one combined finding contains two valid test gaps, with appropriately explicit runtime abstention.**

- Supported substance: the missing between-page append and missing compaction-during-continuation scenarios are exactly absent from the public tests and matter to explicit contracts. Grouping them under a pagination regression-protection finding is reasonable; finding count is not quality evidence.
- Correct dismissal/abstention: source correctness and the shared helper are acknowledged. No claim is made that changes are currently lost or that expiration itself violates a snapshot guarantee.
- Important misses: none material established. As with r01, the unmeasured scan-cost observation is optional rather than a required defect.
- False positives or unsupported certainty: none factual. Medium impact should be read as the importance of protecting the contract, not an observed production incident. The current common helper is meaningful counterevidence against a separate resume-only failure.
- Useful next actions and verification effort: inexpensive. The two proposed scenarios and floor equality are clear and bounded. They are proposed, not executed by the worker. The evaluator's earlier oracle checks independently exercised the first two mechanisms successfully.

## r04 — q2

**Judgment: the NaN mechanism is supported; whether it is a consequential in-scope defect remains conditional on the duration input contract.**

- Supported substance: `ttl <= 0` does not reject floating-point NaN (`leases.py:33-34`). Adding it produces a NaN deadline (`:46`); both `now >= deadline` comparisons become false (`:37,60`). An abandoned lease is then ineligible for reclamation, while its still-current token can finish at an arbitrarily later finite time. This is a legitimate novel source-derived observation and matches the uncertainty independently recorded before reading reports.
- Correct dismissal/abstention: the report distinguishes ordinary finite durations, admits that adapter reachability is unknown, and does not attack intentional completed-key retention or correctly implemented ordinary stale-token fencing. A report with no findings under an explicit finite-duration precondition would also be defensible.
- Important misses: the normal-duration test gap found by r06/r08 is absent. It is a useful additional check but does not invalidate this report's different observation.
- False positives or unsupported certainty: the opening “supported finding” and unconditional title are slightly stronger than the resolved evidence warrants. The body provides the necessary qualification: the README leaves TTL's finite domain implicit and no adapter is available. Timestamp monotonicity alone does not establish valid finite TTLs. Accept the conditional concern; do not count an unqualified contract violation or an observed hang as proven. There is no actual runtime witness in this report or the executed oracle for NaN.
- Useful next actions and verification effort: local mechanism verification is inexpensive; contract adjudication requires checking or specifying the caller's valid duration domain. If the API owns validation, a focused NaN rejection check before state mutation is appropriate. Deciding infinite-duration policy is reasonable only as clarification of that domain, not an extra required feature. This should not displace the documented ordinary lease semantics.

## r05 — q1

**Judgment: correctly identifies the same consequential first-publication defect, with a precise test and scope.**

- Supported substance: correctly traces complete bytes plus metadata, failed first pointer replacement, recovery promotion, and visibility through read. It correctly relates the public test's prior approved publication to the missing empty-state boundary.
- Correct dismissal/abstention: explicitly limits the claim to source reasoning, preserves existing-CURRENT counterevidence, and avoids excluded failure models. Diagnostic retention of complete unpublished generations is respected by the proposed test.
- Important misses: none material. Immediate post-failure read could be included alongside the reopened read in the proposed assertion to show the state transition more fully.
- False positives or unsupported certainty: “DEMONSTRATED source-level contradiction” is justified by the direct control flow and is immediately qualified as no runtime reproduction. It must not be recounted as a worker-executed demonstration. High impact is plausible for generated configuration consumers, though no deployment incident is established.
- Useful next actions and verification effort: inexpensive, with a deterministic empty-store fault injection and a small recovery decision. The proposed staging cleanup and diagnostic-generation assertions fit the explicit contract. The independent evaluator already witnessed candidate visibility; worker execution remains none as reported.

## r06 — q2

**Judgment: supported normal-input test gap; correctly abstains from claiming an implementation defect.**

- Supported substance: in the public expiry test, reserve reissues at the deadline before old completion is attempted (`test_leases.py:18-26`). Token mismatch alone rejects the old completion. Other public completions are before expiry. Removing only finish's deadline condition would therefore escape these public assertions. This is exact, useful reasoning rather than generic “add more tests” advice.
- Correct dismissal/abstention: recognizes the current deadline guard and meaningful stale-token coverage. It does not misclassify completed-key retention, bounded memory, serialized access, or lack of persistence.
- Important misses: it does not discuss the conditional NaN concern. Because valid duration-domain ownership is unresolved, this is not a confirmed missed in-scope defect; a carefully qualified mention could improve completeness.
- False positives or unsupported certainty: no factual false positive. Medium impact is a reasonable prioritization of the protected rule, not proof of current failure. “No implementation defect established” remains fair given the unresolved duration domain.
- Useful next actions and verification effort: inexpensive. Exercise finish at and after expiry without reassignment, assert rejection preserves state/result, and optionally pin just-before success. These are not worker-executed tests. The evaluator's earlier oracle separately checked finish at exact expiry before reassignment, then stale/fresh tokens.

## r07 — q1

**Judgment: correctly identifies and bounds the consequential first-publication defect.**

- Supported substance: complete generation creation precedes replacement; absent CURRENT causes recovery promotion; resulting bytes violate the explicit empty-state recovery rule. The consumer consequence and public test blind spot are accurately explained.
- Correct dismissal/abstention: explicitly states runtime was not tested, preserves the existing-commit counterexample, and requires no excluded concurrency, corruption, or durability assumption.
- Important misses: none material. It could explicitly assert immediate post-failure None in the proposed check, but the recovery consequence is already clear.
- False positives or unsupported certainty: none. “DEMONSTRATED source-level contradiction” is appropriately qualified and must remain separate from actual execution.
- Useful next actions and verification effort: inexpensive. The deterministic empty-store replacement-failure/reopen test and instruction not to infer commitment from completeness are sufficient. Retaining complete generations for diagnostics is correctly included. The evaluator's earlier witness independently confirms the predicted behavior.

## r08 — q2

**Judgment: supported test-protection finding, materially equivalent to r06.**

- Supported substance: its mutation thought experiment is accurate: removing only finish's deadline comparison leaves the public tests satisfied because the old token has already been superseded. Exact-deadline and post-deadline finish without intervening reserve are missing.
- Correct dismissal/abstention: recognizes correct current implementation and existing coverage for deadline reassignment, stale tokens, duplicate completion, serialized calls, and bounded lifetime. It makes no retention or persistence false alarm.
- Important misses: the same conditional NaN issue is absent. The phrase “No additional consequential findings survived” is a report of its review, not an exhaustive correctness certificate; its explicit limits for unusual values help. It should not be used to reject r04's qualified observation.
- False positives or unsupported certainty: none factual. Medium denotes a regression-protection priority, not demonstrated expired-work acceptance in the snapshot.
- Useful next actions and verification effort: inexpensive. The suggested exact/after-deadline rejection and unchanged-state checks directly protect the missing branch. Actual evaluator execution previously covered exact-deadline rejection; this worker proposed rather than ran tests.

## r09 — q3

**Judgment: one supported asymptotic performance concern with unresolved practical materiality, plus one supported test gap.**

- Supported substance: `_page` scans all retained events and materializes the full matching pending list before slicing (`changes.py:58-66`). For a fixed history of N events drained in pages of L, roughly N/L calls each scan N retained events, yielding O(N²/L) scan work and O(N) peak pending allocation. The source supports that algorithmic observation without benchmarking. A small page limit does not bound the first page's temporary pending allocation.
- Correct dismissal/abstention: the report acknowledges compaction and lack of workload/performance targets, and proposes measurement rather than claiming measured slowness. Compaction can reduce retained history when callers use it; no automatic fixed bound follows from this component. Its frozen-pull test omission and source correctness counterevidence are accurate.
- Important misses: compaction during an active continuation lacks a public test, as r01/r03 identify. This is a useful omission within a request allowing at most three findings, but it is not a missed current failure.
- False positives or unsupported certainty: the complexity claim is not a false positive. Treating it as an established consequential performance defect would overstate the evidence: no realistic history size, latency budget, or measurement is supplied. The conditional wording and proposed benchmark keep it a legitimate concern. No hostile-token, snapshot, or lost-write alarm is raised.
- Useful next actions and verification effort: the frozen-pull test is inexpensive. Practical performance validation requires a modest benchmark with representative retained-history sizes and page limits, plus an actual workload threshold. Do that before changing to indexed lookup or limit-plus-one traversal. No such measurement was run by the worker or in the earlier oracle.

## Within-case comparison and disagreements

All three q1 reports identify the same important consequence, source path, and test boundary. Their detail and formatting differ without a meaningful outcome difference; none claims executed reproduction.

For q2, r06/r08 provide the same concrete ordinary-duration regression check. r04 provides a different, technically valid NaN mechanism whose contract status remains unresolved. Neither exact agreement with the manifest nor novelty alone decides quality. I disagree with an unconditional interpretation of r04's opening, but its body preserves the uncertainty needed to keep the observation useful. I also would not treat absence of that conditional issue in r06/r08 as a proven missed defect.

For q3, r01/r03 cover both explicit interleaving gaps; r09 covers the frozen-pull gap and a valid unmeasured scaling concern. I would not classify these test findings as false positives merely because the intended case permits a no-finding response. Equally, none proves a current functional failure, and the performance concern should not trigger an optimization without a relevant workload. A scoped no-finding answer would remain acceptable; none of the nine reports takes a wholly no-finding outcome, though all q3 reports and r06/r08 explicitly abstain from alleging implementation failure.

The reports largely preserve counterevidence and distinguish proposals from execution. Repetition of medium-priority test findings on tiny correct components raises an open usefulness question: are developers gaining a meaningful guard or spending effort on tests that mostly mirror a shared helper? These particular scenarios exercise documented interleavings and a masked deadline branch, so they are defensible, but report count alone cannot resolve their value.

## Next experiment based on these reports alone

Use a fresh, larger frozen cohort with explicit caller input-domain contracts and a mix of consequential defects, meaningful uncovered contract boundaries, already-covered clean components, and scaling cases with stated workloads. Keep report origins hidden during outcome review. Ask a developer to apply the suggested checks or fixes and record whether each produces new protection or a material behavior change and how much verification effort it takes. Predeclare treatment of qualified input-validation concerns and test-only findings, while still allowing independently supported novel claims. This addresses the ambiguity exposed by NaN, test-gap proliferation, and unmeasured performance without inferring which method produced any report.

## Inspection record and limits

For this report-judging phase, actual inspection shell/tool calls: four (one failed attempt to read the initially absent nested index; one report-directory file listing; one successful index read after the index was supplied there; one batched read of all nine reports in index order). There was one separate shell write call to create this judgment artifact. Communication comprised one message to request the missing index and one wait. No project code or tests were executed in this phase. The earlier source-assessment phase used three inspection shell calls, one authorized evaluator-oracle execution call, and one artifact-write call. Thus the two review phases together used seven inspection calls, one evaluator execution call, and two artifact-write calls. These are observed reviewer calls, not inferred worker calls or costs.

Review-active time: UNAVAILABLE. No reliable active-time timer was observed, and waiting time must not be relabeled as active review time. Worker self-reported inspection counts were read but not independently audited. No numerical quality scores were assigned. Historical predeclaration, host isolation/compliance, real-world effectiveness, workload relevance, and exhaustive correctness remain unverified.
