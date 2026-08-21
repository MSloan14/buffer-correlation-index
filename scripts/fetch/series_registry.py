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
BIS_SDMX = "https://stats.bis.org/api/v2/data/dataflow/BIS/{flow}/1.0/{key}?format=csv"
ERS_FILE = "https://www.ers.usda.gov/(see identifier)"
OMB_XLSX = "https://www.whitehouse.gov/wp-content/uploads/2026/04/{table}_fy2027.xlsx"

REGISTRY: list[PlannedSeries] = [
    # ---- Domain 1: strategic reserve -----------------------------------
    PlannedSeries(
        domain=1, key="spr_stocks", label="SPR crude oil stocks",
        source="EIA", route=EIA_BULK, identifier="WCSSTUS1",
        expect_units="Thousand Barrels", expect_frequency="Weekly",
        orientation=+1, tier="Tier 1", confidence="confirmed",
        notes="SETTLED 2026-08-20. WCSSTUS1 is 'Weekly U.S. Ending Stocks of "
              "Crude Oil in SPR', thousand barrels, 1982-08-20 to current. "
              "Enters the annual index as a calendar-year mean per Index Spec "
              "v0.2 section 1. Spec says million bbl and the source publishes "
              "THOUSAND - convert at build, do not relabel the source.",
        traps=["Must be SPR stocks specifically, NOT total US commercial crude "
               "stocks. Both are weekly, both in thousand barrels, and a mixup "
               "would pass any units check.",
               "Coverage must reach the SPR's own history (fill began in the "
               "late 1970s). A route starting in 2000 leaves Study 2 without "
               "early episodes for this domain.",
               "THE REGISTRY'S OWN ROUTE TRIPPED THIS TRAP. The weekly series "
               "starts 1982-08-20, which is AFTER the fill began, so the trap "
               "above was written against a route that could not satisfy it. "
               "The monthly MER counterpart MCSSTUS1 reaches January 1977 and "
               "covers the full history. Decide weekly-vs-monthly on how much "
               "1977-1982 depth Study 2 needs, and record the choice; do not "
               "silently accept the 1982 start as if it were the series' own "
               "beginning."],
    ),
    PlannedSeries(
        domain=1, key="refinery_inputs", label="Refiner net crude oil input",
        source="EIA", route=EIA_BULK, identifier="WCRRIUS2",
        expect_units="Thousand Barrels per Day", expect_frequency="Weekly",
        orientation=+1, tier="Tier 1", confidence="confirmed", derived=True,
        notes="Denominator only. The coverage ratio is SPR stocks divided by "
              "trailing-12-month mean daily inputs, and is DERIVED here, not "
              "fetched as a series.",
        traps=["This is a denominator. It must never be charted or scored as a "
               "buffer series in its own right.",
               "Refiner NET crude input, GROSS inputs to refineries, and crude "
               "'product supplied' are three different weekly series in "
               "thousand barrels per day. RESOLVED 2026-08-20 in favour of "
               "NET, and the reasoning is recorded because the spec never uses "
               "the word: spec v0.2 section 3.1 says 'crude inputs to "
               "refineries', which names a CRUDE-ONLY quantity. EIA's "
               "crude-only input series is refiner NET input. 'Gross inputs' "
               "(WGIRIUS2) measures total inputs to distillation units "
               "INCLUDING unfinished oils, so it is not 'crude inputs', and "
               "it starts only in Jan 1990. The chosen identifier was already "
               "consistent with this; the judgement is now on the record "
               "rather than implicit in a series code.",
               "Monthly counterpart MCRRIUS2 reaches Jan 1961, should the "
               "weekly 1982 start prove too short for the denominator."],
    ),

    # ---- Domain 2: financial -------------------------------------------
    PlannedSeries(
        domain=2, key="credit_gap",
        label="BIS credit-to-GDP gap, US private non-financial",
        source="BIS", route=BIS_SDMX, identifier="WS_CREDIT_GAP / Q.US.P.A.C",
        expect_units="Percentage points of GDP", expect_frequency="Quarterly",
        orientation=-1, tier="Tier 2", confidence="confirmed",
        coverage="1957-Q4 to 2025-Q4, quarterly",
        notes="SETTLED 2026-08-20. Dataflow BIS/WS_CREDIT_GAP/1.0, dimension "
              "order FREQ.BORROWERS_CTY.TC_BORROWERS.TC_LENDERS.CG_DTYPE, key "
              "Q.US.P.A.C - quarterly, United States, P = private "
              "non-financial borrowers, A = all lending sectors, C = "
              "credit-to-GDP gap (actual minus trend). Read live: 2025-Q4 = "
              "-11.54, consistent with the well-known deeply negative US gap. "
              "Spec v0.2 section 3.1: PUBLISHED VALUES ONLY. Do not recompute "
              "the one-sided HP filter (lambda = 400,000); the .C code IS the "
              "published gap, which is what makes that rule satisfiable.",
        traps=["Gap vs ratio vs trend. BIS publishes the credit-to-GDP RATIO, "
               "its estimated TREND, and the GAP between them. All three are in "
               "percent-of-GDP units. Only the GAP is the spec quantity.",
               "Borrower sector. Total private non-financial is the spec "
               "quantity; households and nonfinancial corporations publish in "
               "the same shape. The NFC series is domain 4's fallback, so a "
               "sector slip either duplicates domain 2 or corrupts both.",
               "Lender basis. Credit from ALL SECTORS and bank credit only are "
               "different series in the same units.",
               "AN UNPINNED KEY SILENTLY RETURNS ALL THREE. For advanced "
               "economies the flow serves ratio, trend AND gap under "
               "constraint CTG_GAPS_ADV_ECON (CG_DTYPE A/B/C), interleaved in "
               "one response. The key must end in .C. This is the gap-vs-ratio "
               "trap above, but as a retrieval failure rather than a reading "
               "one - it produces three times as many rows, not wrong units.",
               "UNITS LABEL MISMATCH, and it will false-fail a correct series. "
               "The SDMX response labels unit 770 = 'Percentage of GDP' even "
               "for the gap, whereas a gap is semantically in percentage "
               "POINTS of GDP. expect_units here keeps the correct semantics; "
               "the verifier must therefore assert on the CG_DTYPE code, not "
               "on the unit string."],
    ),

    # ---- Domain 3: fiscal ----------------------------------------------
    PlannedSeries(
        domain=3, key="debt_held_public",
        label="Federal debt held by the public, % of GDP",
        source="OMB Historical Tables", route=OMB_XLSX,
        identifier="hist07z1 / Table 7.1 / column 8",
        expect_units="Percent of GDP", expect_frequency="Annual (FY)",
        orientation=-1, tier="Tier 1", confidence="confirmed",
        coverage="FY1940-2025, 86 annual observations",
        notes="CONFIRMED 2026-08-20. Replaces the Treasury debt_to_penny route, "
              "which was the right quantity built the wrong way: a daily dollar "
              "level divided by BEA calendar-year GDP, starting ~1993. Table 7.1 "
              "publishes the ratio DIRECTLY as a fiscal-year figure, which is what "
              "spec v0.2 section 3.1 names (OMB/CBO annual). Read live: 2025 = "
              "99.5 percent held by the public against 123.3 percent gross. Three "
              "consequences - no GDP denominator is needed, the FY-vs-CY alignment "
              "judgement disappears because the published ratio is already "
              "fiscal-year, and coverage runs from FY1940 instead of ~1993, which "
              "is what makes pre-2000 episodes available to Study 2 at all.",
        traps=["THE RECORDED TRAP, still live. Column 6 is GROSS federal debt as a "
               "percent of GDP; column 8 is HELD BY THE PUBLIC. For 2025 they read "
               "123.3 and 99.5 - both plausible, both percentages.",
               "Table 7.1 has TWO sections with IDENTICAL sub-headers: columns 1-5 "
               "are 'In Millions of Dollars', columns 6-10 are 'As Percentages of "
               "GDP'. Column 3 and column 8 both read 'Equals: Held by the Public "
               "/ Total'. Assert on the ROW-1 section header.",
               "Within 'Held by the Public' the row-3 split is Total / Federal "
               "Reserve System / Other at columns 8 / 9 / 10. Column 9 is a much "
               "smaller but entirely plausible percentage.",
               "Years are TEXT in this workbook, as in Table 1.1. A numeric-only "
               "parser returns an empty series rather than erroring.",
               "RETRACTED 2026-08-21, and the retraction matters. This slot "
               "read \"FY2027 edition extends past the last actual year, trim "
               "projections\". Read live: Table 7.1 ends at FY2025 and goes "
               "straight to its footnotes, with NO estimate rows. Only Table "
               "3.1 carries projections. A false trap is not inert - a fetcher "
               "told to cut at an actual/estimate boundary that does not exist "
               "can invent one and silently drop real observations."],
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
              "budget edition and extends past the last actual year. PINNED "
              "2026-08-21 - row 1 carries 92 year headers, 1940 through 2031 "
              "estimate, of which the LAST SIX are projections and one (TQ) is "
              "the 1976 transition quarter. The actual/estimate boundary falls "
              "after FY2025, matching Tables 1.1 and 7.1, which simply stop "
              "there. Data cells are numeric; it is the HEADERS that are text.",
        traps=["SEVERE. Table 3.1 contains THREE rows labelled 'Net interest', "
               "distinguished only by a heading several rows above: row 21 in "
               "millions of dollars, row 41 as a percentage of OUTLAYS, row 51 "
               "as a percentage of GDP. The spec quantity is net interest as a "
               "share of RECEIPTS. Row 41 is already a percentage and would look "
               "correct while carrying an entirely different denominator. Assert "
               "on the section heading, never on the row label alone.",
               "FY2027 edition extends past the last actual year. Untrimmed, "
               "projection years enter the ratchet detector's sigma and episode "
               "set as if they were observations.",
               "TRANSPOSED. Table 3.1 is laid out the OTHER WAY UP from Tables "
               "1.1 and 7.1: years run ACROSS row 1 as column headers and "
               "functions run DOWN column 0. A parser written against the "
               "sibling tables finds no year rows and returns an empty series "
               "without erroring. Confirmed live 2026-08-21.",
               "The missing-data sentinel is ten literal periods, 189 of them "
               "in this workbook. float() raises on it; a bare except that "
               "falls back to 0.0 injects fabricated zeros into a level "
               "series. Skip these cells, never zero-fill.",
               "In the two percentage sections a bare asterisk means 0.05 "
               "percent or less, not missing. It does not appear in the "
               "dollars section this series reads, but it does appear in the "
               "rows a units check might cross-reference.",
               "TQ (transition quarter, 1976) is a COLUMN here, not a row - "
               "the consequence of the transposition above. An isdigit() year "
               "filter drops it, which is correct, and also drops the six "
               "estimate headers. Both outcomes are right, but make them "
               "deliberate: assert what was dropped, do not rely on it."],
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
    PlannedSeries(
        domain=4, key="corp_coverage", label="Aggregate interest coverage ratio",
        source="IMF GFSR; S&P summaries", route="(transcription)",
        identifier="(manual)",
        expect_units="Ratio", expect_frequency="Annual (sparse)",
        orientation=+1, tier="Tier 3", confidence="manual",
        notes="Spec v0.2 section 3.1 sub-series 4b. Section 5 defines domain 4 as "
              "the unweighted mean of its sub-series z-scores, so 4a alone is HALF "
              "A DOMAIN. This entry was missing entirely from the 2026-08-11 "
              "registry and was found by independent review; without it domain 4 "
              "would have been built short with every check passing. Orientation "
              "is POSITIVE here and negative on 4a - higher coverage is more "
              "buffer, higher leverage is less.",
        blockers=["Cannot be scripted. Requires manual transcription."],
    ),
    PlannedSeries(
        domain=4, key="corp_bis_fallback",
        label="BIS US nonfinancial-corporations credit-to-GDP (contingency)",
        source="BIS", route="https://data.bis.org/", identifier="(endpoint TBD)",
        expect_units="Percent of GDP", expect_frequency="Quarterly",
        orientation=-1, tier="Tier 2", confidence="reachable",
        notes="NOT fetched by default. Spec v0.2 section 3.1 carries a MECHANICAL "
              "substitution: if the corporate domain covers less than 60 percent "
              "of any analysis block's usable years, domain 4 switches to this for "
              "the FULL window. Registered so the contingency has a route rather "
              "than being improvised if it fires.",
        traps=["If this fires it shares construction with domain 2 (both BIS "
               "credit-to-GDP), so a nonzero slice of measured co-movement is "
               "artifactual. Spec makes the drop-corporate sensitivity run "
               "MANDATORY reporting in that case.",
               "Sector: NONFINANCIAL CORPORATIONS, not total private "
               "non-financial. Taking the domain-2 series here silently "
               "duplicates domain 2."],
        blockers=["Do not fetch unless the coverage rule has actually fired, and "
                  "record that it fired.",
                  "BORROWER CODE NOT PINNED. Domain 2 settled on TC_BORROWERS "
                  "= P (private non-financial). The nonfinancial-corporations "
                  "code for the GAP flow was NOT established - BIS may publish "
                  "gaps for the total private non-financial sector only, in "
                  "which case this contingency needs the total-credit RATIO "
                  "flow instead and is a different quantity from domain 2's. "
                  "Settle that BEFORE the coverage rule can be allowed to "
                  "fire, not after."],
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
        identifier="DSD_HEALTH_REAC_HOSP@DF_BEDS_FUNC / "
                   "USA.HB.10P3HB._Z._Z._T._T._Z._Z",
        expect_units="Per 1 000 inhabitants", expect_frequency="Annual",
        orientation=+1, tier="Tier 1", confidence="confirmed",
        coverage="1960-2022; 1961-64 and 1966-69 missing; 2000-2022 complete",
        notes="SETTLED 2026-08-20. PRIMARY for domain 6 per "
              "docs/domain-6-decision.md. The 422 is explained: the key needs "
              "exactly NINE positions (eight dots) - "
              "REF_AREA.MEASURE.UNIT_MEASURE.STATISTICAL_OPERATION."
              "OWNERSHIP_TYPE.HEALTH_FUNCTION.CARE_TYPE.MEDICAL_TECH."
              "HEALTH_CARE_PROVIDER - and the earlier attempt supplied the "
              "wrong count, which SDMX rejects rather than defaulting. Read "
              "live: 2000 = 3.49, 2019 = 2.80, 2022 = 2.75, matching the known "
              "US level. AHA was set aside for licence reasons (Tier 3), not "
              "because of its numbers.",
        traps=["Must be TOTAL hospital beds, not curative-only or ICU-only. "
               "DF_BEDS_FUNC carries several bed types under the same units. "
               "MEASURE=HB is total beds and ICU variants are separate MEASURE "
               "codes; HEALTH_FUNCTION=_T is Total and HC1 is curative-only.",
               "UNIT_MEASURE MUST BE PINNED. 10P3HB (per 1,000 inhabitants) "
               "and BD (absolute bed counts) coexist under the same measure. "
               "An unpinned unit dimension does not default to the rate."],
        blockers=["COVERAGE CLIFF - a data reality, not an identifier problem, "
                  "and potentially decisive for the headline. US beds data "
                  "currently ENDS AT 2022. The crisis-excluded third block "
                  "B3ex is {2018, 2019, 2022, 2023, 2024, 2025}, so beds cover "
                  "3 of 6 years = 50 percent, BELOW spec v0.2 section 5's "
                  "60-percent block-coverage rule. On today's data domain 6 "
                  "falls out of the verdict-bearing B3 block entirely. If OECD "
                  "publishes US 2023 before Phase 3 the figure becomes 4 of 6 "
                  "= 66.7 percent and it stays in. No route change fixes this; "
                  "watch it at every OECD health release, and if it does not "
                  "resolve, report domain 6 as excluded by the coverage rule "
                  "rather than quietly carrying three points."],
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
        traps=["'Members of unions' and 'Represented by unions' are different "
               "BLS series, both percentages, roughly 1.2 points apart, with "
               "nearly identical identifiers. The spec quantity is MEMBERSHIP.",
               "Coverage must reach back to 1983, the CPS-consistent span the "
               "spec cites as the reason this series was chosen over GSS trust. "
               "Verified only 2005-2024 so far."],
    ),

    # ---- Domain 8: food -------------------------------------------------
    PlannedSeries(
        domain=8, key="grain_stocks_use",
        label="US grain stocks-to-use (corn, wheat, soybeans)",
        source="USDA ERS balance sheets (Feed Grains, Wheat Data, Oil Crops)",
        route=ERS_FILE,
        identifier="Feed Grains Yearbook (corn) / Wheat Data-All Years / "
                   "Oil Crops Yearbook (soybeans)",
        expect_units="Ratio (derived)", expect_frequency="Annual (marketing year)",
        orientation=+1, tier="Tier 1", confidence="reachable",
        notes="Key validated 2026-08-11. Marketing years map to the year in which "
              "they BEGIN (harvest-year convention, Index Spec v0.2 section 3.1). "
              "NASS STRUCTURE CONFIRMED 2026-08-20, and it does NOT supply this "
              "domain on its own. Queried live: statisticcat_desc for CORN returns "
              "46 categories of which exactly one is STOCKS, with NO use, "
              "disappearance, utilization or supply category anywhere - the "
              "denominator is simply absent. reference_period_desc for CORN STOCKS "
              "returns only FIRST OF MAR / JUN / SEP / DEC, so there is NO "
              "marketing-year ending-stocks period. short_desc returns three "
              "variants: all positions, OFF FARM, ON FARM. NASS therefore gives a "
              "QUARTERLY numerator split by position and nothing else, and both "
              "halves of the recorded trap were real. The denominator needs a "
              "balance-sheet source; reachable 2026-08-20 are the ERS Feed Grains "
              "database, the WASDE archive at Cornell ESMIS, and USDA FAS PSD "
              "(which answered again after refusing connections on 2026-08-11). "
              "RESOLVED 2026-08-20 to ERS, and BOTH halves of each ratio now "
              "come from the SAME balance sheet. Mixing a NASS numerator with "
              "an ERS denominator would pair two independently revised "
              "vintages; ERS supply-and-disappearance tables carry ending "
              "stocks and total use together, and are the WASDE-consistent "
              "published estimates that NASS stocks feed into, so this still "
              "satisfies the spec's 'WASDE/NASS published estimates' wording. "
              "The WASDE ARCHIVE was rejected for a specific reason: each "
              "WASDE carries only the current and prior marketing years, so "
              "the archive serves VINTAGES, while the spec demands the latest "
              "published estimate per marketing year - for MY 2000/01 that "
              "lives in today's revised ERS sheet, not in any archived WASDE. "
              "FAS PSD was rejected because it refuses without its own key "
              "(API_KEY_MISSING confirmed live; .env has BEA/NASS/BLS only) "
              "and its attribute set appears to carry Domestic Consumption and "
              "Exports but no explicit total-use line, so summing would brush "
              "against the no-construction rule.",
        traps=["Stocks-to-use is DERIVED: ending stocks divided by total use, "
               "per crop, then an unweighted mean of the three ratios. Do not "
               "fetch a published 'stocks to use' figure and assume it matches "
               "the frozen construction.",
               "QUARTERLY Grain Stocks (Dec 1 / Mar 1 / Jun 1 / Sep 1) are not "
               "marketing-year ENDING stocks. Dec 1 corn stocks are the "
               "post-harvest peak - a plausible thousand-bushel series that is "
               "the wrong quantity.",
               "On-farm and off-farm positions vs all positions.",
               "DOMESTIC use vs TOTAL use as the denominator. Total is the "
               "spec quantity.",
               "All wheat vs a single wheat class.",
               "The DENOMINATOR does not exist in QuickStats: total use is a "
               "WASDE/ERS balance-sheet item. CONFIRMED by live query, twice "
               "and independently. Kept as a trap because the numerator IS "
               "there, so a future revision could reasonably reach for NASS "
               "again and find half of what it needs.",
               "ERS discontinued the Feed Grains custom-query application in "
               "May 2025. Since January 2026 only the All Years Excel/CSV "
               "files are posted, so the corn route is a FILE PARSE, not a "
               "query API. A route written against the old query app fails.",
               "Latest published estimate per marketing year at retrieval, "
               "retrieval-date logged, NO vintage selection."],
        blockers=["Do not improvise a denominator and do not substitute a "
                  "published stocks-to-use figure for the frozen three-crop "
                  "construction. The route is now sourced but NOT yet read: "
                  "only the corn documentation was confirmed to describe a "
                  "total-disappearance line. Open the wheat and soybean "
                  "workbooks at gate-open and assert an EXPLICIT total-use "
                  "column in each before building anything.",
                  "TAIL-YEAR VINTAGE DECISION, unresolved. The Oil Crops "
                  "Yearbook revises annually in March, so the newest marketing "
                  "year may exist only in current WASDE/PSD at retrieval. That "
                  "is a vintage choice and the spec forbids vintage selection - "
                  "so decide the rule in advance and record it, rather than "
                  "picking whichever source happens to have the tail year."],
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
