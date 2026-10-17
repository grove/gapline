"""Evaluator-only MCP file inspection: immutable allowlist, no execution API."""

import json
from pathlib import Path
import sys


class Inspector:
    def __init__(self, root, limit=12):
        self.files = {}
        for path in sorted(Path(root).rglob("*")):
            if path.is_symlink():
                raise ValueError("symlinks are forbidden")
            if path.is_file():
                self.files[path.relative_to(root).as_posix()] = path.read_text()
        self.limit = limit
        self.calls = 0

    def inspect(self, operation, paths=None, query=""):
        self.calls += 1
        if self.calls > self.limit:
            raise ValueError("inspection budget exhausted")
        if operation == "list":
            return "\n".join(self.files)
        selected = list(self.files) if paths is None else paths
        if not selected or any(path not in self.files for path in selected):
            raise ValueError("only exact listed relative file paths are permitted")
        if operation not in ("read", "search"):
            raise ValueError("only list, read, search are permitted")
        lines = []
        for path in selected:
            for number, line in enumerate(self.files[path].splitlines(), 1):
                if operation == "read" or query in line:
                    lines.append(f"{path}:{number}: {line}")
        result = "\n".join(lines)
        return result[:80000] + ("\n[TRUNCATED; read fewer files]" if len(result) > 80000 else "")


def main():
    inspector = Inspector(Path(sys.argv[1]))
    log = Path(sys.argv[2])
    schema = {
        "name": "inspect", "description": "Read-only inspection of supplied files. Exact relative paths only; no shell, code execution, writes or network. Each call consumes one of 12 inspections. Batch reads allowed.",
        "inputSchema": {"type": "object", "properties": {
            "operation": {"type": "string", "enum": ["list", "read", "search"]},
            "paths": {"type": "array", "items": {"type": "string"}},
            "query": {"type": "string", "description": "Literal search text"},
        }, "required": ["operation"], "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    }
    for line in sys.stdin:
        request = json.loads(line)
        if "id" not in request:
            continue
        method = request["method"]
        if method == "initialize":
            result = {"protocolVersion": request["params"]["protocolVersion"], "capabilities": {"tools": {}},
                      "serverInfo": {"name": "frozen-file-inspection", "version": "1"}}
        elif method == "tools/list":
            result = {"tools": [schema]}
        elif method == "tools/call":
            params = request["params"]
            try:
                if params["name"] != "inspect":
                    raise ValueError("unknown tool")
                output = inspector.inspect(**params["arguments"])
                result = {"content": [{"type": "text", "text": output}]}
            except (ValueError, TypeError) as error:
                result = {"isError": True, "content": [{"type": "text", "text": str(error)}]}
            with log.open("a") as stream:
                stream.write(json.dumps({"call": inspector.calls, "params": params, "result": result}) + "\n")
        elif method == "ping":
            result = {}
        else:
            print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "error": {"code": -32601, "message": "unsupported method"}}), flush=True)
            continue
        print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)


if __name__ == "__main__":
    main()
