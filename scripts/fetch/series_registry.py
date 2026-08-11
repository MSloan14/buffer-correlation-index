#!/usr/bin/env python3
"""Registry of planned series, rewritten 2026-08-11 against reachable routes.

The 2026-08-01 registry routed six series through FRED. FRED has been
unreachable from this machine since at least 2026-08-02 -- every
`stlouisfed.org` subdomain times out, sandboxed and unsandboxed -- so those
routes are gone. DATA_TERMS.md already preferred the issuing agency over an
aggregator, so the replacements are closer to the rule than the originals were.

## Confidence levels mean something here

    confirmed   The endpoint was queried and returned the expected series.
                Title, units and coverage below were READ from the response,
                not remembered.
    reachable   The host answers, but this specific series has not been pulled.
                Everything below it is an expectation to be tested.
    unrouted    No working route is known. This is a gap, not a to-do.
    manual      Cannot be scripted. Requires a human.

Only `confirmed` entries have had their metadata verified. Everything else is a
claim awaiting `verify_registry()`.

## The failure mode this file exists to prevent

A wrong identifier does not raise an error. It returns a different real series
with plausible units, and every number downstream is quietly about the wrong
thing. Two specific traps are recorded as `traps` below and are checked
explicitly rather than left to a units comparison.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlannedSeries:
    domain: int
    key: str
    label: str
    source: str
    route: str                       # how to get it
    identifier: str
    expect_units: str
    expect_frequency: str
    orientation: int                 # +1 higher = more buffer, -1 invert first
    tier: str
    confidence: str                  # confirmed | reachable | unrouted | manual
    coverage: str = "unknown"
    derived: bool = False            # a component of a ratio, not an analysis series
    notes: str = ""
    traps: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)


BEA_API = "https://apps.bea.gov/api/data/"
BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
EIA_BULK = "https://www.eia.gov/dnav/pet/hist_xls/{id}w.xls"
TREASURY = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
OECD_SDMX = "https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,{flow}/"
NASS_API = "https://quickstats.nass.usda.gov/api/api_GET/"
OMB_XLSX = "https://www.whitehouse.gov/wp-content/uploads/2026/04/{table}_fy2027.xlsx"

REGISTRY: list[PlannedSeries] = [
    # ---- Domain 1: strategic reserve -----------------------------------
    PlannedSeries(
        domain=1, key="spr_stocks", label="SPR crude oil stocks",
        source="EIA", route=EIA_BULK, identifier="WCSSTUS1",
        expect_units="Thousand Barrels", expect_frequency="Weekly",
        orientation=+1, tier="Tier 1", confidence="reachable",
        notes="Bulk xls endpoint answered with 129 KB on 2026-08-11. The series "
              "itself has not been parsed. Enters the annual index as a "
              "calendar-year mean per Index Spec v0.2 section 1.",
        traps=["Must be SPR stocks specifically, NOT total US commercial crude "
               "stocks. Both are weekly, both in thousand barrels, and a mixup "
               "would pass any units check."],
    ),
    PlannedSeries(
        domain=1, key="refinery_inputs", label="Refiner net crude oil input",
        source="EIA", route=EIA_BULK, identifier="WCRRIUS2",
        expect_units="Thousand Barrels per Day", expect_frequency="Weekly",
        orientation=+1, tier="Tier 1", confidence="reachable", derived=True,
        notes="Denominator only. The coverage ratio is SPR stocks divided by "
              "trailing-12-month mean daily inputs, and is DERIVED here, not "
              "fetched as a series.",
        traps=["This is a denominator. It must never be charted or scored as a "
               "buffer series in its own right."],
    ),

    # ---- Domain 2: financial -------------------------------------------
    PlannedSeries(
        domain=2, key="credit_gap",
        label="BIS credit-to-GDP gap, US private non-financial",
        source="BIS", route="https://data.bis.org/", identifier="(endpoint TBD)",
        expect_units="Percentage points of GDP", expect_frequency="Quarterly",
        orientation=-1, tier="Tier 2", confidence="reachable",
        notes="bis.org answers. The specific download path has not been "
              "established. Spec v0.2 section 3.1: PUBLISHED VALUES ONLY. Do "
              "not recompute the one-sided HP filter.",
        blockers=["Tier 2 terms of use must be verified before any BIS file is "
                  "committed. Until verified, handle as Tier 3."],
    ),

    # ---- Domain 3: fiscal ----------------------------------------------
    PlannedSeries(
        domain=3, key="debt_held_public", label="Federal debt held by the public",
        source="Treasury FiscalData", route=TREASURY,
        identifier="v2/accounting/od/debt_to_penny",
        expect_units="US Dollars", expect_frequency="Daily",
        orientation=-1, tier="Tier 1", confidence="reachable", derived=True,
        notes="API answered on 2026-08-11. Level only; the spec quantity is a "
              "share of GDP, so this is a numerator requiring a BEA GDP "
              "denominator.",
        traps=["THE RECORDED TRAP. The required quantity is debt held by THE "
               "PUBLIC, not TOTAL public debt (which includes intragovernmental "
               "holdings and is roughly a quarter larger). Both are dollar "
               "series named almost identically. verify_registry must assert on "
               "the field name, not the units."],
    ),
    PlannedSeries(
        domain=3, key="gdp", label="Gross domestic product",
        source="BEA", route=BEA_API, identifier="NIPA/T10105",
        expect_units="Millions of dollars", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="reachable", derived=True,
        notes="Denominator for debt/GDP. Table not yet confirmed.",
        traps=["Denominator only. Never charted or scored as a buffer."],
    ),
    PlannedSeries(
        domain=3, key="net_interest", label="Federal net interest outlays",
        source="OMB Historical Tables", route=OMB_XLSX,
        identifier="hist03z1 / Table 3.1 / row 21",
        expect_units="Millions of dollars", expect_frequency="Annual (FY)",
        orientation=-1, tier="Tier 1", confidence="confirmed", derived=True,
        coverage="93 annual observations (1940 onward, incl. projections)",
        notes="CONFIRMED 2026-08-11, replacing the dead FRED route (FYOINT). "
              "OMB Table 3.1, outlays by superfunction and function. Row 21 "
              "read as 899 (first) to 1,363,769 (last), in millions of dollars. "
              "Projection years must be trimmed at fetch: the file is the FY2027 "
              "budget edition and extends past the last actual year.",
        traps=["SEVERE. Table 3.1 contains THREE rows labelled 'Net interest', "
               "distinguished only by a heading several rows above: row 21 in "
               "millions of dollars, row 41 as a percentage of OUTLAYS, row 51 "
               "as a percentage of GDP. The spec quantity is net interest as a "
               "share of RECEIPTS. Row 41 is already a percentage and would look "
               "correct while carrying an entirely different denominator. Assert "
               "on the section heading, never on the row label alone."],
    ),
    PlannedSeries(
        domain=3, key="federal_receipts", label="Federal receipts, total",
        source="OMB Historical Tables", route=OMB_XLSX,
        identifier="hist01z1 / Table 1.1 / column 'Total Receipts'",
        expect_units="Millions of dollars", expect_frequency="Annual (FY)",
        orientation=+1, tier="Tier 1", confidence="confirmed", derived=True,
        coverage="single years from 1901; aggregate rows before that",
        notes="CONFIRMED 2026-08-11. Denominator for the net-interest share. "
              "Two-level header: row 2 spans Total / On-Budget / Off-Budget, "
              "row 3 names Receipts / Outlays / Surplus within each. The spec "
              "quantity is TOTAL receipts, the first numeric column.",
        traps=["The first two data rows are MULTI-YEAR AGGREGATES ('1789-1849', "
               "'1850-1900'), not years. Parsing them as years would inject two "
               "fabricated observations at the start of the series.",
               "On-Budget receipts appear in a later column with the same label "
               "'Receipts'. Total is the spec quantity; On-Budget excludes "
               "Social Security and is materially smaller."],
    ),

    # ---- Domain 4: corporate -------------------------------------------
    PlannedSeries(
        domain=4, key="corp_leverage", label="US nonfinancial net debt / EBITDA",
        source="IMF GFSR; S&P summaries", route="(transcription)",
        identifier="(manual)",
        expect_units="Ratio", expect_frequency="Annual (sparse)",
        orientation=-1, tier="Tier 3", confidence="manual",
        notes="TIER 3. Transcribed values with citation only -- never the GFSR "
              "PDF, its tables, or any bulk extract. Spec v0.2 carries a "
              "mechanical substitution to BIS NFC credit-to-GDP if coverage "
              "falls below 60 percent of any block's usable years.",
        blockers=["Cannot be scripted. Requires manual transcription."],
    ),

    # ---- Domain 5: household -------------------------------------------
    PlannedSeries(
        domain=5, key="saving_rate", label="Personal saving rate",
        source="BEA NIPA", route=BEA_API, identifier="NIPA/T20100/line35/A072RC",
        expect_units="Percent", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="confirmed",
        coverage="1929-2025 (97 annual observations)",
        notes="CONFIRMED 2026-08-11. Line description read from the API: "
              "'Personal saving as a percentage of disposable personal income', "
              "which matches Index Spec v0.2 section 3.1 word for word. Longer "
              "history than the FRED route would have provided.",
    ),

    # ---- Domain 6: health capacity -------------------------------------
    PlannedSeries(
        domain=6, key="hospital_beds", label="Hospital beds per 1,000 population",
        source="OECD Health Statistics", route=OECD_SDMX,
        identifier="DSD_HEALTH_REAC_HOSP@DF_BEDS_FUNC",
        expect_units="Per 1 000 inhabitants", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="reachable",
        notes="PRIMARY for domain 6 per docs/domain-6-decision.md. Dataflow "
              "identified 2026-08-11; the keyed query form returned 422 and the "
              "unkeyed form returns ~319k rows, so the filter syntax still needs "
              "settling. AHA was set aside for licence reasons (Tier 3), not "
              "because of its numbers.",
        traps=["Must be TOTAL hospital beds, not curative-only or ICU-only. "
               "DF_BEDS_FUNC carries several bed types under the same units."],
    ),

    # ---- Domain 7: social / associational -------------------------------
    PlannedSeries(
        domain=7, key="union_density", label="Union membership rate",
        source="BLS", route=BLS_API, identifier="LUU0204899600",
        expect_units="Percent", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="confirmed",
        coverage="verified 2005-2024; full span to be pulled",
        notes="CONFIRMED 2026-08-11. Returned 9.9 for 2024 and 10.0 for 2023, "
              "consistent with the published union membership rate. Was blocked "
              "by a 403 on 2026-08-02; api.bls.gov began answering by "
              "2026-08-11. The registration key lifts the span cap from 10 to "
              "20 years per query.",
    ),

    # ---- Domain 8: food -------------------------------------------------
    PlannedSeries(
        domain=8, key="grain_stocks_use",
        label="US grain stocks-to-use (corn, wheat, soybeans)",
        source="USDA NASS QuickStats", route=NASS_API, identifier="(query TBD)",
        expect_units="Ratio (derived)", expect_frequency="Annual (marketing year)",
        orientation=+1, tier="Tier 1", confidence="reachable",
        notes="Key validated 2026-08-11; CORN, WHEAT and SOYBEANS all present in "
              "the commodity list. The USDA FAS route used on 2026-08-02 stopped "
              "answering by 2026-08-11, which is why NASS moved from optional to "
              "required. Marketing years map to the year in which they BEGIN "
              "(harvest-year convention, Index Spec v0.2 section 3.1).",
        traps=["Stocks-to-use is DERIVED: ending stocks divided by total use, "
               "per crop, then an unweighted mean of the three ratios. Do not "
               "fetch a published 'stocks to use' figure and assume it matches "
               "the frozen construction."],
    ),
]

# Supplementary tier. Post-freeze, descriptive only, excluded from Study 2.
# See SUPPLEMENTARY.md.
SUPPLEMENTARY: list[PlannedSeries] = [
    PlannedSeries(
        domain=0, key="student_teacher", label="NCES student-teacher ratios",
        source="NCES Digest", route="https://nces.ed.gov/programs/digest/",
        identifier="(table TBD)", expect_units="Ratio",
        expect_frequency="Annual", orientation=-1, tier="Tier 1",
        confidence="reachable",
        notes="SUPPLEMENTARY. Inverted: a lower ratio means more capacity. "
              "Confound to state on the chart -- a falling ratio can mean more "
              "teachers or fewer students.",
    ),
    PlannedSeries(
        domain=0, key="nurses_per_capita",
        label="BLS OES registered nurses per capita",
        source="BLS OES", route=BLS_API, identifier="(OES series TBD)",
        expect_units="Employment per 1,000", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="reachable",
        notes="SUPPLEMENTARY, domain-6 staffing companion. NEVER enters Study 2. "
              "Confound to state on the chart -- nurse hiring tracks demand, so "
              "it can rise exactly when a buffer measure should show strain.",
    ),
    PlannedSeries(
        domain=0, key="nerc_reserve_margin",
        label="NERC regional reserve margins",
        source="NERC LTRA", route="https://www.nerc.com/pa/RAPA/ra/",
        identifier="(per-region, TBD)", expect_units="Percent",
        expect_frequency="Annual", orientation=+1, tier="Tier 1",
        confidence="reachable",
        notes="SUPPLEMENTARY. PER-REGION ONLY, no national splice -- spec v0.2 "
              "section 3.2 rejected a national grid series because the "
              "regional-entity map was reorganised repeatedly. Annotate the "
              "methodology breaks on-chart.",
    ),
]


def by_domain() -> dict[int, list[PlannedSeries]]:
    out: dict[int, list[PlannedSeries]] = {}
    for s in REGISTRY:
        out.setdefault(s.domain, []).append(s)
    return out


def by_confidence() -> dict[str, list[PlannedSeries]]:
    out: dict[str, list[PlannedSeries]] = {}
    for s in REGISTRY:
        out.setdefault(s.confidence, []).append(s)
    return out


def all_blockers() -> list[tuple[str, str]]:
    return [(s.key, b) for s in REGISTRY for b in s.blockers]


def all_traps() -> list[tuple[str, str]]:
    return [(s.key, t) for s in REGISTRY for t in s.traps]


if __name__ == "__main__":
    print("Series registry - rewritten 2026-08-11")
    print("")
    order = ["confirmed", "reachable", "unrouted", "manual"]
    groups = by_confidence()
    for level in order:
        items = groups.get(level, [])
        print("%s (%d)" % (level.upper(), len(items)))
        for s in items:
            flag = " [derived]" if s.derived else ""
            print("  d%d %-20s %-42s %s%s"
                  % (s.domain, s.key, s.label[:42], s.source, flag))
        print("")
    print("TRAPS (%d) - checked explicitly, not left to a units comparison:"
          % len(all_traps()))
    for key, t in all_traps():
        print("  [%s] %s" % (key, t))
    print("")
    print("BLOCKERS (%d):" % len(all_blockers()))
    for key, b in all_blockers():
        print("  [%s] %s" % (key, b))
