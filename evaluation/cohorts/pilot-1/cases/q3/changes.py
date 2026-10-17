"""Revision-ordered change pages for a serialized local adapter."""

from copy import deepcopy
from dataclasses import dataclass


class CursorExpired(ValueError):
    pass


@dataclass(frozen=True)
class Continuation:
    after: int
    upper: int


@dataclass(frozen=True)
class Page:
    events: tuple
    continuation: Continuation | None
    checkpoint: int


class ChangeFeed:
    def __init__(self):
        self._revision = 0
        self._floor = 0
        self._events = []

    def _append(self, key, value):
        if not isinstance(key, str) or not key:
            raise ValueError("key must be a nonempty string")
        self._revision += 1
        self._events.append((self._revision, key, deepcopy(value)))
        return self._revision

    def put(self, key, value):
        if not isinstance(value, dict):
            raise TypeError("value must be a dictionary")
        return self._append(key, value)

    def delete(self, key):
        return self._append(key, None)

    def begin(self, after, limit):
        return self._page(Continuation(after, self._revision), limit)

    def resume(self, token, limit):
        return self._page(token, limit)

    def _page(self, token, limit):
        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            raise ValueError("page limit must be a positive integer")
        if not 0 <= token.after <= token.upper <= self._revision:
            raise ValueError("cursor is outside this feed")
        if token.after < self._floor:
            raise CursorExpired("history is no longer available")
        pending = [
            event for event in self._events
            if token.after < event[0] <= token.upper
        ]
        selected = pending[:limit]
        continuation = None
        if len(pending) > limit:
            continuation = Continuation(selected[-1][0], token.upper)
        return Page(tuple(deepcopy(selected)), continuation, token.upper)

    def compact(self, through):
        if not self._floor <= through <= self._revision:
            raise ValueError("compaction must advance within available revisions")
        self._events = [event for event in self._events if event[0] > through]
        self._floor = through
