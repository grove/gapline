import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from artifacts import ArtifactStore


class ArtifactTests(unittest.TestCase):
    def test_empty_and_successive_publications(self):
        with tempfile.TemporaryDirectory() as root:
            store = ArtifactStore(root)
            self.assertIsNone(store.read())
            self.assertEqual(store.publish(b"version one"), 1)
            self.assertEqual(store.publish(b"version two"), 2)
            self.assertEqual(ArtifactStore(root).read(), b"version two")
            self.assertEqual(store.generations(), [1, 2])

    def test_failed_replacement_preserves_existing_commit(self):
        with tempfile.TemporaryDirectory() as root:
            store = ArtifactStore(root)
            store.publish(b"approved")
            with patch("artifacts.os.replace", side_effect=OSError("disk error")):
                with self.assertRaises(OSError):
                    store.publish(b"candidate")
            self.assertEqual(store.read(), b"approved")
            self.assertEqual(ArtifactStore(root).read(), b"approved")
            self.assertFalse((Path(root) / "CURRENT.next").exists())


if __name__ == "__main__":
    unittest.main()
