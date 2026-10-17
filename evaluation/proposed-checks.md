# Proposed-check planning controls (#14)

These are **authored development controls**, inspected and checked by the
implementing agent. They are not unseen audit cases, independent review, a
host/model comparison, or pg-trickle reproductions. No target-project runtime
failure has been reproduced. **Efficacy of the guidance remains unproven.**

Expected improvement: catch infeasible inputs and
overrestrictive oracles during the existing planning pass, without adding a
report template, model stage, or runtime tool. Preserve #7's simplification,
the three-finding ceiling, read-only audits, and direct documentation fixes.

The shipped change is one risk-triggered paragraph in the existing Probe step
and short optional examples in the existing test-protection recipe. Unknown
harness behavior stays an evidence gap. An executable recipe remains
**PROPOSED — NOT RUN** and never strengthens the underlying finding by itself.

## Controls and handoffs

The definitions and executable semantic checks are in
[test_proposed_checks.py](../tests/test_proposed_checks.py). These small models
exercise the planning mistakes, not PostgreSQL permissions, MVCC, transactions,
locks, or a target project's snapshot implementation.

1. **Primary key versus NULL.** The authored SQLite table has a non-null primary
   key `id` and nullable `value`; rows include NULL, 1, and 2 in `value`.
   The suspected wrong rewrite replaces ordinary negated equality with a
   null-safe inequality.
   Rejected handoff: compare the two predicates on `id`; both select the same
   rows, so the NULL boundary is missed. Inserting a NULL key is rejected.
   Corrected handoff, **PROPOSED — NOT RUN** in an audit: use the nullable
   operand and assert the exact selected IDs. Ordinary negation excludes the
   NULL row; the wrong rewrite includes it. Ordinary `<>` is an accepted
   alternate repair. SQLite is only the authored SQL control, not evidence of
   a PostgreSQL defect or equivalence across SQL dialects.

2. **Caller selects the snapshot branch.** In the authored `snapshot_path`,
   `owner` takes the direct shortcut and `reader` reaches the snapshot branch.
   Rejected handoff: use the privileged owner and assume snapshot creation is
   covered. Corrected handoff, **PROPOSED — NOT RUN**: use the inspected reader
   path with valid size 2; verify branch reachability before proposing a pause.
   The model has no database grants or session setup. If those are unknown in
   an actual audit, disclose the missing seam rather than claim an executable
   reproducer. Branch selection alone establishes no snapshot defect.

3. **Serialization-safe interleaving.** The authored state is a generation and
   matching payload. Pause the snapshot after its first observation, then
   attempt refresh in another thread. The contract permits either atomic
   capture or serialization; a mixed `(0, 1)` snapshot violates it.
   Rejected handoff: require refresh to commit before releasing the pause. A
   correct serializing repair blocks there, so this harness can hang.
   Corrected handoff, **PROPOSED — NOT RUN**: wait a bounded interval for refresh,
   release the pause whether refresh committed or blocked, bound both joins,
   then check consistency and refresh completion. The control distinguishes a
   torn snapshot from both atomic capture and a serializing repair. Failure to
   reach the schedule or complete operations is a harness/behavior uncertainty,
   not proof of the suspected race. An actual target also needs inspected
   transaction/session rules and a usable pause seam.

4. **Minimum-size guard refutes the fallback lead.** The same authored dispatch
   rejects sizes below 2 before its apparent size-1 fallback.
   Rejected handoff: force size 1 to demonstrate that fallback's bad result.
   Correct outcome: withdraw the lead for this entry point; the guard prevents
   the claimed path. Do not bypass it or invent a runtime finding. Other entry
   points would require separate inspection. No executable follow-up is needed.

5. **Direct documentation contradiction.** The existing
   [README](fixtures/doc-drift/README.md) promises two retries by default;
   [the constructor](fixtures/doc-drift/client.py) explicitly defaults to zero.
   Correct handoff: reconcile that text with the authoritative intended default.
   This is a demonstrated source/document mismatch, not a runtime receipt.
   No request failure, concurrency harness, or mandatory test plan is needed.
   The control reads the two sources without importing or executing the client.

## Validation and limits

Run the authored controls in the development checkout:

```sh
python3 -B -m unittest discover -s tests -p test_proposed_checks.py -v
```

The implementing agent ran all five controls successfully. The intentionally
bad recipes remain recorded above: the primary-key recipe cannot distinguish
the wrong predicate, the owner misses the snapshot path, and requiring commit
before release excludes a valid serializing implementation. The size guard
refutes the fallback concern, and the documentation control needs only reads.
These are controlled semantic results, not generated handoffs or measured
developer benefit. Concise corrected handoffs are authored here; their quality
in actual model reports has not been compared.

The full development suite passed all 63 tests with Python 3.12. The first run
used the host's default Python 3.9.6 and failed the existing pilot oracle because
its `Continuation | None` annotation needs a newer interpreter; all five new
controls passed in that run. No frozen fixture was changed to accommodate it.
The installer check with Node 26.12.0 and skills CLI 1.7.2 also passed all three
payload files and local links for Codex and Claude Code, in copy and symlink
modes. Installation checks do not establish host activation or audit quality.

The historical scouting variants and all prior receipts remain unchanged.
Their regression test now checks the frozen cohort identity rather than
requiring future production wording to equal the historical baseline.
Package instruction-presence checks still establish only declared structure.
No model sessions, target-project tests, new audit execution permissions, or
efficacy comparison were added or run; #7's completed experiment stays closed.
