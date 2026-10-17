"""Check authored fixture semantics, not the effectiveness of an audit agent.

Fixture code is deliberately executed here during Gapline development. The
read-only skill must not attribute these runs to an investigation it performs.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evaluation" / "fixtures"
spec = importlib.util.spec_from_file_location(
    "prepare_fixture", ROOT / "evaluation" / "prepare_fixture.py"
)
preparation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preparation)


RUN_SELECTED_TESTS = """
import importlib.util
from pathlib import Path

for path in sorted(Path.cwd().glob('test_*.py')):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in sorted(vars(module)):
        if name.startswith('test_'):
            getattr(module, name)()
"""

INLINE_CACHE = """
import cache
import test_cache

def get(self, key):
    if key not in self._values:
        self._values[key] = self._fetch(key)
    return self._values[key]

cache.Lookup.get = get
"""


class FixtureSemanticsTests(unittest.TestCase):
    def run_case(self, case, program):
        bootstrap = "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd()))\n"
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", bootstrap + textwrap.dedent(program)],
            cwd=FIXTURES / case,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_authored_baselines_pass_even_where_checks_are_incomplete(self):
        for case in preparation.fixture_names():
            with self.subTest(case=case):
                self.run_case(case, RUN_SELECTED_TESTS)

    def test_overlap_violates_unique_recipient_contract(self):
        self.run_case("composition-unique", """
            from notifications import recipients
            result = recipients(['ada'], ['ada'])
            assert result == ['ada', 'ada']
            assert len(result) != len(set(result))
        """)

    def test_same_composition_preserves_required_repeated_deliveries(self):
        self.run_case("composition-repeated", """
            from notifications import recipients
            assert recipients(['ada', 'ada'], ['ada']) == ['ada', 'ada', 'ada']
        """)

    def test_contract_tests_tolerate_inlining_private_delegate(self):
        for case in ("cache-contract", "cache-private-calls"):
            with self.subTest(case=case):
                self.run_case(case, INLINE_CACHE + """
for name in sorted(vars(test_cache)):
    if name.startswith('test_') and name != 'test_lookup_calls_private_loader':
        getattr(test_cache, name)()
""")

    def test_private_call_expectation_rejects_the_same_valid_change(self):
        self.run_case("cache-private-calls", INLINE_CACHE + """
try:
    test_cache.test_lookup_calls_private_loader()
except AssertionError as error:
    assert 'Called 0 times' in str(error), str(error)
else:
    raise AssertionError('private-call test no longer exhibits the intended coupling')
""")

    def test_required_fetch_interaction_detects_lost_caching(self):
        self.run_case("cache-contract", """
            import cache
            import test_cache
            cache.Lookup.get = lambda self, key: self._fetch(key)
            try:
                test_cache.test_successful_value_is_fetched_once()
            except AssertionError as error:
                assert 'Called 2 times' in str(error), str(error)
            else:
                raise AssertionError('a required interaction went unchecked')
        """)

    def test_assertion_free_smoke_still_detects_lookup_exceptions(self):
        self.run_case("cache-contract", """
            import cache
            import test_cache
            def broken_get(self, key):
                raise RuntimeError('lookup unavailable')
            cache.Lookup.get = broken_get
            try:
                test_cache.test_construction_and_lookup_smoke()
            except RuntimeError as error:
                assert str(error) == 'lookup unavailable'
            else:
                raise AssertionError('the smoke test failed to observe execution failure')
        """)

    def test_both_boundaries_reject_direct_invalid_input(self):
        self.run_case("boundary-guards", """
            from orders import consume, submit
            for quantity in (0, 101, -1, True, '3'):
                for invoke in (lambda: submit(quantity), lambda: consume({'quantity': quantity})):
                    try:
                        invoke()
                    except ValueError:
                        pass
                    else:
                        raise AssertionError('an independent boundary accepted invalid input')
            assert consume({'quantity': 1}) == {'allocated': 1}
            assert consume({'quantity': 100}) == {'allocated': 100}
        """)

    def test_producer_guard_does_not_protect_independent_consumer(self):
        self.run_case("boundary-gap", """
            from orders import consume, submit
            try:
                submit(0)
            except ValueError:
                pass
            else:
                raise AssertionError('the producer no longer supplies the intended control')
            assert consume({'quantity': 0}) == {'allocated': 0}
        """)

    def test_advertised_sort_option_is_actually_ignored(self):
        self.run_case("option-current", """
            from reports import prepare
            names = ['Grace', 'Ada', 'Ada']
            result = prepare(names, sort_by_name=True)
            assert result == names
            assert result != sorted(names)
        """)

    def test_deferred_sorting_is_not_part_of_the_current_api(self):
        self.run_case("option-deferred", """
            from reports import prepare
            names = ['Grace', 'Ada', 'Ada']
            result = prepare(names)
            assert result == names and result is not names
            try:
                prepare(names, sort_by_name=True)
            except TypeError:
                pass
            else:
                raise AssertionError('the deferred option has become a current API')
        """)


class FixturePreparationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.fixtures = self.directory / "fixtures"
        self.source = self.fixtures / "example"
        self.source.mkdir(parents=True)
        self.patch = patch.object(preparation, "FIXTURES", self.fixtures)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.payload = b"# caf\xc3\xa9\r\nraise RuntimeError('must not execute')\r\n"
        (self.source / "code.py").write_bytes(self.payload)

    def test_prepares_only_selected_source_without_executing_it(self):
        (self.directory / "fixture_expectations.md").write_text("private answer")
        other = self.fixtures / "other"
        other.mkdir()
        (other / "answer.txt").write_text("other source")
        cache = self.source / "__pycache__"
        cache.mkdir()
        (cache / "code.pyc").write_bytes(b"generated")
        destination = self.directory / "trial"
        receipt = preparation.prepare_fixture("example", destination)
        worker = destination / "repository"
        self.assertEqual(
            {path.relative_to(worker).as_posix() for path in worker.rglob("*")},
            {"code.py"},
        )
        self.assertEqual((worker / "code.py").read_bytes(), self.payload)
        self.assertEqual((self.source / "code.py").read_bytes(), self.payload)
        self.assertEqual(receipt, json.loads((destination / "receipt.json").read_text()))
        self.assertEqual(receipt["files"], [{
            "path": "code.py",
            "size_bytes": len(self.payload),
            "sha256": hashlib.sha256(self.payload).hexdigest(),
        }])

    def test_identity_is_destination_independent_and_detects_bytes_and_names(self):
        first = preparation.prepare_fixture("example", self.directory / "one")
        same = preparation.prepare_fixture("example", self.directory / "two")
        self.assertEqual(first["tree_sha256"], same["tree_sha256"])
        (self.source / "code.py").write_bytes(self.payload + b"# changed\n")
        changed = preparation.prepare_fixture("example", self.directory / "three")
        self.assertNotEqual(first["tree_sha256"], changed["tree_sha256"])
        (self.source / "code.py").write_bytes(self.payload)
        (self.source / "code.py").rename(self.source / "renamed.py")
        renamed = preparation.prepare_fixture("example", self.directory / "four")
        self.assertNotEqual(first["tree_sha256"], renamed["tree_sha256"])

    def test_existing_trial_is_not_overwritten(self):
        destination = self.directory / "trial"
        destination.mkdir()
        marker = destination / "retained.txt"
        marker.write_text("retain me")
        with self.assertRaises(FileExistsError):
            preparation.prepare_fixture("example", destination)
        self.assertEqual(marker.read_text(), "retain me")
        self.assertFalse((destination / "repository").exists())

    def test_symlink_cannot_copy_evaluator_material(self):
        notes = self.directory / "answers.md"
        notes.write_text("private answer")
        try:
            (self.source / "README.md").symlink_to(notes)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is unavailable")
        destination = self.directory / "trial"
        with self.assertRaisesRegex(ValueError, "symlink"):
            preparation.prepare_fixture("example", destination)
        self.assertFalse(destination.exists())

    def test_dangling_destination_link_is_not_followed(self):
        destination = self.directory / "trial"
        target = self.directory / "elsewhere"
        try:
            destination.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is unavailable")
        with self.assertRaises(FileExistsError):
            preparation.prepare_fixture("example", destination)
        self.assertTrue(destination.is_symlink())
        self.assertFalse(target.exists())

    def test_unknown_or_traversing_case_does_not_create_output(self):
        for name in ("missing", "../example", "example/../example"):
            with self.subTest(name=name):
                destination = self.directory / "trial"
                with self.assertRaisesRegex(ValueError, "unknown fixture"):
                    preparation.prepare_fixture(name, destination)
                self.assertFalse(destination.exists())

    def test_output_cannot_be_nested_in_fixture_sources(self):
        destination = self.source / "trial"
        with self.assertRaisesRegex(ValueError, "outside the fixture collection"):
            preparation.prepare_fixture("example", destination)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
