import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from fieldlog.ledger import Ledger
from fieldlog.reading import parse
from fieldlog.summary import Summary


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.start = datetime(2026, 5, 1, tzinfo=timezone.utc)
        self.stop = self.start + timedelta(days=1)
        self.ledger = Ledger()

    def row(self, value, *, sensor='north', at=None, unit='C'):
        return sensor, self.start if at is None else at, value, unit

    def test_celsius_fahrenheit_and_absolute_zero(self):
        self.assertEqual(parse(self.row(32, unit='F')).celsius, 0)
        self.assertEqual(parse(self.row(212, unit='F')).celsius, 100)
        self.assertEqual(parse(self.row(-273.15)).celsius, -273.15)
        self.assertAlmostEqual(parse(self.row(-459.67, unit='F')).celsius, -273.15)

    def test_invalid_values_names_units_and_time(self):
        for value in (True, False, '12', None, float('nan'), float('inf'),
                      float('-inf'), -274, 1001, 10**1000, -(10**1000)):
            with self.assertRaises(ValueError, msg=repr(value)):
                parse(self.row(value))
        for sensor in ('', '  ', 42):
            with self.assertRaises(ValueError):
                parse(self.row(10, sensor=sensor))
        for unit in ('c', 'K', ''):
            with self.assertRaises(ValueError):
                parse(self.row(10, unit=unit))
        with self.assertRaises(ValueError):
            parse(self.row(10, at=self.start.replace(tzinfo=None)))

    def test_summary_interval_and_sensor_isolation(self):
        self.ledger.add([
            self.row(99, at=self.start - timedelta(seconds=1)),
            self.row(0), self.row(20, at=self.start + timedelta(hours=2)),
            self.row(88, at=self.stop), self.row(1000, sensor='south'),
        ])
        self.assertEqual(self.ledger.summary('north', self.start, self.stop),
                         Summary(2, 0, 20, 10))
        self.assertEqual(self.ledger.summary('none', self.start, self.stop),
                         Summary(0, None, None, None))

    def test_replacement_timezone_equivalence_and_same_batch_last_wins(self):
        local = self.start.astimezone(timezone(timedelta(hours=-4)))
        self.ledger.add([self.row(1), self.row(2), self.row(32, at=local, unit='F')])
        rows = self.ledger.readings('north')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].at, self.start)
        self.assertEqual(rows[0].celsius, 0)
        self.ledger.add([self.row(8)])
        self.assertEqual(self.ledger.readings('north')[0].celsius, 8)

    def test_atomic_batches_and_empty_batch(self):
        self.ledger.add([self.row(1)])
        before = self.ledger.readings('north')
        with self.assertRaises(ValueError):
            self.ledger.add([self.row(9), self.row(float('nan'), sensor='south')])
        self.assertEqual(self.ledger.readings('north'), before)
        self.ledger.add([])
        self.assertEqual(self.ledger.readings('north'), before)

    def test_order_and_immutable_results(self):
        later = self.start + timedelta(hours=1)
        self.ledger.add([self.row(20, at=later), self.row(10)])
        rows = self.ledger.readings('north')
        self.assertEqual([row.at for row in rows], [self.start, later])
        with self.assertRaises(FrozenInstanceError):
            rows[0].celsius = 999
        result = self.ledger.summary('north', self.start, self.stop)
        with self.assertRaises(FrozenInstanceError):
            result.mean = 999

    def test_supported_upper_bounds_and_large_batch_summary(self):
        self.assertEqual(parse(self.row(1000)).celsius, 1000)
        self.assertEqual(parse(self.row(1832, unit='F')).celsius, 1000)
        for value in (-460, 1833, 1e308, 10**1000):
            with self.assertRaises(ValueError):
                parse(self.row(value, unit='F'))
        self.ledger.add([
            self.row(1000, at=self.start + timedelta(seconds=index))
            for index in range(1024)
        ])
        result = self.ledger.summary('north', self.start, self.stop)
        self.assertEqual(result, Summary(1024, 1000, 1000, 1000))

    def test_bad_windows_and_equivalent_timezone_bounds(self):
        for start, stop in ((self.stop, self.start), (self.start, self.start),
                            (self.start.replace(tzinfo=None), self.stop),
                            (self.start, self.stop.replace(tzinfo=None))):
            with self.assertRaises(ValueError):
                self.ledger.summary('north', start, stop)
        local_start = self.start.astimezone(timezone(timedelta(hours=2)))
        self.ledger.add([self.row(12)])
        self.assertEqual(self.ledger.summary('north', local_start, self.stop).count, 1)


if __name__ == '__main__':
    unittest.main()
