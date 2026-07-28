#!/usr/bin/env python3
"""Generate and verify SHA-256 checksums over the frozen pre-registration.

The pre-registration's credibility rests on prereg/ being unaltered after the
freeze. CHECKSUMS.sha256 is the record of what those files hashed to. This
script writes that record and, later, checks it.

Usage:
    python scripts/checksums.py generate    # write CHECKSUMS.sha256
    python scripts/checksums.py verify      # check files against it

Output format is compatible with sha256sum(1), so a reader who distrusts this
script can verify independently:

    sha256sum -c CHECKSUMS.sha256

Notes:
    Files are hashed as raw bytes. .gitattributes pins line endings to LF so
    that a file committed from Windows and one committed from Linux hash
    identically; without that, this record would be platform-dependent.

    An empty prereg/ is a valid state before the specification is written. It
    produces an empty checksum file, and verify reports zero files rather than
    failing.

Exit codes:
    0  success (generate wrote the file, or verify found no discrepancies)
    1  verification failed, or a usage error
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = REPO_ROOT / "prereg"
CHECKSUM_FILE = REPO_ROOT / "CHECKSUMS.sha256"

# Placeholder files that exist only to keep an empty directory in git. They are
# not part of the pre-registration and are excluded so that removing one later
# does not read as tampering.
EXCLUDED_NAMES = {".gitkeep"}

CHUNK_SIZE = 1024 * 1024


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 of a file, read as raw bytes."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_files() -> list[Path]:
    """Return prereg/ files to hash, sorted for a stable, diffable record."""
    if not TARGET_DIR.is_dir():
        return []
    found = [
        p
        for p in TARGET_DIR.rglob("*")
        if p.is_file() and p.name not in EXCLUDED_NAMES
    ]
    return sorted(found, key=lambda p: p.relative_to(REPO_ROOT).as_posix())


def relative_posix(path: Path) -> str:
    """Repo-relative path with forward slashes, so records are OS-independent."""
    return path.relative_to(REPO_ROOT).as_posix()


def read_checksum_file() -> dict[str, str]:
    """Parse CHECKSUMS.sha256 into {relative_path: hex_digest}."""
    records: dict[str, str] = {}
    if not CHECKSUM_FILE.is_file():
        return records
    with CHECKSUM_FILE.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            # sha256sum format: "<64 hex chars><two spaces><path>"
            parts = line.split("  ", 1)
            if len(parts) != 2:
                print(
                    "ERROR: malformed record at line %d: %s" % (line_number, line)
                )
                sys.exit(1)
            digest, name = parts
            records[name] = digest
    return records


def generate() -> int:
    files = collect_files()
    lines = ["%s  %s" % (sha256_of(p), relative_posix(p)) for p in files]
    # Written with an explicit LF newline so the record matches what
    # .gitattributes stores, on every platform.
    CHECKSUM_FILE.write_text(
        "".join(line + "\n" for line in lines), encoding="utf-8", newline="\n"
    )
    if not files:
        print("Wrote %s: 0 files." % CHECKSUM_FILE.name)
        print("prereg/ is empty. This is expected before the specification is frozen.")
    else:
        print("Wrote %s: %d file(s)." % (CHECKSUM_FILE.name, len(files)))
        for path in files:
            print("  %s" % relative_posix(path))
    return 0


def verify() -> int:
    if not CHECKSUM_FILE.is_file():
        print("ERROR: %s does not exist. Run 'generate' first." % CHECKSUM_FILE.name)
        return 1

    recorded = read_checksum_file()
    present = {relative_posix(p): p for p in collect_files()}

    missing = sorted(set(recorded) - set(present))
    added = sorted(set(present) - set(recorded))
    changed = sorted(
        name
        for name in set(recorded) & set(present)
        if sha256_of(present[name]) != recorded[name]
    )

    if not recorded and not present:
        print("OK: 0 files recorded, 0 files present.")
        print("prereg/ is empty. This is expected before the specification is frozen.")
        return 0

    for name in changed:
        print("CHANGED : %s" % name)
    for name in missing:
        print("MISSING : %s" % name)
    for name in added:
        print("UNTRACKED: %s (present but not in the record)" % name)

    if changed or missing or added:
        print("")
        print(
            "FAILED: %d changed, %d missing, %d untracked."
            % (len(changed), len(missing), len(added))
        )
        print("A frozen pre-registration should produce none of these.")
        return 1

    print("OK: %d file(s) match the recorded checksums." % len(recorded))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify SHA-256 checksums over prereg/."
    )
    parser.add_argument(
        "command",
        choices=("generate", "verify"),
        help="'generate' writes CHECKSUMS.sha256; 'verify' checks against it",
    )
    args = parser.parse_args()
    return generate() if args.command == "generate" else verify()


if __name__ == "__main__":
    sys.exit(main())
