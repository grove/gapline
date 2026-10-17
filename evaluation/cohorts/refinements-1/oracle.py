"""Evaluator-only checks. Never place this file in a worker-visible case tree."""
import ast
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def verify_inventory(manifest):
    actual = {str(path.relative_to(ROOT)) for path in (ROOT / 'cases').rglob('*') if path.is_file()}
    expected = {entry['path'] for case in manifest['cases'] for entry in case['files']}
    assert actual == expected, (actual - expected, expected - actual)
    for case in manifest['cases']:
        for entry in case['files']:
            content = (ROOT / entry['path']).read_bytes()
            assert len(content) == entry['size_bytes'], entry['path']
            assert hashlib.sha256(content).hexdigest() == entry['sha256'], entry['path']


def rubric_boundary():
    sys.path.insert(0, str(ROOT / 'cases/s1'))
    from rubrics.editor import Draft
    from rubrics.catalog import Catalog
    from rubrics.assessment import Assessments
    draft, catalog = Draft('Drawing'), Catalog()
    draft.add('line', 'Line control', 10)
    version = catalog.publish(draft)
    results = Assessments(catalog)
    results.record('r', 'Rae', version, {'line': 10})
    assert results.percentage('r') == Decimal('100.00')
    draft.revise('line', maximum=20, name='Line quality')
    assert catalog.describe(version)['criteria'][0]['maximum'] == 20
    assert catalog.describe(version)['criteria'][0]['name'] == 'Line quality'
    assert results.percentage('r') == Decimal('50.00')
    draft.add('space', 'Space', 5)
    assert len(catalog.describe(version)['criteria']) == 1
    assert catalog.describe(catalog.publish(draft))['criteria'][0]['maximum'] == 20


def listening_policy():
    sys.path.insert(0, str(ROOT / 'cases/s2'))
    from listening.licenses import Licenses
    from listening.runs import Runs
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    stop = start + timedelta(hours=1)
    licenses = Licenses()
    licenses.add('room', start, stop, ['old'])
    runs = Runs(licenses)
    reference = runs.start('room', 'Ari', start)
    licenses.replace_tracks('room', ['new'])
    licenses.revoke('room')
    completion = runs.finish(reference, stop + timedelta(hours=5))
    assert completion.tracks == ('old',)
    assert completion is runs.finish(reference, stop + timedelta(days=1))
    try:
        runs.start('room', 'Bea', start)
    except PermissionError:
        pass
    else:
        raise AssertionError('revoked license admitted a new visitor')
    licenses.add('boundary', start, stop, ['one'])
    runs.start('boundary', 'Cy', start)
    try:
        runs.start('boundary', 'Cy', stop)
    except PermissionError:
        pass
    else:
        raise AssertionError('closing boundary admitted a visitor')


def sensor_controls():
    sys.path.insert(0, str(ROOT / 'cases/s3'))
    from fieldlog.ledger import Ledger
    ledger = Ledger()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    stop = start + timedelta(hours=1)
    ledger.add([('a', start, 32, 'F'), ('a', stop, 99, 'C'), ('b', start, 12, 'C')])
    result = ledger.summary('a', start, stop)
    assert (result.count, result.minimum, result.maximum, result.mean) == (1, 0, 0, 0)
    before = ledger.readings('a')
    try:
        ledger.add([('a', start, 10, 'C'), ('b', start, float('nan'), 'C')])
    except ValueError:
        pass
    else:
        raise AssertionError('invalid batch accepted')
    assert ledger.readings('a') == before
    equivalent = start.astimezone(timezone(timedelta(hours=4)))
    ledger.add([('a', equivalent, 20, 'C')])
    assert len(ledger.readings('a')) == 2
    assert ledger.summary('a', start, stop).mean == 20
    for value, unit in ((1e308, 'F'), (10**1000, 'C'), (1001, 'C'), (1833, 'F')):
        try:
            ledger.add([('a', start, value, unit)])
        except ValueError:
            pass
        else:
            raise AssertionError('unsupported magnitude accepted')
    ledger.add([('hot', start + timedelta(seconds=i), 1832, 'F') for i in range(1024)])
    summary = ledger.summary('hot', start, stop)
    assert (summary.count, summary.mean, summary.maximum) == (1024, 1000, 1000)


def worksheet_uncertainty():
    sys.path.insert(0, str(ROOT / 'cases/s4'))
    from desk.service import Desk
    desk, day = Desk(), date(2026, 1, 2)
    first = desk.approve([('guard', 'Inspect guard')])
    planned = desk.prepare(day, 'morning')
    second = desk.approve([('guard', 'Inspect and latch guard')])
    existing = desk.prepare(day, 'morning')
    later = desk.prepare(day, 'evening')
    assert planned == existing
    assert existing['revision'] == first and later['revision'] == second
    assert existing['tasks'] != later['tasks']
    policy = (ROOT / 'cases/s4/POLICY.md').read_text()
    assert 'appear on the next shift worksheet' in policy
    assert 'prepare morning and evening worksheets several days ahead' in policy
    assert 'Generating an\n   existing date and shift returns that worksheet' in policy
    # Observable behavior is proven; whether "next" includes a prepared sheet is not.


def documentation_contract():
    base = ROOT / 'cases/s5'
    readme = (base / 'README.md').read_text()
    contract = (base / 'FORMAT.md').read_text()
    cli = (base / 'tileplan/cli.py').read_text()
    layout = (base / 'tileplan/layout.py').read_text()
    assert 'gap in millimeters' in readme and '5 mm gap' in readme
    assert 'whole raster pixels' in contract
    assert 'no physical-unit conversion or DPI parameter' in contract
    assert "help='gap in pixels'" in cli
    assert 'options.spacing_px' in layout
    tree = ast.parse(layout)
    assert not any(isinstance(node, ast.Name) and node.id.lower() == 'dpi' for node in ast.walk(tree))
    # Source correction follows from documents and direct mapping; no program run needed.


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    verify_inventory(manifest)
    for check in (rubric_boundary, listening_policy, sensor_controls,
                  worksheet_uncertainty, documentation_contract):
        check()
        print(check.__name__ + ': verified')
    print('Frozen case inventory: verified')


if __name__ == '__main__':
    main()
