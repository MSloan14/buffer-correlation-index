#!/usr/bin/env python3
"""Registry of planned series. NOTHING HERE HAS BEEN FETCHED OR VERIFIED.

This file is written while the data gate is CLOSED. Every identifier below is a
**candidate**, recorded from prior knowledge, and every one carries
`verified=False`. None has been checked against its source.

## Why the identifiers are unverified

The task brief permitted verifying identifiers against "source documentation
pages (titles, units, frequency, coverage)". For FRED that is not separable from
data contact: a series page renders the current value and a chart of the entire
history. Those are precisely the levels and trajectories the ratchet criterion
would key on. Verifying by that route would have spent the blindness the gate
exists to protect, so it was not done.

## The failure mode this creates, stated plainly

A wrong identifier does not error. It silently fetches a *different real series*
with plausible units, and every downstream number is quietly about the wrong
thing. `verify_registry()` in `fetch_all.py` therefore runs at gate-open and
checks each fetched series against the `expect_*` fields below BEFORE any
analysis. A series whose returned title, units, or frequency does not match its
expectation is not used.

Orientation follows Ratchet Spec section 3 and Index Spec v0.2 section 3.1:
positive means higher = more buffer.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlannedSeries:
    domain: int
    key: str
    label: str
    source: str
    identifier: str                  # CANDIDATE - unverified
    url_template: str
    expect_units: str
    expect_frequency: str
    orientation: int                 # +1 higher = more buffer, -1 = invert
    tier: str                        # DATA_TERMS.md tier
    verified: bool = False
    confidence: str = "low"          # low | medium - never high before checking
    notes: str = ""
    blockers: list[str] = field(default_factory=list)


FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={id}"

REGISTRY: list[PlannedSeries] = [
    # --- Domain 1: strategic reserve -------------------------------------
    PlannedSeries(
        domain=1, key="spr_stocks", label="SPR crude oil stocks",
        source="EIA", identifier="WCSSTUS1",
        url_template=FRED_CSV,
        expect_units="Thousands of Barrels", expect_frequency="Weekly",
        orientation=+1, tier="Tier 1", confidence="medium",
        notes="EIA weekly SPR stocks; FRED mirrors the EIA series. Native EIA "
              "API is the preferred route per DATA_TERMS (issuing agency first).",
    ),
    PlannedSeries(
        domain=1, key="refinery_inputs", label="Refiner net crude oil input",
        source="EIA", identifier="WCRRIUS2",
        url_template=FRED_CSV,
        expect_units="Thousands of Barrels per Day", expect_frequency="Weekly",
        orientation=+1, tier="Tier 1", confidence="low",
        notes="Denominator only. The coverage ratio is stocks / trailing-12-month "
              "mean daily inputs; it is DERIVED, not fetched.",
    ),

    # --- Domain 2: financial ---------------------------------------------
    PlannedSeries(
        domain=2, key="credit_gap", label="BIS credit-to-GDP gap, US private non-financial",
        source="BIS", identifier="BIS credit-gap statistics (bulk download)",
        url_template="(BIS statistics portal - exact endpoint TBD at gate)",
        expect_units="Percentage points of GDP", expect_frequency="Quarterly",
        orientation=-1, tier="Tier 2", confidence="low",
        notes="Spec v0.2 section 3.1: PUBLISHED VALUES ONLY, not re-derived. "
              "Do not recompute the one-sided HP filter.",
        blockers=["BIS terms of use must be verified before any file is "
                  "committed (DATA_TERMS Tier 2). Until verified, treat Tier 3."],
    ),

    # --- Domain 3: fiscal -------------------------------------------------
    PlannedSeries(
        domain=3, key="debt_held_public_gdp", label="Federal debt held by the public, % of GDP",
        source="OMB / CBO (FRED mirror permitted by spec)", identifier="FYPUGDA188S",
        url_template=FRED_CSV,
        expect_units="Percent of GDP", expect_frequency="Annual",
        orientation=-1, tier="Tier 1", confidence="low",
        notes="CAUTION: must be debt held by the PUBLIC, not total public debt. "
              "Total-debt series (e.g. GFDEGDQ188S) is a DIFFERENT and wrong "
              "quantity here and would pass a units check unnoticed.",
    ),
    PlannedSeries(
        domain=3, key="net_interest", label="Federal net interest outlays",
        source="OMB Historical Tables / CBO", identifier="FYOINT",
        url_template=FRED_CSV,
        expect_units="Millions of Dollars", expect_frequency="Annual",
        orientation=-1, tier="Tier 1", confidence="low",
        notes="Numerator only; the spec quantity is net interest as % of federal "
              "RECEIPTS, so it is derived against the receipts series below.",
    ),
    PlannedSeries(
        domain=3, key="federal_receipts", label="Federal current receipts",
        source="OMB / BEA", identifier="FYFR",
        url_template=FRED_CSV,
        expect_units="Millions of Dollars", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="low",
        notes="Denominator only. Fiscal-year alignment per Index Spec v0.2 "
              "section 1: FY t maps to calendar year t.",
    ),

    # --- Domain 4: corporate ---------------------------------------------
    PlannedSeries(
        domain=4, key="corp_net_debt_ebitda", label="US nonfinancial net debt / EBITDA",
        source="IMF GFSR; S&P / rating-agency summaries", identifier="(transcribed)",
        url_template="(none - transcription only)",
        expect_units="Ratio", expect_frequency="Annual (sparse)",
        orientation=-1, tier="Tier 3", confidence="low",
        notes="TIER 3. Transcribed numeric values with citation ONLY. Never the "
              "GFSR PDF, its tables, or any bulk extract. Spec v0.2 carries a "
              "mechanical substitution rule to BIS NFC credit-to-GDP if coverage "
              "falls below 60% of any block's usable years.",
        blockers=["Requires manual transcription; cannot be scripted."],
    ),

    # --- Domain 5: household ----------------------------------------------
    PlannedSeries(
        domain=5, key="saving_rate", label="Personal saving rate",
        source="BEA NIPA", identifier="PSAVERT",
        url_template=FRED_CSV,
        expect_units="Percent", expect_frequency="Monthly",
        orientation=+1, tier="Tier 1", confidence="medium",
        notes="Enters the annual index as the calendar-year mean of monthly values.",
    ),

    # --- Domain 6: health capacity ---------------------------------------
    #  DELIBERATELY UNRESOLVED. See docs/domain-6-options.md. The author decides.
    PlannedSeries(
        domain=6, key="health_capacity", label="(UNRESOLVED - see domain-6 options memo)",
        source="(pending author decision)", identifier="(pending)",
        url_template="(pending)",
        expect_units="(pending)", expect_frequency="Annual",
        orientation=+1, tier="(pending)", confidence="low",
        notes="AHA Hospital Statistics is Tier 3 and cannot be redistributed. "
              "Beds per 1,000 measures physical plant; the binding constraint is "
              "staffed capacity. Options memo prepared; NOT decided here.",
        blockers=["Author must choose the substitution. Do not decide "
                  "unilaterally. See docs/domain-6-options.md."],
    ),

    # --- Domain 7: social / associational ---------------------------------
    PlannedSeries(
        domain=7, key="union_density", label="Union membership rate",
        source="BLS Union Members release", identifier="LUU0204899600",
        url_template=FRED_CSV,
        expect_units="Percent", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="low",
        notes="CPS-based, consistent from 1983. Spec v0.2 notes this is a "
              "data-quality-over-construct-validity choice; union density is an "
              "organised-associational-capacity proxy, not social connection.",
    ),

    # --- Domain 8: food ----------------------------------------------------
    PlannedSeries(
        domain=8, key="grain_stocks_use", label="US grain stocks-to-use (corn, wheat, soybeans)",
        source="USDA WASDE / NASS", identifier="(WASDE tables; endpoint TBD)",
        url_template="(USDA - exact endpoint TBD at gate)",
        expect_units="Ratio", expect_frequency="Annual (marketing year)",
        orientation=+1, tier="Tier 1", confidence="low",
        notes="Unweighted mean of ending-stocks/total-use for the three crops. "
              "Marketing years map to the year in which they BEGIN "
              "(harvest-year convention, Index Spec v0.2 section 3.1) - a "
              "disclosed deviation from the fiscal-year majority rule.",
    ),
]


def by_domain() -> dict[int, list[PlannedSeries]]:
    out: dict[int, list[PlannedSeries]] = {}
    for s in REGISTRY:
        out.setdefault(s.domain, []).append(s)
    return out


def all_blockers() -> list[tuple[str, str]]:
    return [(s.key, b) for s in REGISTRY for b in s.blockers]


if __name__ == "__main__":
    print("Planned series registry - NOTHING FETCHED, NOTHING VERIFIED")
    print("")
    for domain, items in sorted(by_domain().items()):
        print("Domain %d" % domain)
        for s in items:
            print("  %-22s %-34s id=%-22s conf=%s verified=%s"
                  % (s.key, s.label[:34], s.identifier[:22], s.confidence,
                     s.verified))
    print("")
    print("BLOCKERS (%d):" % len(all_blockers()))
    for key, b in all_blockers():
        print("  [%s] %s" % (key, b))
