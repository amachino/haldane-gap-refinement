"""Check distributed SHA-256 sums and imported upstream Git blob identities."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    snapshot = json.loads((ROOT / "SHA256SUMS.json").read_text())
    for relative, expected in snapshot.items():
        data = (ROOT / relative).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            raise RuntimeError(f"Snapshot mismatch: {relative}")
    upstream = json.loads((ROOT / "source_manifest.json").read_text())
    for entry in upstream["files"]:
        data = (ROOT / "source" / entry["path"]).read_bytes()
        header = f"blob {len(data)}\0".encode("ascii")
        actual = hashlib.sha1(header + data).hexdigest()
        if actual != entry["git_sha"] or len(data) != entry["size"]:
            raise RuntimeError(f"Upstream Git blob mismatch: {entry['path']}")
    print(f"PASS: {len(snapshot)} snapshot files and {len(upstream['files'])} upstream Git blobs.")


if __name__ == "__main__":
    main()
