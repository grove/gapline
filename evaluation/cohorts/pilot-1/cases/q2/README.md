# Batch task leases

`BatchQueue` coordinates workers for one bounded in-memory import batch. The
adapter serializes calls and supplies nondecreasing monotonic timestamps in
seconds. Persistence, cross-process locking, and an unbounded service lifetime
are outside its scope. A new import batch gets a new queue instance.

`enqueue(key, payload)` accepts a nonempty string key and returns a job ID.
The key identifies the operation for the **entire lifetime of this batch**,
including after completion. Repeating it with an equal payload returns the
same job ID and preserves its status and result; a different payload is a
conflict. To request another operation, the caller must use another key.
Payloads and results are ordinary copyable Python values.

`reserve(owner, now, ttl)` leases the oldest eligible job and returns its ID,
payload, and a fresh token, or `None`. At `now == deadline` a lease is expired.
Expired jobs may be leased again. `finish(job_id, token, result, now)` succeeds
only for the current, unexpired lease, then marks the job done. A stale token
must not finish a reissued lease, even if the original worker eventually
returns. Completion does not enqueue another attempt or release the key.

`inspect(job_id)` returns a detached status snapshot. Callers cannot mutate
the queue by changing submitted payloads, reserved payloads, or results.
Owner names are diagnostic; tokens establish lease ownership.

Run the public checks with `python -m unittest discover -v`.
