from .reading import parse, instant
from .summary import summarize


class Ledger:
    def __init__(self):
        self._rows = {}

    def add(self, rows):
        parsed = [parse(row) for row in rows]
        self._rows.update({(row.sensor, row.at): row for row in parsed})

    def readings(self, sensor):
        return tuple(sorted(
            (row for row in self._rows.values() if row.sensor == sensor),
            key=lambda row: row.at,
        ))

    def summary(self, sensor, start, stop):
        start, stop = instant(start), instant(stop)
        if start >= stop:
            raise ValueError('summary window must have positive length')
        return summarize(
            row.celsius for row in self.readings(sensor)
            if start <= row.at < stop
        )
