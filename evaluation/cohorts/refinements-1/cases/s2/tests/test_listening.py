import unittest
from datetime import datetime, timedelta, timezone
from listening.licenses import Licenses
from listening.runs import Runs


class ListeningTests(unittest.TestCase):
    def setUp(self):
        self.open = datetime(2026, 4, 2, 10, tzinfo=timezone.utc)
        self.close = self.open + timedelta(hours=1)
        self.licenses = Licenses()
        self.licenses.add('gallery', self.open, self.close, ['intro', 'river'])
        self.runs = Runs(self.licenses)

    def test_window_edges(self):
        self.runs.start('gallery', 'Ari', self.open)
        self.runs.start('gallery', 'Bea', self.close - timedelta(microseconds=1))
        for instant in (self.open - timedelta(microseconds=1), self.close,
                        self.close + timedelta(days=1)):
            with self.assertRaises(PermissionError):
                self.runs.start('gallery', 'Cy', instant)

    def test_revocation_blocks_new_runs_but_preserves_admitted_runs(self):
        reference = self.runs.start('gallery', 'Ari', self.open)
        self.licenses.revoke('gallery')
        with self.assertRaises(PermissionError):
            self.runs.start('gallery', 'Bea', self.open)
        completed = self.runs.finish(reference, self.open + timedelta(minutes=20))
        self.assertEqual(completed.tracks, ('intro', 'river'))

    def test_finish_after_closure_is_supported_and_idempotent(self):
        reference = self.runs.start('gallery', 'Ari', self.open)
        first = self.runs.finish(reference, self.close + timedelta(hours=2))
        second = self.runs.finish(reference, self.close + timedelta(days=1))
        self.assertIs(first, second)
        self.assertEqual(first.finished_at, self.close + timedelta(hours=2))

    def test_admission_captures_track_list(self):
        old = self.runs.start('gallery', 'Ari', self.open)
        tracks = ['birds']
        self.licenses.replace_tracks('gallery', tracks)
        tracks.append('external')
        new = self.runs.start('gallery', 'Bea', self.open)
        self.assertEqual(self.runs.finish(old, self.close).tracks, ('intro', 'river'))
        self.assertEqual(self.runs.finish(new, self.close).tracks, ('birds',))

    def test_awareness_and_timezone_equivalence(self):
        local = self.open.astimezone(timezone(timedelta(hours=3)))
        reference = self.runs.start('gallery', 'Ari', local)
        self.assertEqual(self.runs.finish(reference, self.close).started_at, self.open)
        with self.assertRaises(ValueError):
            self.runs.start('gallery', 'Ari', self.open.replace(tzinfo=None))
        with self.assertRaises(ValueError):
            self.runs.finish(reference, self.close.replace(tzinfo=None))

    def test_validation_and_unknown_references(self):
        reference = self.runs.start('gallery', 'Ari', self.open)
        with self.assertRaises(ValueError):
            self.runs.finish(reference, self.open - timedelta(seconds=1))
        with self.assertRaises(KeyError):
            self.runs.finish('missing', self.close)
        with self.assertRaises(ValueError):
            self.runs.start('gallery', ' ', self.open)
        for tracks in ([], ['']):
            with self.assertRaises(ValueError):
                self.licenses.replace_tracks('gallery', tracks)
        for start, stop in ((self.close, self.open), (self.open, self.open)):
            with self.assertRaises(ValueError):
                self.licenses.add('other', start, stop, ['one'])
        with self.assertRaises(ValueError):
            self.licenses.add('gallery', self.open, self.close, ['one'])


if __name__ == '__main__':
    unittest.main()
