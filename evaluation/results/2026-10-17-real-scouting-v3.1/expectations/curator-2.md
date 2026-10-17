This is a nonexhaustive expectation set for later investigation, not an audit or a finding of defects. Each candidate below is challengeable; no guaranteed bug is assumed.

**r3 — eventsourcing**

Observed public contracts:

- Applications save aggregate events, reconstruct state, and expose notifications; the worked example expects three notifications after three changes (`r3/README.md:63–98`). Default persistence is in memory, with SQLite available through configuration (`r3/README.md:101–120`).
- Stored events and snapshots support upward version migration before reconstruction (`r3/README.md:148–152`).
- Optimistic concurrency and reliable notification propagation are advertised capabilities (`r3/README.md:154–165`).
- The notification-log property explicitly promises events in recorded order (`r3/eventsourcing/application.py:657–660`).

Candidate boundaries worth investigating:

| Candidate | Observed source facts | Risk hypothesis and consequence |
|---|---|---|
| R3-A: Event commit → snapshots → notification | `save()` records events before taking snapshots and notifying (`r3/eventsourcing/application.py:770–775`). Snapshot configuration can raise after recording (`r3/eventsourcing/application.py:800–817`). | A downstream failure could leave durable events despite a failed save call, complicating retries or notification delivery. Investigate the documented recovery contract before treating this as a defect. |
| R3-B: Domain state → stored bytes → migrated object | Mapper encodes, compresses, then encrypts (`r3/eventsourcing/persistence.py:385–401`); reading reverses those transformations and applies sequential upcasters (`r3/eventsourcing/persistence.py:410–439`). | Configuration or schema changes could prevent historical reconstruction. Candidate scope: supported migrations, identifier conversion, and user-provided transcodings—not arbitrary compatibility with every model change. |

Suspicious but potentially valid designs and counterevidence:

- Reconstruction bypasses constructors using `object.__new__` and restored state (`r3/eventsourcing/persistence.py:438–439`). This can appropriately avoid replaying creation behavior; constructor bypass alone is not evidence of invalid state.
- Encryption covers serialized state, while identifier, version, and topic remain separate fields (`r3/eventsourcing/persistence.py:395–401`). Do not infer a promise to encrypt all metadata.
- Cache behavior is deliberately configurable, with fast-forward and defensive copying enabled by default in application construction (`r3/eventsourcing/application.py:743–753`). An explicitly relaxed configuration may have different consistency expectations.
- Custom transcodings and substituted persistence are advertised extension points (`r3/README.md:128–132`); missing registration produces explicit errors (`r3/eventsourcing/persistence.py:229–238,257–265`).

Accepted alternatives include reconstructing from events without snapshots, custom projectors for alternative event models, and application-managed retry/recovery after a committed write. These remain acceptable where their documented semantics meet the caller’s requirements; save-wide atomicity has not been established by this sample.

Abstain or clarify before alleging violations involving retry guarantees, snapshot atomicity, supported downgrade behavior, custom mapper obligations, or cache consistency under nondefault settings. Concrete backend transaction and concurrency behavior was not inspected.

**r4 — requests-cache**

Observed public contracts:

- `CachedSession` behaves like a Requests session with caching, and the quickstart promises reuse after the first fetch (`r4/README.md:50–77`).
- Matching uses normalized method, URL, parameters, and body (`r4/docs/user_guide/matching.md:3–4`).
- `Vary` combinations should be cached separately by default (`r4/docs/user_guide/matching.md:68–71`).
- Ignored parameters are excluded from matching and redacted from cached request data (`r4/docs/user_guide/matching.md:51–52`).
- Expiration has explicit precedence and normally applies to new responses rather than retroactively (`r4/docs/user_guide/expiration.md:16–30`). Stale responses may intentionally satisfy requests after errors (`r4/docs/user_guide/expiration.md:100–125`).
- `only_if_cached` promises a 504 instead of a new request when unavailable (`r4/requests_cache/session.py:175–178`).

Candidate boundaries worth investigating:

| Candidate | Observed source facts | Risk hypothesis and consequence |
|---|---|---|
| R4-A: Vary lookup → policy reevaluation → response selection | Session performs a secondary variant lookup and resets decision flags before reevaluation (`r4/requests_cache/session.py:227–244`). Policy combines availability, freshness, cache-only behavior, and Vary validation (`r4/requests_cache/policy/actions.py:208–238`). | Alternating variants combined with expiration or cache-only requests could select inappropriate content or contact the origin unexpectedly. The secondary lookup is explicit counterevidence against assuming variants are simply unsupported. |
| R4-B: Ignored credentials → request identity → stored representation | Documentation promises both redaction and exclusion from matching; it also promises refusal when an ignored header appears in `Vary` (`r4/docs/user_guide/security.md:18–29,58–60`). | Different identity and redaction paths could disagree, affecting confidentiality or reuse. Implementation of those paths was not sampled, so this is a contract-driven candidate only. |
| R4-C: Revalidation/error policy → session → persistence | Policy updates expiration and headers after revalidation and considers read-only, disabled, and no-store settings (`r4/requests_cache/policy/actions.py:276–307`). Session handles saving, 304 responses, and stale fallback (`r4/requests_cache/session.py:280–324,332–344`). | Branch interactions could return or persist inconsistent freshness/content metadata, or handle failures outside the intended stale policy. Investigate combinations before drawing conclusions. |

Suspicious but valid designs and accepted alternatives:

- Ignoring authentication information is deliberate for the intended private, single-user cache. Multi-principal isolation is explicitly an application concern (`r4/docs/user_guide/security.md:5–14,47–68`). Separate caches, excluding authenticated requests, or explicitly matching authentication headers are documented alternatives.
- An expired response may remain useful for validation or stale fallback; expiration does not universally mean “must delete” (`r4/docs/user_guide/expiration.md:38–47,100–125`).
- Broad exception handling during resend is paired with a usability decision and otherwise re-raises (`r4/requests_cache/session.py:323–344`). Catch breadth alone does not establish swallowed failures.
- Temporary cache disabling explicitly lacks thread safety (`r4/requests_cache/session.py:346–351`).
- Pickle’s trust requirement and alternative serializers are documented (`r4/docs/user_guide/security.md:82–97`); untrusted-cache safety cannot be assumed for every serializer.

Abstain or clarify when claims depend on public-proxy semantics, automatic tenant isolation, undocumented server behavior without `Vary`, custom key functions, or universal thread safety. Backend durability and serializer implementation require separate inspection.

**Actions and sampling limits**

I emitted the qualified tool-name inventory, listed files before reading contents, and worked alone using 12 inspection calls: one successful listing, seven bounded reads, three rejected argument attempts, and one search returning no results. Some multi-file output was truncated; only visible evidence supports the citations above.

No skills, upstream issues/history, Git metadata, credentials, or other sessions were inspected. No repository code, tests, builds, installations, edits, or network operations ran. Documentation and selected implementation paths were sampled; test protection and backend behavior remain unassessed.

**PROPOSED — NOT RUN:** Later reviewers could challenge R3-A/R3-B with controlled failure and historical reconstruction scenarios, and R4-A/R4-B/R4-C with variant, redaction, cache-only, and revalidation scenarios. These are investigation suggestions, not confirmed failures.