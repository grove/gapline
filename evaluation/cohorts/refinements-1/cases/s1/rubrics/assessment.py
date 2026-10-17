from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class Assessment:
    student: str
    edition: int
    scores: tuple[tuple[str, int], ...]


class Assessments:
    def __init__(self, catalog):
        self.catalog = catalog
        self._records = {}

    def record(self, reference, student, edition, scores):
        if reference in self._records:
            raise ValueError('assessment already exists')
        if not student.strip():
            raise ValueError('student is required')
        snapshot = tuple(scores.items())
        self._percentage(edition, dict(snapshot))
        self._records[reference] = Assessment(student, edition, snapshot)

    def _percentage(self, number, scores):
        criteria = self.catalog.get(number).criteria
        if set(scores) != {row.key for row in criteria}:
            raise ValueError('scores do not match edition')
        for row in criteria:
            value = scores[row.key]
            if type(value) is not int or not 0 <= value <= row.maximum:
                raise ValueError('score outside criterion range')
        total = sum(scores.values())
        maximum = sum(row.maximum for row in criteria)
        return (Decimal(total) * 100 / maximum).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    def percentage(self, reference):
        record = self._records[reference]
        return self._percentage(record.edition, dict(record.scores))
