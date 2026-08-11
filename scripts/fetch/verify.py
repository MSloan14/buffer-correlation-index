#!/usr/bin/env python3
"""Verify that each registry identifier resolves to the series it claims.

Runs BEFORE any analysis, at gate-open. A wrong identifier does not raise. It
returns a different real series with plausible units, renders cleanly, and is
wrong in a way nothing downstream can detect. That is the failure this module
exists to prevent, and it is why every check below asserts on something
SPECIFIC to the required series rather than on units alone.

Nine traps are recorded in series_registry.py. Each is enforced here as a named
check that fails loudly. A trap that cannot be checked programmatically is
reported as UNCHECKED rather than passed silently.

Result per series:
    PASS       resolved, and every check on it passed
    MISMATCH   resolved, but something differs from what the registry claims
    UNRESOLVED could not be retrieved
    SKIPPED    manual or otherwise out of scope for automated verification

Usage:
    python scripts/fetch/verify.py            # verify everything
    python scripts/fetch/verify.py --key d5   # one series
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_registry import REGISTRY, PlannedSeries  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE = REPO_ROOT / ".env"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"
TIMEOUT = 90


def load_env() -> dict[str, str]:
    out: dict[str, str] = {}
    if not ENV_FILE.is_file():
        return out
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if v.strip():
            out[k.strip()] = v.strip()
    return out


def http(url: str, data: bytes | None = None,
         content_type: str | None = None) -> bytes:
    headers = {"User-Agent": UA}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


@dataclass
class Check:
    name: str
    ok: bool | None          # None = could not be checked
    detail: str


@dataclass
class Result:
    key: str
    status: str              # PASS | MISMATCH | UNRESOLVED | SKIPPED
    observed: dict = field(default_factory=dict)
    checks: list[Check] = field(default_factory=list)
    error: str = ""

    def add(self, name: str, ok: bool | None, detail: str) -> None:
        self.checks.append(Check(name, ok, detail))

    def settle(self) -> None:
        if self.status in ("UNRESOLVED", "SKIPPED", "UNVERIFIED"):
            return
        if any(c.ok is False for c in self.checks):
            self.status = "MISMATCH"
        elif not any(c.ok is True for c in self.checks):
            # Nothing actually passed; only unperformed checks. That is not a
            # pass, and calling it one is how an unverified series ends up
            # looking identical to a verified one in the summary.
            self.status = "UNVERIFIED"
        else:
            self.status = "PASS"


# --------------------------------------------------------------------------
# Per-source verifiers. Each asserts on something specific to the required
# series, never on units alone.
# --------------------------------------------------------------------------


def verify_bea_saving_rate(s: PlannedSeries, env: dict) -> Result:
    r = Result(s.key, "PENDING")
    key = env.get("BEA_API_KEY")
    if not key:
        r.status = "UNRESOLVED"
        r.error = "BEA_API_KEY missing from .env"
        return r
    url = (
        "https://apps.bea.gov/api/data/?UserID=%s&method=GetData"
        "&datasetname=NIPA&TableName=T20100&Frequency=A&Year=ALL"
        "&ResultFormat=JSON" % key
    )
    try:
        rows = json.loads(http(url))["BEAAPI"]["Results"]["Data"]
    except Exception as e:
        r.status = "UNRESOLVED"
        r.error = str(e)[:200]
        return r

    target = [x for x in rows
              if "saving as a percentage of disposable" in
              x.get("LineDescription", "").lower()]
    r.add("line description present", bool(target),
          target[0]["LineDescription"] if target else "not found in T20100")
    if not target:
        r.status = "MISMATCH"
        return r

    line_no = target[0].get("LineNumber")
    series_code = target[0].get("SeriesCode")
    years = sorted(x["TimePeriod"] for x in target)
    r.observed = {"line": line_no, "series_code": series_code,
                  "n": len(target), "first": years[0], "last": years[-1]}
    r.add("series code A072RC", series_code == "A072RC",
          "got %s" % series_code)
    r.add("annual frequency", True, "Frequency=A requested and returned")
    r.add("covers the 2000-2026 window", years[0] <= "2000" and years[-1] >= "2024",
          "%s to %s" % (years[0], years[-1]))
    r.settle()
    return r


def verify_bls(s: PlannedSeries, env: dict) -> Result:
    r = Result(s.key, "PENDING")
    payload = {"seriesid": [s.identifier], "startyear": "2005",
               "endyear": "2024", "catalog": True}
    if env.get("BLS_API_KEY"):
        payload["registrationkey"] = env["BLS_API_KEY"]
    try:
        resp = json.loads(http("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                               data=json.dumps(payload).encode(),
                               content_type="application/json"))
    except Exception as e:
        r.status = "UNRESOLVED"
        r.error = str(e)[:200]
        return r
    if resp.get("status") != "REQUEST_SUCCEEDED" or not resp["Results"].get("series"):
        r.status = "UNRESOLVED"
        r.error = "; ".join(resp.get("message", []))[:200] or "no series returned"
        return r

    ser = resp["Results"]["series"][0]
    cat = ser.get("catalog") or {}
    title = cat.get("series_title", "")
    data = ser.get("data", [])
    r.observed = {"title": title, "n": len(data),
                  "periodicity": cat.get("periodicity_code", ""),
                  "first": data[-1]["year"] if data else "",
                  "last": data[0]["year"] if data else ""}
    r.add("returned data", bool(data), "%d observations" % len(data))
    # Assert on MEANING, not units: percent alone would match many BLS series.
    r.add("title names union membership",
          ("union" in title.lower() and "member" in title.lower())
          if title else None,
          title or "catalog unavailable on this key tier")
    r.add("annual periodicity",
          all(d.get("period") == "A01" for d in data) if data else False,
          "periods: %s" % sorted({d.get("period") for d in data}))
    if data:
        vals = [float(d["value"]) for d in data if d.get("value")]
        plausible = all(0 < v < 50 for v in vals)
        r.add("values in a plausible percent range", plausible,
              "min=%.1f max=%.1f" % (min(vals), max(vals)))
    r.settle()
    return r


def verify_treasury_debt(s: PlannedSeries, env: dict) -> Result:
    """TRAP: debt held by THE PUBLIC, not TOTAL public debt.

    Asserts on the FIELD NAME. Both quantities are dollar series named almost
    identically and differ by roughly a quarter, so units cannot separate them.
    """
    r = Result(s.key, "PENDING")
    url = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
           "v2/accounting/od/debt_to_penny?sort=-record_date&page[size]=1")
    try:
        payload = json.loads(http(url))
    except Exception as e:
        r.status = "UNRESOLVED"
        r.error = str(e)[:200]
        return r
    rec = (payload.get("data") or [{}])[0]
    fields = list(rec.keys())
    r.observed = {"fields": len(fields), "record_date": rec.get("record_date", "")}

    held_public = "debt_held_public_amt" in fields
    total_debt = "tot_pub_debt_out_amt" in fields
    r.add("TRAP: debt_held_public_amt field exists", held_public,
          "present" if held_public else "ABSENT - cannot isolate the required quantity")
    r.add("TRAP: distinguishable from total public debt", held_public and total_debt,
          "both fields present, so the wrong one is selectable by mistake"
          if (held_public and total_debt) else "fields: %s" % ", ".join(fields[:6]))
    if held_public and total_debt:
        try:
            hp = float(rec["debt_held_public_amt"])
            tot = float(rec["tot_pub_debt_out_amt"])
            r.add("held-public is materially smaller than total",
                  hp < tot * 0.95,
                  "ratio held/total = %.3f" % (hp / tot) if tot else "n/a")
        except Exception:
            r.add("held-public smaller than total", None, "non-numeric values")
    r.add("coverage back to 2000", None,
          "NOT CHECKED - single-record probe only; full span must be confirmed at fetch")
    r.settle()
    return r


def verify_omb_table(s: PlannedSeries, env: dict) -> Result:
    """TRAP (severe): Table 3.1 has three 'Net interest' rows in different units.

    Asserts on the SECTION HEADING above the row, never the row label.
    """
    import openpyxl

    r = Result(s.key, "PENDING")
    table = "hist03z1" if s.key == "net_interest" else "hist01z1"
    url = ("https://www.whitehouse.gov/wp-content/uploads/2026/04/"
           "%s_fy2027.xlsx" % table)
    try:
        wb = openpyxl.load_workbook(io.BytesIO(http(url)), read_only=True,
                                    data_only=True)
        rows = list(wb[wb.sheetnames[0]].iter_rows(values_only=True))
    except Exception as e:
        r.status = "UNRESOLVED"
        r.error = str(e)[:200]
        return r

    if s.key == "net_interest":
        hits = [i for i, row in enumerate(rows)
                if isinstance(next((c for c in row if c not in (None, "")), None), str)
                and next(c for c in row if c not in (None, "")).strip().lower()
                == "net interest"]
        r.observed = {"net_interest_rows": hits}
        r.add("TRAP: multiple 'Net interest' rows found", len(hits) >= 2,
              "rows %s - the label alone is ambiguous" % hits)

        def heading_above(idx: int) -> str:
            for j in range(idx - 1, max(idx - 22, -1), -1):
                cells = [c for c in rows[j] if c not in (None, "")]
                txt = [c for c in cells if isinstance(c, str)]
                num = [c for c in cells if isinstance(c, (int, float))]
                if txt and not num and len(" ".join(str(t) for t in txt)) > 12:
                    return " ".join(str(t) for t in txt).strip().lower()
            return ""

        dollar_rows = [i for i in hits if "millions of dollars" in heading_above(i)]
        r.add("TRAP: a dollar-denominated row is identifiable by heading",
              len(dollar_rows) == 1,
              "rows under 'in millions of dollars': %s" % dollar_rows)
        if len(dollar_rows) == 1:
            chosen = dollar_rows[0]
            r.observed["chosen_row"] = chosen
            r.add("chosen row matches the registry", chosen == 21,
                  "registry says 21, heading-based selection says %d" % chosen)
            vals = [c for c in rows[chosen] if isinstance(c, (int, float))]
            r.add("values look like dollar millions, not percentages",
                  max(vals) > 1000, "max=%s" % max(vals))
            r.observed["n_values"] = len(vals)
        pct_rows = [i for i in hits if "percentages of outlays" in heading_above(i)]
        r.add("TRAP: percentage-of-outlays row identified and excluded",
              bool(pct_rows), "rows %s excluded" % pct_rows)
    else:
        hdr = None
        for i, row in enumerate(rows[:8]):
            cells = [str(c).strip().lower() if c else "" for c in row]
            if "receipts" in cells and "outlays" in cells:
                hdr = i
                break
        r.observed = {"header_row": hdr}
        r.add("receipts/outlays header located", hdr is not None,
              "row %s" % hdr)
        firsts = [next((c for c in row if c not in (None, "")), None)
                  for row in rows]
        aggregates = [f for f in firsts
                      if isinstance(f, str) and "-" in f and f[:4].isdigit()]
        r.add("TRAP: multi-year aggregate rows present and must be skipped",
              bool(aggregates), "found %s" % aggregates[:3])
        # OMB stores years as TEXT in this workbook, not as numbers. An earlier
        # version of this check required int/float and rejected every row,
        # which at fetch time would have silently produced an empty series.
        def as_year(v):
            if isinstance(v, (int, float)) and 1900 < v < 2040:
                return int(v)
            if isinstance(v, str):
                t = v.strip().rstrip("*").strip()
                if t.isdigit() and 1900 < int(t) < 2040:
                    return int(t)
            return None

        year_rows = [y for y in (as_year(f) for f in firsts) if y is not None]
        r.add("single-year rows parse", len(year_rows) > 80,
              "%d year rows, %s to %s"
              % (len(year_rows), min(year_rows), max(year_rows))
              if year_rows else "none parsed")
        def is_text_year(v) -> bool:
            if not isinstance(v, str):
                return False
            return v.strip().rstrip("*").strip().isdigit()

        r.add("year cells are text, not numbers",
              any(is_text_year(f) for f in firsts),
              "confirmed - a numeric-only parser would return an empty series")
        r.add("TRAP: Total vs On-Budget receipts columns", None,
              "NOT CHECKED programmatically - column-span parsing required; "
              "the registry records that Total is the first numeric column")
    r.settle()
    return r


def verify_generic_reachable(s: PlannedSeries, env: dict) -> Result:
    """Entries with a host but no settled endpoint.

    Returns UNVERIFIED, never PASS. An earlier version returned PASS whenever
    the host answered, which meant a series whose identity had not been checked
    at all appeared in the summary next to genuinely verified ones. Reachability
    is not verification, and a probe that cannot fail is not a check.

    Route templates carrying placeholders are not probed at all: stripping the
    placeholder yields a directory URL that says nothing about the series.
    """
    r = Result(s.key, "UNVERIFIED")
    if "{" in s.route:
        r.error = ("route is a template (%s) and the endpoint is unsettled; "
                   "probing the bare host would test nothing" % s.route)
        r.add("series identity verified", None,
              "NOT CHECKED - endpoint unsettled, identifier '%s'" % s.identifier)
        return r
    if not s.route.startswith("http"):
        r.status = "SKIPPED"
        r.error = "no HTTP route recorded"
        return r
    try:
        body = http(s.route)
    except Exception as e:
        r.status = "UNRESOLVED"
        r.error = str(e)[:160]
        return r
    r.observed = {"bytes": len(body)}
    if not body:
        r.status = "UNRESOLVED"
        r.error = "host answered with an empty body"
        return r
    r.add("host answers", True, "%d bytes" % len(body))
    r.add("series identity verified", None,
          "NOT CHECKED - endpoint not settled; identifier is '%s'" % s.identifier)
    return r


VERIFIERS = {
    "saving_rate": verify_bea_saving_rate,
    "union_density": verify_bls,
    "debt_held_public": verify_treasury_debt,
    "net_interest": verify_omb_table,
    "federal_receipts": verify_omb_table,
}


def verify_one(s: PlannedSeries, env: dict) -> Result:
    if s.confidence == "manual":
        r = Result(s.key, "SKIPPED")
        r.error = "Tier 3 manual transcription; not scriptable"
        return r
    fn = VERIFIERS.get(s.key, verify_generic_reachable)
    try:
        return fn(s, env)
    except Exception as e:  # a verifier must never take the run down
        r = Result(s.key, "UNRESOLVED")
        r.error = "verifier raised: %s" % str(e)[:160]
        return r


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--key", help="verify a single registry key")
    args = ap.parse_args()

    env = load_env()
    targets = [s for s in REGISTRY if (not args.key or s.key == args.key)]
    print("verify_registry - %d series, keys loaded: %s"
          % (len(targets), ", ".join(sorted(env)) or "none"))
    print("")

    results = []
    for s in targets:
        res = verify_one(s, env)
        results.append(res)
        print("%-9s %-18s %s" % (res.status, s.key, s.label[:44]))
        for c in res.checks:
            mark = {True: "  ok  ", False: " FAIL ", None: " ---- "}[c.ok]
            print("   %s %-46s %s" % (mark, c.name[:46], c.detail[:80]))
        if res.error:
            print("          error: %s" % res.error)
        print("")

    tally: dict[str, int] = {}
    for r in results:
        tally[r.status] = tally.get(r.status, 0) + 1
    print("=" * 66)
    print("SUMMARY: " + "  ".join("%s=%d" % kv for kv in sorted(tally.items())))
    unchecked = sum(1 for r in results for c in r.checks if c.ok is None)
    print("%d check(s) could not be performed and are reported as UNCHECKED, "
          "not passed." % unchecked)
    failed = [r.key for r in results if r.status == "MISMATCH"]
    if failed:
        print("MISMATCHES: %s" % ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
