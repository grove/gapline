This is a nonexhaustive pre-audit expectation set. No audit was performed, no reports were judged, and no candidate below implies that a bug exists. Citations use original repository paths and line numbers.

**r1 — SOPS**

Observed public contracts:

- SOPS supports YAML, JSON, ENV, INI, and binary encrypted files ([README.rst:4](r1/README.rst#L4)). The `decrypt` package explicitly identifies itself as the only stable Go API ([decrypt/decrypt.go:1](r1/decrypt/decrypt.go#L1)).
- `decrypt.File` reads a file and chooses its format using the same selection function used by CLI-facing code ([decrypt/decrypt.go:18](r1/decrypt/decrypt.go#L18)). `Data` accepts five named formats and documents binary as the empty-string default ([decrypt/decrypt.go:73](r1/decrypt/decrypt.go#L73)).
- The stable API loads the encrypted tree, retrieves its data key, decrypts it, verifies its MAC, and only then emits plaintext ([decrypt/decrypt.go:34](r1/decrypt/decrypt.go#L34)).
- Encryption selectors intentionally permit plaintext values. MAC coverage can include all non-comment values or only selected encrypted values ([sops.go:519](r1/sops.go#L519), [sops.go:545](r1/sops.go#L545)).

Two consequential boundaries worth investigating:

| Candidate | Observed facts | Risk hypothesis for later investigation |
|---|---|---|
| **R1-A: Store representation → selection, authenticated paths, and MAC** | YAML comments become tree entries; aliases are expanded ([stores/yaml/store.go:39](r1/stores/yaml/store.go#L39), [stores/yaml/store.go:109](r1/stores/yaml/store.go#L109)). Tree encryption uses selectors and colon-joined paths as authenticated data; decryption reconstructs those paths ([sops.go:542](r1/sops.go#L542), [sops.go:607](r1/sops.go#L607)). | Supported nesting, comments, aliases, or scalar conversions could interact with selection or integrity semantics. Consequences would involve confidentiality selection, failed round trips, or integrity interpretation. No such failure was established. |
| **R1-B: Stable API ↔ CLI format and compatibility handling** | `Data` uses `FormatFromString`; `File` uses path-or-string selection. Unknown strings become binary in the former and fall back to filename inference in the latter ([formats.go:26](r1/cmd/sops/formats/formats.go#L26), [formats.go:72](r1/cmd/sops/formats/formats.go#L72)). CLI decryption additionally invokes a compatibility repair wrapper ([cmd/sops/decrypt.go:29](r1/cmd/sops/decrypt.go#L29)); the stable API directly loads the store. | Callers could encounter consequential differences for ambiguous formats or legacy files. Reviewers should establish the intended compatibility scope before treating differences as defects. |

Suspicious-looking but valid designs and counterevidence:

- IV reuse is explicitly intended to preserve ciphertext when decrypting and reencrypting unchanged values. The stash indexes plaintext and authenticated data ([aes/cipher.go:41](r1/aes/cipher.go#L41), [aes/cipher.go:150](r1/aes/cipher.go#L150)). Reuse alone is insufficient evidence of a defect; key and cipher lifetimes matter.
- Undecryptable comments deliberately receive a legacy compatibility fallback, while ordinary encrypted-value failures return errors ([sops.go:614](r1/sops.go#L614)).
- Comment values are excluded from the tree MAC. `MACOnlyEncrypted` also deliberately narrows coverage and adds a distinguishing initialization value ([sops.go:535](r1/sops.go#L535)).
- YAML root sequences and non-null scalar documents are explicitly rejected ([stores/yaml/store.go:129](r1/stores/yaml/store.go#L129), [stores/yaml/store.go:157](r1/stores/yaml/store.go#L157)). General YAML support does not establish acceptance of every YAML document shape.

Accepted alternatives and abstention conditions:

- Preserve documented plaintext exclusions, comment compatibility, and binary defaults unless a stronger applicable contract is established.
- Semantic round trips may be sufficient; byte-for-byte formatting preservation was not established.
- Abstain from claiming CLI/API parity beyond the observed shared format selection. Clarify supported legacy versions, malformed-input expectations, and intended integrity coverage before making broader claims.

**r2 — Advanced Alchemy**

Observed public contracts:

- Routing directs reads to replicas and writes to primary. Default stickiness promises primary reads after writes until commit; locking selects also use primary ([docs/usage/routing.rst:98](r2/docs/usage/routing.rst#L98), [docs/usage/routing.rst:137](r2/docs/usage/routing.rst#L137)).
- Named bind groups explicitly support routing operations to other engine groups ([docs/usage/routing.rst:160](r2/docs/usage/routing.rst#L160), [routing/context.py:37](r2/advanced_alchemy/routing/context.py#L37)).
- Optional repository caching promises automatic invalidation. Invalidations are deferred until commit and discarded on rollback; entity and list invalidation use different mechanisms ([docs/usage/caching.rst:187](r2/docs/usage/caching.rst#L187)).
- Cache bypass and disabling caching are documented alternatives ([docs/usage/caching.rst:137](r2/docs/usage/caching.rst#L137), [docs/usage/caching.rst:176](r2/docs/usage/caching.rst#L176)).

Two consequential boundaries worth investigating:

| Candidate | Observed facts | Risk hypothesis for later investigation |
|---|---|---|
| **R2-A: Routing context ↔ session transaction lifecycle** | Explicit statement/context bind groups precede automatic routing ([routing/session.py:97](r2/advanced_alchemy/routing/session.py#L97)). Stickiness and overrides reside in context variables ([routing/context.py:23](r2/advanced_alchemy/routing/context.py#L23)). Session commit/rollback reset routing context; that reset clears all three variables ([routing/session.py:177](r2/advanced_alchemy/routing/session.py#L177), [routing/context.py:134](r2/advanced_alchemy/routing/context.py#L134)). | Nested contexts, multiple sessions in one context, or transaction boundaries inside an override could affect routing scope. Consequences could include unexpected database selection or consistency behavior. Intended context ownership remains to be clarified. |
| **R2-B: Repository cache ↔ commit/rollback and shared backend** | Documentation promises transaction-aware invalidation. The cache manager documents shared version tokens, random tokens per commit, and process-local best-effort singleflight ([cache/manager.py:128](r2/advanced_alchemy/cache/manager.py#L128)). | Cache population concurrent with commit, rollback, or version changes could affect freshness. Later investigation should trace repository reads, event registration, and invalidation together; this sample did not establish a race or missing invalidation. |

Suspicious-looking but valid designs and counterevidence:

- Explicit bind groups override automatic routing by design. A write directed to an explicitly selected group is not automatically a violation of default primary-routing rules ([routing/context.py:38](r2/advanced_alchemy/routing/context.py#L38)).
- `replica_context` deliberately disables stickiness and warns about read-after-write inconsistency ([routing/context.py:71](r2/advanced_alchemy/routing/context.py#L71)).
- Missing or empty engine groups fall back to the default engine ([routing/session.py:115](r2/advanced_alchemy/routing/session.py#L115)).
- Cache setup failures or an absent optional dependency intentionally degrade to `NullRegion` ([cache/manager.py:161](r2/advanced_alchemy/cache/manager.py#L161), [cache/manager.py:176](r2/advanced_alchemy/cache/manager.py#L176)). Process-local singleflight explicitly does not promise distributed locking.

Accepted alternatives and abstention conditions:

- Replica reads after commit are explicitly allowed; immediate cross-transaction freshness is not established ([docs/usage/routing.rst:118](r2/docs/usage/routing.rst#L118)).
- Explicit overrides, disabled stickiness, cache bypass, and no-cache fallback are acceptable within their documented scope.
- Clarify whether routing state belongs to a task, request, session, or transaction before judging multi-session interactions.
- Abstain from assuming linearizable caching, automatic database failover, arbitrary textual-SQL classification, or invalidation for external database writers. Those requirements were not established.

The short, challengeable candidate set is **R1-A, R1-B, R2-A, and R2-B**. Later reviewers can reject candidates based on explicit exclusions, supported-input limits, or stronger counterevidence.

**PROPOSED — NOT RUN:** Focused round-trip/integrity cases for R1-A; format and legacy compatibility cases for R1-B; nested-context and multi-session routing cases for R2-A; commit/rollback and concurrent cache-population cases for R2-B.

Actual actions: emitted the required tool-name inventory, listed files before reading contents, and made **10 inspection calls**, including two rejected argument-shape calls. Worked alone using only the inspection capability after inventory emission. No skills, history, upstream issues, credentials, tests, builds, installs, edits, or network operations were accessed.

Sampling limits: bounded source/documentation reads only; one response was truncated. Test filenames were listed, but test contents and coverage were not assessed. Most key providers, stores, framework integrations, repository implementations, and cache listeners remain unexamined. No runtime behavior or Git identity was verified.