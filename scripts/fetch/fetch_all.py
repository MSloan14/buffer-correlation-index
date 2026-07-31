#!/usr/bin/env python3
"""Fetch driver for Study 1. WRITTEN WHILE THE DATA GATE IS CLOSED.

**This script has never been run and must not be run until the gate opens.**

The gate is a deliberate obstacle, not a formality. The project's remaining
confirmatory element is only confirmatory if its criterion was fixed before any
real series was seen. Fetching early does not merely break a rule; it destroys
the property that makes the result worth anything, irreversibly and silently.

Two independent locks, both of which must be released:

  1. `--apply` must be passed. Default behaviour is a dry run that prints the
     plan and touches no network. (Repository convention: report mode by
     default, explicit flag to act.)
  2. `data/.gate-open` must exist and contain a line
     `OPENED BY: <name> ON <ISO date>`. The author creates it. This script will
     not create it, and no automated process should.

Usage:
    python scripts/fetch/fetch_all.py                 # dry run, no network
    python scripts/fetch/fetch_all.py --verify-only   # fetch metadata, no data
    python scripts/fetch/fetch_all.py --apply         # real fetch, gate required
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_registry import REGISTRY, all_blockers, by_domain  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GATE_FILE = REPO_ROOT / "data" / ".gate-open"
RAW_DIR = REPO_ROOT / "data" / "raw"


def gate_is_open() -> tuple[bool, str]:
    if not GATE_FILE.is_file():
        return False, "data/.gate-open does not exist"
    text = GATE_FILE.read_text(encoding="utf-8").strip()
    if "OPENED BY:" not in text:
        return False, "data/.gate-open exists but has no 'OPENED BY:' line"
    return True, text.splitlines()[0]


def print_plan() -> None:
    print("PLANNED FETCHES (dry run - no network access performed)")
    print("")
    for domain, items in sorted(by_domain().items()):
        print("Domain %d" % domain)
        for s in items:
            print("  %-22s %s" % (s.key, s.label))
            print("      source     : %s" % s.source)
            print("      identifier : %s   [UNVERIFIED, confidence=%s]"
                  % (s.identifier, s.confidence))
            print("      expect     : %s, %s" % (s.expect_units, s.expect_frequency))
            print("      orientation: %+d   tier: %s" % (s.orientation, s.tier))
            if s.notes:
                print("      note       : %s" % s.notes.replace("\n", " ")[:160])
            for b in s.blockers:
                print("      BLOCKER    : %s" % b)
        print("")


def verify_registry() -> int:
    """Check fetched metadata against expectations. Runs at gate-open, before analysis.

    A wrong identifier does not raise; it returns a different real series with
    plausible units. This is the only thing standing between a typo and an
    analysis quietly about the wrong quantity, so it runs before anything is
    computed and a mismatch is fatal rather than a warning.
    """
    raise NotImplementedError(
        "verify_registry runs at gate-open. It must compare each fetched "
        "series' returned title, units and frequency against expect_units / "
        "expect_frequency in series_registry.py, and refuse any series that "
        "does not match. Not implemented while the gate is closed, because it "
        "cannot be tested without fetching."
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="perform real fetches (requires the gate to be open)")
    ap.add_argument("--verify-only", action="store_true",
                    help="fetch metadata only, to check identifiers")
    args = ap.parse_args()

    blockers = all_blockers()

    if not args.apply and not args.verify_only:
        print_plan()
        print("=" * 68)
        print("DRY RUN. No network access was performed.")
        print("%d series planned, %d unverified identifiers, %d blockers."
              % (len(REGISTRY), sum(1 for s in REGISTRY if not s.verified),
                 len(blockers)))
        if blockers:
            print("")
            print("BLOCKERS - resolve before fetching:")
            for key, b in blockers:
                print("  [%s] %s" % (key, b))
        ok, why = gate_is_open()
        print("")
        print("Gate: %s (%s)" % ("OPEN" if ok else "CLOSED", why))
        return 0

    ok, why = gate_is_open()
    if not ok:
        print("REFUSING TO FETCH: the data gate is closed.")
        print("  reason: %s" % why)
        print("")
        print("The gate is released by the author creating data/.gate-open with")
        print("a line 'OPENED BY: <name> ON <ISO date>'. No automated process")
        print("should create it. Nothing was fetched.")
        return 1

    print("Gate is open: %s" % why)
    if blockers:
        print("REFUSING TO FETCH: %d unresolved blocker(s) remain." % len(blockers))
        for key, b in blockers:
            print("  [%s] %s" % (key, b))
        return 1

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print("Fetch implementation is deliberately absent until the gate opens;")
    print("it should be written and reviewed at that point, not before.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
