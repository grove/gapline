This is a nonexhaustive expectation set, not an audit or a finding list. No guaranteed bug is assumed. Citations use original supplied paths and line numbers.

**Files listed first:** the initial inspection returned the complete supplied file inventory for r1 and r2. Sampling then focused on public documentation and the implementation boundaries below.

**r1 — SOPS**

Observed public contracts:

- SOPS supports YAML, JSON, ENV, INI and binary files with several key providers (`r1/README.rst:4–5`).
- The `decrypt` package explicitly identifies itself as the only stable Go API (`r1/decrypt/decrypt.go:1–3`). `Data` documents its accepted formats and binary default (`r1/decrypt/decrypt.go:73–79`).
- That API decrypts the tree, verifies its stored MAC and only then emits plaintext (`r1/decrypt/decrypt.go:48–70`).
- Tree encryption deliberately supports selective plaintext and two MAC scopes: all non-comment values or encrypted values only (`r1/sops.go:519–530`, `545–552`).

Challengeable candidate boundaries:

| Candidate | Observed basis | Risk hypothesis worth investigating |
|---|---|---|
| R1-A: stores → tree → integrity verification | Tree paths become authenticated additional data; leaf values feed the MAC (`r1/sops.go:545–558`, `613–645`). | Supported format conversions or unusual keys/types might alter the semantic material authenticated or emitted. Establish supported round-trip semantics before assessing any discrepancy. |
| R1-B: selection rules/comments → encryption and decryption | Both directions use `shouldBeEncrypted`; comment-decryption failures retain the comment for older-file compatibility (`r1/sops.go:544`, `609–624`). | Comment placement or selector interactions might change which substantive values receive encryption or MAC coverage. Compatibility behavior alone is not evidence of failure. |
| R1-C: key groups → key services → recovered data key | One group wraps the full key; multiple groups use Shamir shares. Recovery accepts a successful key within each group and combines recovered shares (`r1/sops.go:783–805`, `858–880`, `887–904`). | Partial provider failures or malformed group metadata might produce unexpected recovery/update behavior. Investigate caller error handling and metadata validation before drawing conclusions. |

Suspicious-looking but intentional designs and accepted alternatives:

- IV reuse is explicitly intended to preserve ciphertext for unchanged values (`r1/aes/cipher.go:41–45`, `149–158`). Any cryptographic investigation must establish actual key, plaintext and additional-data reuse conditions.
- Comments are excluded from the tree MAC, and legacy plaintext comments are tolerated (`r1/sops.go:545–552`, `614–624`). Universal comment authentication is not an established requirement.
- CLI helpers explicitly support `IgnoreMac`; the stable decrypt API checks integrity unconditionally (`r1/cmd/sops/common/common.go:78–79`, `94–106`; `r1/decrypt/decrypt.go:58–68`).
- Encrypted-only MAC scope is an explicit alternative, with a distinct hash initialization (`r1/sops.go:535–539`).

Abstain or clarify when a claim depends on byte-for-byte formatting preservation, authenticating every comment, stability of internal Go APIs, or provider availability guarantees. Those requirements were not established by this sample.

**r2 — Advanced Alchemy**

Observed public contracts:

- Publicly advertised capabilities include sync/async CRUD, composite keys, replica routing, caching and optional file lifecycle hooks (`r2/README.md:35–45`).
- Routing documentation promises writes and locking reads use primary, with default stickiness after writes until commit (`r2/docs/usage/routing.rst:98–143`).
- Bulk upserts document native dispatch for suitable unique match keys, otherwise a portable fallback (`r2/docs/usage/repositories/basics.rst:129–133`, `176–194`).
- File lifecycle tracking exposes explicit strict-versus-warning failure handling (`r2/advanced_alchemy/types/file_object/session_tracker.py:25–36`).

Challengeable candidate boundaries:

| Candidate | Observed basis | Risk hypothesis worth investigating |
|---|---|---|
| R2-A: repository options/context → routing session → transaction | Explicit groups precede automatic routing; write classification sets context-based stickiness; commit/rollback reset routing state (`r2/advanced_alchemy/routing/session.py:97–113`, `145–186`). | Nested contexts, multiple sessions in one context, or explicit groups might interact unexpectedly with consistency expectations. Clarify override precedence and state ownership first. |
| R2-B: model metadata/input rows → upsert strategy → hydration | The async repository resolves strategy, chooses fallback for several conditions, propagates bind options and copies returned primary keys (`r2/advanced_alchemy/repository/_async.py:2934–3008`). | Native and fallback paths might differ in omitted-field preservation, duplicate-key handling, result correspondence or routing. Documentation supplies concrete expectations, but helper bodies remain unexamined. |
| R2-C: database lifecycle → file tracker → external storage | Optional automatic hooks are advertised; tracker commit methods perform saves/deletes and offer configurable failure propagation (`r2/README.md:43–45`; `r2/advanced_alchemy/types/file_object/session_tracker.py:62–85`, `87–154`). | Partial storage failure, cancellation or retry might leave database/file state requiring reconciliation. Establish event wiring and recovery guarantees before assessing behavior. |

Suspicious-looking but valid designs and accepted alternatives:

- Explicit bind groups intentionally override automatic routing; missing/empty groups fall back to the default engine (`r2/advanced_alchemy/routing/context.py:37–42`; `r2/advanced_alchemy/routing/session.py:115–131`).
- Replica reads after commit are documented, and stickiness can be disabled. Post-commit replica freshness is therefore not established (`r2/docs/usage/routing.rst:118–131`).
- `no_merge=True` deliberately selects portable upserts. SQL Server and fallback concurrency explicitly rely on uniqueness constraints and caller retries rather than missing-key gap locking (`r2/docs/usage/repositories/basics.rst:195–217`).
- File failures may intentionally log and continue; missing files during deletion are tolerated (`r2/advanced_alchemy/types/file_object/session_tracker.py:25–30`, `74–83`).

Abstain or clarify when a claim requires cross-resource atomicity, automatic transaction retries, post-commit replica consistency, session-local routing state, or precedence between explicit groups and primary-forcing contexts. These need requirements or further evidence.

**Actions and limits:** worked alone; emitted the requested host-tool inventory before reading files; used exactly 12 inspection calls: one listing, two searches and nine bounded reads. Clock observations spanned 25 seconds. No skills, history, issues, credentials, network access, code execution, test collection/runs, builds, installs or edits were used. Some batched output was truncated; unseen portions were not treated as evidence. Test files were listed but not read, so this establishes no test-protection conclusions.

**PROPOSED — NOT RUN:** later reviewers could challenge these six candidates with narrowly scoped round-trip, provider-failure, routing-context, upsert-equivalence and file-lifecycle scenarios. The candidate set is deliberately limited and does not rank confirmed defects.