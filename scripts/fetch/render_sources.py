"""Render the tables in data/SOURCES.md from the registry.

SOURCES.md calls series_registry.py its machine-readable twin, but the two were
maintained by hand and drifted badly: after FRED stopped answering and domains 3,
6 and 8 were re-routed, SOURCES.md still listed four dead FRED identifiers, still
showed domain 6 as UNRESOLVED nine days after it was decided, and still pointed
domain 8 at the WASDE tables. Standing rule 1 keys admission to data/raw/ on a
row in that table, so the drift would have bitten at gate-open, on the one
document whose whole job is provenance.

Generating the tables removes the failure mode instead of fixing this instance
of it. Prose is left alone; only the two tables and the status paragraph are
rewritten, between explicit markers.

Report mode by default. Pass --apply to write.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

# The generated tables carry a real minus sign for inverted orientation.
# Windows consoles default to cp1252, which cannot encode it, so printing
# the diff would crash the tool rather than the tool being wrong.
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:  # pragma: no cover - older interpreters
    pass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from series_registry import REGISTRY  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
SOURCES = REPO / "data" / "SOURCES.md"

BEGIN_STATUS = "<!-- BEGIN GENERATED: status -->"
END_STATUS = "<!-- END GENERATED: status -->"
BEGIN_SERIES = "<!-- BEGIN GENERATED: series -->"
END_SERIES = "<!-- END GENERATED: series -->"
BEGIN_BLOCK = "<!-- BEGIN GENERATED: blockers -->"
END_BLOCK = "<!-- END GENERATED: blockers -->"

CONFIDENCE_MARK = {
    "confirmed": "**verified**",
    "reachable": "*reachable, identity unverified*",
    "manual": "*transcription*",
    "unrouted": "*no route*",
}


def esc(text: str) -> str:
    return (text or "").replace("|", "\\|").strip()


def series_table() -> str:
    head = ("| Domain | Series | Source | Identifier | Units (expected) | "
            "Freq. | Orient. | Tier | Identity | Retrieved |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n")
    lines = []
    for s in sorted(REGISTRY, key=lambda x: (x.domain, x.key)):
        if s.domain == 0:
            continue
        ident = s.identifier or ""
        ident = "*(%s)*" % esc(ident.strip("()")) if ident.startswith("(") \
            else "`%s`" % esc(ident)
        lines.append(
            "| %s | %s | %s | %s | %s | %s | %s | %s | %s | — |"
            % (s.domain, esc(s.label), esc(s.source), ident,
               esc(s.expect_units), esc(s.expect_frequency),
               "+" if s.orientation > 0 else "**−**",
               esc(s.tier).replace("Tier ", "").replace("3", "**3**"),
               CONFIDENCE_MARK.get(s.confidence, s.confidence)))
    return head + "\n".join(lines) + "\n"


def blocker_table() -> str:
    head = "| Series | Blocker |\n|---|---|\n"
    lines = []
    for s in sorted(REGISTRY, key=lambda x: (x.domain, x.key)):
        for b in (s.blockers or []):
            lines.append("| %s | %s |" % (esc(s.label), esc(b)))
    if not lines:
        return head + "| *(none)* | |\n"
    return head + "\n".join(lines) + "\n"


def status_paragraph() -> str:
    n_conf = sum(1 for s in REGISTRY if s.confidence == "confirmed" and s.domain)
    n_reach = sum(1 for s in REGISTRY if s.confidence == "reachable" and s.domain)
    n_manual = sum(1 for s in REGISTRY if s.confidence == "manual" and s.domain)
    return (
        "**Status: PLANNED. Nothing below has been retrieved.**\n\n"
        "The data gate is closed. No series in this table has been fetched into\n"
        "`data/raw/`, and the Retrieved column is blank because no retrieval has\n"
        "occurred.\n\n"
        "Identity is a separate question from retrieval, and the two are tracked\n"
        "separately on purpose. **%d series have had their identity verified**\n"
        "against a live response by\n"
        "[`verify.py`](../scripts/fetch/verify.py) — the endpoint answers, the\n"
        "returned series is the one the spec names, and the source-specific traps\n"
        "were checked. %d more are reachable but unverified, and %d are Tier 3\n"
        "transcriptions that cannot be scripted at all. Verifying an identity\n"
        "reads metadata and a probe window; it is not the same as admitting the\n"
        "series to the study, and it does not open the gate.\n"
        % (n_conf, n_reach, n_manual))


def build(text: str) -> str:
    for begin, end, body in (
            (BEGIN_STATUS, END_STATUS, status_paragraph()),
            (BEGIN_SERIES, END_SERIES, series_table()),
            (BEGIN_BLOCK, END_BLOCK, blocker_table())):
        i, j = text.find(begin), text.find(end)
        if i == -1 or j == -1:
            raise SystemExit(
                "marker %s / %s not found in SOURCES.md - add them around the "
                "table before generating" % (begin, end))
        text = text[:i + len(begin)] + "\n" + body + text[j:]
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="write the file (default is report only)")
    args = ap.parse_args()

    before = SOURCES.read_text(encoding="utf-8")
    after = build(before)

    if before == after:
        print("SOURCES.md already matches the registry. Nothing to do.")
        return 0
    import difflib
    diff = list(difflib.unified_diff(
        before.splitlines(), after.splitlines(),
        fromfile="data/SOURCES.md", tofile="data/SOURCES.md (generated)",
        lineterm="", n=1))
    print("\n".join(diff[:120]))
    if len(diff) > 120:
        print("... %d more diff lines" % (len(diff) - 120))
    if not args.apply:
        print("\nREPORT ONLY. Re-run with --apply to write.")
        return 0
    SOURCES.write_text(after, encoding="utf-8", newline="\n")
    print("\ndata/SOURCES.md written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
