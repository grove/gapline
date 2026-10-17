from __future__ import annotations

from dataclasses import dataclass
from math import fsum


@dataclass(frozen=True)
class Summary:
    count: int
    minimum: float | None
    maximum: float | None
    mean: float | None


def summarize(values):
    values = tuple(values)
    if not values:
        return Summary(0, None, None, None)
    return Summary(len(values), min(values), max(values), fsum(values) / len(values))
