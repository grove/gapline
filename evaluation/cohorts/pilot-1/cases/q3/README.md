# Offline change feed

`ChangeFeed` supplies ordered changes to a local offline client. Calls are
serialized by its adapter. Each `put(key, value)` or `delete(key)` appends a
revision, including repeated changes to the same key. Deletes are tombstones;
the client must apply all events in revision order. Values are dictionaries
with copyable contents; tombstones use `None`.

`begin(after, limit)` freezes a pull at the current revision. A page contains
`events`, an optional continuation token, and `checkpoint`. `resume(token,
limit)` continues that same frozen pull. Changes appended between pages are
excluded and must appear in a later pull. Clients persist `checkpoint` only
after applying the final page, even when intermediate pages display it.
Continuation tokens are trusted in-process values returned by this instance;
they are not serialized network input or a security boundary.

`compact(through)` drops events through that inclusive revision. A cursor or
continuation whose position is below that floor raises `CursorExpired`.
It must never silently skip retained history. The adapter handles this by
discarding local state and requesting a full snapshot from its separate
snapshot endpoint; that endpoint is outside this component. Compaction may
invalidate active pulls, so callers must handle expiration on every page.
The floor itself remains a valid starting position.

The feed is in memory, starts at revision zero, and is scoped to one adapter
session. Persistence, multiple writers, token transport, and snapshot storage
are supplied by other components. Run `python -m unittest discover -v`.
