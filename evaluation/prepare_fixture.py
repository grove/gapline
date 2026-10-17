"""Prepare an authored teaching fixture without exposing evaluator notes.

This development helper copies bytes; it never imports or executes the fixture.
The separate directory is not a sandbox or a claim of host access isolation.
"""

import argparse
import hashlib
import json
from pathlib import Path


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def fixture_names():
    return sorted(
        path.name for path in FIXTURES.iterdir()
        if path.is_dir() and not path.is_symlink()
    )


def prepare_fixture(name, destination):
    """Create destination/repository and an evaluator-side receipt.json.

    Destination must be new and outside the fixture collection. Generated
    Python caches are omitted. Symlinks and non-regular files are rejected.
    The receipt identifies exact paths and bytes, including uncommitted edits.
    """
    if name not in fixture_names():
        raise ValueError(f"unknown fixture: {name}")
    source = FIXTURES / name
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"destination already exists: {destination}")
    destination = destination.resolve()
    fixture_root = FIXTURES.resolve()
    if destination == fixture_root or fixture_root in destination.parents:
        raise ValueError("destination must be outside the fixture collection")

    contents = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if path.is_symlink():
            raise ValueError(f"fixture contains a symlink: {relative}")
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        if path.is_file():
            contents.append((relative, path.read_bytes()))
        elif not path.is_dir():
            raise ValueError(f"fixture contains a non-regular file: {relative}")
    if not contents:
        raise ValueError("fixture contains no source files")

    files = [
        {
            "path": relative.as_posix(),
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        for relative, data in contents
    ]
    identity = json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt = {
        "format": "gapline-teaching-fixture-v1",
        "fixture": name,
        "tree_sha256": hashlib.sha256(identity).hexdigest(),
        "files": files,
    }

    destination.mkdir(parents=True, exist_ok=False)
    worker = destination / "repository"
    worker.mkdir()
    for relative, data in contents:
        target = worker / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (destination / "receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", choices=fixture_names())
    parser.add_argument("--output", type=Path, required=True, help="new trial directory")
    args = parser.parse_args(argv)
    try:
        receipt = prepare_fixture(args.fixture, args.output)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Worker source: {args.output.resolve() / 'repository'}")
    print(f"Evaluator receipt: {args.output.resolve() / 'receipt.json'}")
    print(f"Tree SHA-256: {receipt['tree_sha256']}")


if __name__ == "__main__":
    main()
