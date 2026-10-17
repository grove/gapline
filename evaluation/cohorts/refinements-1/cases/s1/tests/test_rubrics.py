import unittest
from decimal import Decimal
from rubrics.editor import Draft
from rubrics.catalog import Catalog
from rubrics.assessment import Assessments


class RubricTests(unittest.TestCase):
    def setUp(self):
        self.draft = Draft('Observational drawing')
        self.draft.add('shape', 'Shape', 10)
        self.draft.add('tone', 'Tone', 20)
        self.catalog = Catalog()
        self.number = self.catalog.publish(self.draft)
        self.results = Assessments(self.catalog)

    def test_weighted_percentage_and_score_copy(self):
        scores = {'shape': 5, 'tone': 15}
        self.results.record('a', 'Rae', self.number, scores)
        scores['shape'] = 0
        self.assertEqual(self.results.percentage('a'), Decimal('66.67'))

    def test_adding_removing_and_title_edits_leave_edition_structure(self):
        self.draft.title = 'Composition'
        self.draft.remove('shape')
        self.draft.add('space', 'Space', 15)
        description = self.catalog.describe(self.number)
        self.assertEqual(description['title'], 'Observational drawing')
        self.assertEqual([row['key'] for row in description['criteria']], ['shape', 'tone'])
        second = self.catalog.publish(self.draft)
        self.assertEqual(second, self.number + 1)
        self.assertEqual(self.catalog.describe(second)['title'], 'Composition')

    def test_description_does_not_allow_external_changes(self):
        view = self.catalog.describe(self.number)
        view['criteria'][0]['maximum'] = 1000
        self.assertEqual(self.catalog.describe(self.number)['criteria'][0]['maximum'], 10)

    def test_validation_preserves_draft(self):
        for maximum in (0, -1, True, 2.5):
            with self.assertRaises(ValueError):
                self.draft.revise('shape', maximum=maximum)
        with self.assertRaises(ValueError):
            self.draft.revise('shape', name=' ')
        self.assertEqual(self.catalog.describe(self.number)['criteria'][0]['maximum'], 10)
        with self.assertRaises(KeyError):
            self.draft.revise('unknown', maximum=10)
        with self.assertRaises(KeyError):
            self.draft.remove('unknown')

    def test_bad_scores_and_duplicate_records(self):
        for scores in ({'shape': 1}, {'shape': 11, 'tone': 0},
                       {'shape': True, 'tone': 0}, {'shape': -1, 'tone': 0}):
            with self.assertRaises(ValueError):
                self.results.record('bad', 'Rae', self.number, scores)
        self.results.record('ok', 'Rae', self.number, {'shape': 10, 'tone': 20})
        with self.assertRaises(ValueError):
            self.results.record('ok', 'Rae', self.number, {'shape': 0, 'tone': 0})

    def test_empty_and_duplicate_criteria(self):
        with self.assertRaises(ValueError):
            self.catalog.publish(Draft('Empty'))
        with self.assertRaises(ValueError):
            self.draft.add('shape', 'Again', 1)
        with self.assertRaises(ValueError):
            self.draft.add('x', 'X', 0)


if __name__ == '__main__':
    unittest.main()
