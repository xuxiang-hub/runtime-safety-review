#!/usr/bin/env python3
"""Write or verify the SHA-256 manifest for the public artifact."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS"


def included_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path != MANIFEST
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
    )


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def current_lines() -> list[str]:
    return [f"{digest(path)}  {path.relative_to(ROOT).as_posix()}" for path in included_files()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="replace SHA256SUMS with current hashes")
    args = parser.parse_args()

    lines = current_lines()
    if args.write:
        MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {len(lines)} checksums to {MANIFEST.name}")
        return 0

    expected = MANIFEST.read_text(encoding="utf-8").splitlines()
    if expected != lines:
        raise AssertionError("SHA256SUMS does not match the current public artifact; run with --write after intentional changes")
    print(f"Checksum verification passed for {len(lines)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
