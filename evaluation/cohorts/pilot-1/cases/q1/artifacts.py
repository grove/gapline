"""Single-writer immutable artifact generations on a local filesystem."""

import hashlib
import json
import os
from pathlib import Path


class ArtifactStore:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.recover()

    def _directory(self, generation):
        return self.root / f"generation-{generation:08d}"

    def _complete(self, directory):
        try:
            metadata = json.loads((directory / "metadata.json").read_text())
            data = (directory / "artifact.bin").read_bytes()
            return (
                metadata["size"] == len(data)
                and metadata["sha256"] == hashlib.sha256(data).hexdigest()
            )
        except (OSError, ValueError, KeyError, TypeError):
            return False

    def generations(self):
        result = []
        for directory in self.root.glob("generation-*"):
            suffix = directory.name.removeprefix("generation-")
            if suffix.isdigit() and self._complete(directory):
                result.append(int(suffix))
        return sorted(result)

    def _write_pointer(self, generation):
        staging = self.root / "CURRENT.next"
        staging.write_text(f"{generation}\n", encoding="ascii")
        os.replace(staging, self.root / "CURRENT")

    def recover(self):
        (self.root / "CURRENT.next").unlink(missing_ok=True)
        current = self.root / "CURRENT"
        if current.exists():
            return
        complete = self.generations()
        if complete:
            self._write_pointer(complete[-1])

    def publish(self, data):
        if not isinstance(data, bytes):
            raise TypeError("artifact must be bytes")
        allocated = [
            int(path.name.removeprefix("generation-"))
            for path in self.root.glob("generation-*")
            if path.name.removeprefix("generation-").isdigit()
        ]
        generation = max(allocated, default=0) + 1
        directory = self._directory(generation)
        directory.mkdir()
        (directory / "artifact.bin").write_bytes(data)
        metadata = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        (directory / "metadata.json").write_text(json.dumps(metadata))
        self._write_pointer(generation)
        return generation

    def read(self):
        current = self.root / "CURRENT"
        if not current.exists():
            return None
        generation = int(current.read_text(encoding="ascii"))
        directory = self._directory(generation)
        if not self._complete(directory):
            raise ValueError("committed artifact is incomplete")
        return (directory / "artifact.bin").read_bytes()
