import unittest
from datetime import date, timedelta
from desk.service import Desk


class DeskTests(unittest.TestCase):
    def setUp(self):
        self.day = date(2026, 6, 9)
        self.desk = Desk()
        self.revision = self.desk.approve([('guard', 'Inspect guard'), ('lamp', 'Check lamp')])

    def test_generation_uses_approved_revision(self):
        sheet = self.desk.prepare(self.day, 'morning')
        self.assertEqual(sheet['revision'], self.revision)
        self.assertEqual(sheet['tasks'][0], ('guard', 'Inspect guard'))
        self.assertEqual(sheet['checked'], frozenset())
        self.assertFalse(sheet['complete'])

    def test_future_generation_uses_updated_wording(self):
        revision = self.desk.approve([('guard', 'Inspect and latch guard')])
        sheet = self.desk.prepare(self.day + timedelta(days=1), 'morning')
        self.assertEqual(sheet['revision'], revision)
        self.assertEqual(sheet['tasks'], (('guard', 'Inspect and latch guard'),))

    def test_repeat_generation_keeps_marks_and_distinct_shifts(self):
        first = self.desk.prepare(self.day, 'morning')
        self.desk.mark(self.day, 'morning', 'guard')
        again = self.desk.prepare(self.day, 'morning')
        evening = self.desk.prepare(self.day, 'evening')
        self.assertEqual(first['reference'], again['reference'])
        self.assertEqual(again['checked'], frozenset({'guard'}))
        self.assertNotEqual(first['reference'], evening['reference'])
        self.assertFalse(evening['checked'])

    def test_completion_preserves_history(self):
        original = self.desk.prepare(self.day, 'morning')
        with self.assertRaises(ValueError):
            self.desk.finish(self.day, 'morning')
        for task in ('guard', 'lamp'):
            self.desk.mark(self.day, 'morning', task)
        self.desk.finish(self.day, 'morning')
        self.desk.approve([('guard', 'New wording')])
        historical = self.desk.view(self.day, 'morning')
        self.assertEqual(historical['tasks'], original['tasks'])
        self.assertEqual(historical['revision'], original['revision'])
        with self.assertRaises(ValueError):
            self.desk.mark(self.day, 'morning', 'guard')

    def test_invalid_actions_do_not_change_approval(self):
        for tasks in ([], [('x', '')], [('x', 'A'), ('x', 'B')]):
            with self.assertRaises(ValueError):
                self.desk.approve(tasks)
        self.assertEqual(self.desk.prepare(self.day, 'morning')['revision'], self.revision)
        with self.assertRaises(ValueError):
            self.desk.prepare(self.day, 'night')
        with self.assertRaises(KeyError):
            self.desk.mark(self.day, 'morning', 'unknown')
        with self.assertRaises(ValueError):
            Desk().prepare(self.day, 'morning')


if __name__ == '__main__':
    unittest.main()
