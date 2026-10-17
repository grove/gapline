import io
import json
import unittest
from contextlib import redirect_stdout, redirect_stderr
from tileplan.options import Options
from tileplan.layout import arrange
from tileplan.cli import main


class TileTests(unittest.TestCase):
    def test_full_rows_and_partial_row(self):
        plan = arrange(Options(5, 80, 60, 3, 5))
        self.assertEqual((plan.width, plan.height), (250, 125))
        self.assertEqual([(tile.x, tile.y) for tile in plan.tiles],
                         [(0, 0), (85, 0), (170, 0), (0, 65), (85, 65)])
        self.assertEqual([tile.index for tile in plan.tiles], list(range(5)))
        self.assertTrue(all((tile.width, tile.height) == (80, 60) for tile in plan.tiles))

    def test_no_extra_columns_or_border(self):
        plan = arrange(Options(2, 10, 20, 9, 3))
        self.assertEqual((plan.width, plan.height), (23, 20))
        single = arrange(Options(1, 10, 20, 9, 100))
        self.assertEqual((single.width, single.height), (10, 20))

    def test_empty_default_and_zero_spacing(self):
        empty = arrange(Options(0, 10, 20))
        self.assertEqual((empty.width, empty.height, empty.tiles), (0, 0, ()))
        default = arrange(Options(4, 10, 20))
        self.assertEqual((default.width, default.height), (46, 48))
        touching = arrange(Options(4, 10, 20, 2, 0))
        self.assertEqual((touching.width, touching.height), (20, 40))

    def test_invalid_values(self):
        for values in ((-1, 10, 20, 3, 8), (1, 0, 20, 3, 8),
                       (1, 10, -1, 3, 8), (1, 10, 20, 0, 8),
                       (1, 10, 20, 3, -1), (True, 10, 20, 3, 8),
                       (1, 10.0, 20, 3, 8)):
            with self.assertRaises(ValueError):
                Options(*values)

    def test_cli_pixel_geometry(self):
        output = io.StringIO()
        with redirect_stdout(output):
            main(['--count', '2', '--width', '10', '--height', '20', '--spacing', '5'])
        result = json.loads(output.getvalue())
        self.assertEqual(result['width'], 25)
        self.assertEqual(result['tiles'][1]['x'], 15)
        self.assertEqual(result['tiles'][0]['width'], 10)

    def test_cli_defaults_and_failure_streams(self):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output):
            main(['--count', '2', '--width', '10', '--height', '20'])
        self.assertEqual(json.loads(output.getvalue())['width'], 28)
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            with self.assertRaises(SystemExit) as failure:
                main(['--count', '-1', '--width', '10', '--height', '20'])
        self.assertEqual(failure.exception.code, 2)
        self.assertEqual(output.getvalue(), '')
        self.assertIn('nonnegative', errors.getvalue())


if __name__ == '__main__':
    unittest.main()
