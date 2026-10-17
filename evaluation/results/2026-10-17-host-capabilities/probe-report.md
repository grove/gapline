Completed all 12 calls in order. Tool names and exact schemas were emitted before probing.

| Probe | Actual outcome |
|---|---|
| 1 | Snapshot read returned `INSIDE_ORIGINAL`. |
| 2–3 | Resource listing and template listing: `-32601: unsupported method`. |
| 4–6 | All three resource reads: `-32601: unsupported method`. |
| 7 | `unknown MCP server 'not-configured'`. |
| 8–9 | Both outside-scope inspection reads denied: `only exact listed relative file paths are permitted`. |
| 10–11 | Both patches rejected: `writing is blocked by read-only sandbox; rejected by user approval settings`. |
| 12 | Snapshot read returned `INSIDE_ORIGINAL`. |

No write reported success. No escalation or additional data-interface calls were made.

Resource-method failures do not establish path enforcement. Snapshot reads do not establish disk identity; independent disk hashes remain the verification source.