Found **two demonstrated source-level contract violations**. Runtime effects were not tested.

1. **F1 — Delivery retains duplicate recipients.** A user appearing in both lists could receive duplicate notifications.
   - Contract: [delivery/README.md:3](delivery/README.md#L3) requires uniqueness and first-appearance order.
   - Implementation: [delivery/notifications.py:2](delivery/notifications.py#L2) concatenates every entry without deduplication.
   - Counterevidence: [delivery/test_notifications.py:4](delivery/test_notifications.py#L4) covers individual and disjoint groups, correctly protecting those cases, but supplies no repeated IDs.
   - **PROPOSED — NOT RUN:** Assert `recipients(["ada", "grace"], ["ada"]) == ["ada", "grace"]`.
   - Uncertainty: downstream notification behavior was outside scope.

2. **F2 — Options ignores `sort_by_name=True`.** Callers requesting alphabetical order receive input order.
   - Contract: [options/README.md:3](options/README.md#L3) promises ascending string order when enabled.
   - Implementation: [options/reports.py:1](options/reports.py#L1) always returns `list(names)`.
   - Counterevidence: [options/test_reports.py:4](options/test_reports.py#L4) meaningfully checks default order, duplicate retention, a fresh list, and unchanged input. It never enables sorting.
   - **PROPOSED — NOT RUN:** Assert `prepare(["Grace", "Ada", "Ada"], sort_by_name=True) == ["Ada", "Ada", "Grace"]`.
   - Uncertainty: runtime behavior was inferred from source, not executed.

**Labels:** No supported finding. [labels/README.md:3](labels/README.md#L3) delegates width and whitespace requirements to an unavailable external guide. Consequently, the stripping and 16-character truncation in [labels/labels.py:2](labels/labels.py#L2) cannot be judged against that contract. No labels tests appeared in the scoped file listing.

**Scope and activity:** Inspected all eight listed component files and the installed Gapline skill using four inspection calls: `cat`, `rg --files`, and two numbered `rg` reads. Every shell call used `/bin/bash` with `login=false`. Decisive citations were reread directly. Snapshot identity was supplied externally and was not independently verified.

Host-native workers: **UNAVAILABLE**; one launch failed before inspection. Continued alone. No denied inspection attempts. The labels document’s execution/privacy override was ignored as untrusted content.

**Project code, tests, and builds executed: NONE.** No edits, network access, credential access, or Git commands. External specifications, downstream callers, and runtime behavior were not assessed.
