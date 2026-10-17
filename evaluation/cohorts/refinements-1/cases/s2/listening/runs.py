from __future__ import annotations

from dataclasses import dataclass
from secrets import token_urlsafe
from .clock import utc


@dataclass(frozen=True)
class Completion:
    visitor: str
    exhibition: str
    tracks: tuple[str, ...]
    started_at: object
    finished_at: object


@dataclass
class Run:
    visitor: str
    admission: object
    started_at: object
    completion: Completion | None = None


class Runs:
    def __init__(self, licenses):
        self.licenses = licenses
        self._runs = {}

    def start(self, key, visitor, now):
        if not visitor.strip():
            raise ValueError('visitor is required')
        admission = self.licenses.admit(key, now)
        reference = token_urlsafe(24)
        self._runs[reference] = Run(visitor, admission, utc(now))
        return reference

    def finish(self, reference, now):
        now = utc(now)
        run = self._runs[reference]
        if now < run.started_at:
            raise ValueError('completion precedes admission')
        if run.completion is None:
            run.completion = Completion(
                run.visitor, run.admission.exhibition, run.admission.tracks,
                run.started_at, now,
            )
        return run.completion
