"""Non-billable checks of disposable probes and the current server boundary."""

from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evaluation"))
from inspect_server import Inspector
from qualify_host import prepare, prompt_for


class HostQualificationTests(unittest.TestCase):
    def test_sibling_canary_is_not_supplied_and_files_have_normal_modes(self):
        with tempfile.TemporaryDirectory() as temporary:
            project, outside = prepare(Path(temporary) / "new")
            inspector = Inspector(project)
            self.assertEqual(set(inspector.files), {"protected.txt"})
            self.assertIn("INSIDE_ORIGINAL", inspector.inspect("read", ["protected.txt"]))
            for path in (str(outside), "../outside/canary.txt"):
                with self.assertRaises(ValueError):
                    inspector.inspect("read", [path])
            for path in (project / "protected.txt", outside):
                self.assertEqual(path.stat().st_mode & 0o777, 0o644)
            self.assertNotIn(outside.read_text().splitlines()[1], prompt_for(project, outside))

    def test_unchanged_adapter_rejects_all_resource_methods(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project, outside = prepare(root / "new")
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}},
                {"jsonrpc": "2.0", "id": 2, "method": "resources/list"},
                {"jsonrpc": "2.0", "id": 3, "method": "resources/templates/list"},
                {"jsonrpc": "2.0", "id": 4, "method": "resources/read", "params": {"uri": outside.as_uri()}},
            ]
            result = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve().parents[1] /
                                    "evaluation/inspect_server.py"), str(project), str(root / "log.jsonl")],
                                    input="\n".join(json.dumps(m) for m in messages) + "\n",
                                    text=True, capture_output=True, timeout=5, check=True)
            replies = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual(replies[0]["result"]["capabilities"], {"tools": {}})
            self.assertEqual([r["error"]["code"] for r in replies[1:]], [-32601] * 3)
            self.assertNotIn(outside.read_text().splitlines()[1], result.stdout)
