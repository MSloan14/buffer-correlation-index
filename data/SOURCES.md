# Data sources

One row per series. <!-- BEGIN GENERATED: status -->
**Status: PLANNED. Nothing below has been retrieved.**

The data gate is closed. No series in this table has been fetched into
`data/raw/`, and the Retrieved column is blank because no retrieval has
occurred.

Identity is a separate question from retrieval, and the two are tracked
separately on purpose. **7 series have had their identity verified**
against a live response by
[`verify.py`](../scripts/fetch/verify.py) — the endpoint answers, the
returned series is the one the spec names, and the source-specific traps
were checked. 4 more are reachable but unverified, and 2 are Tier 3
transcriptions that cannot be scripted at all. Verifying an identity
reads metadata and a probe window; it is not the same as admitting the
series to the study, and it does not open the gate.
<!-- END GENERATED: status -->

Machine-readable form: [`../scripts/fetch/series_registry.py`](../scripts/fetch/series_registry.py).
Fetch driver and gate guard: [`../scripts/fetch/fetch_all.py`](../scripts/fetch/fetch_all.py).

---

## Planned series

<!-- BEGIN GENERATED: series -->
| Domain | Series | Source | Identifier | Units (expected) | Freq. | Orient. | Tier | Identity | Retrieved |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Refiner net crude oil input | EIA | `WCRRIUS2` | Thousand Barrels per Day | Weekly | + | 1 | *reachable, identity unverified* | — |
| 1 | SPR crude oil stocks | EIA | `WCSSTUS1` | Thousand Barrels | Weekly | + | 1 | *reachable, identity unverified* | — |
| 2 | BIS credit-to-GDP gap, US private non-financial | BIS | `WS_CREDIT_GAP / Q.US.P.A.C` | Percentage points of GDP | Quarterly | **−** | 2 | **verified** | — |
| 3 | Federal debt held by the public, % of GDP | OMB Historical Tables | `hist07z1 / Table 7.1 / column 8` | Percent of GDP | Annual (FY) | **−** | 1 | **verified** | — |
| 3 | Federal receipts, total | OMB Historical Tables | `hist01z1 / Table 1.1 / column 'Total Receipts'` | Millions of dollars | Annual (FY) | + | 1 | **verified** | — |
| 3 | Federal net interest outlays | OMB Historical Tables | `hist03z1 / Table 3.1 / row 21` | Millions of dollars | Annual (FY) | **−** | 1 | **verified** | — |
| 4 | BIS US nonfinancial-corporations credit-to-GDP (contingency) | BIS | *(endpoint TBD)* | Percent of GDP | Quarterly | **−** | 2 | *reachable, identity unverified* | — |
| 4 | Aggregate interest coverage ratio | IMF GFSR; S&P summaries | *(manual)* | Ratio | Annual (sparse) | + | **3** | *transcription* | — |
| 4 | US nonfinancial net debt / EBITDA | IMF GFSR; S&P summaries | *(manual)* | Ratio | Annual (sparse) | **−** | **3** | *transcription* | — |
| 5 | Personal saving rate | BEA NIPA | `NIPA/T20100/line35/A072RC` | Percent | Annual | + | 1 | **verified** | — |
| 6 | Hospital beds per 1,000 population | OECD Health Statistics | `DSD_HEALTH_REAC_HOSP@DF_BEDS_FUNC / USA.HB.10P3HB._Z._Z._T._T._Z._Z` | Per 1 000 inhabitants | Annual | + | 1 | **verified** | — |
| 7 | Union membership rate | BLS | `LUU0204899600` | Percent | Annual | + | 1 | **verified** | — |
| 8 | US grain stocks-to-use (corn, wheat, soybeans) | USDA ERS balance sheets (Feed Grains, Wheat Data, Oil Crops) | `Feed Grains Yearbook (corn) / Wheat Data-All Years / Oil Crops Yearbook (soybeans)` | Ratio (derived) | Annual (marketing year) | + | 1 | *reachable, identity unverified* | — |
<!-- END GENERATED: series -->

**Orientation** is applied before any other computation: `+` means higher = more
buffer; `−` means the series is inverted first.

## Every identifier is unverified, and that is a real risk

None of the identifiers above has been checked against its source, because
checking would have meant data contact — a FRED series page renders the current
value and the full history as a chart, which is exactly what the gate protects.

**A wrong identifier does not fail loudly.** It returns a different real series
with plausible units, and every downstream number is quietly about the wrong
quantity. Two specific traps already identified:

- **Domain 3 debt:** the required series is federal debt held by *the public* as
  a share of GDP. A total-public-debt series is a different quantity, is
  similarly named, and would pass a units check unnoticed.
- **Domains 1 and 3:** several entries are numerators or denominators of derived
  ratios, not the analysis series themselves. Fetching one and treating it as
  the buffer measure would be a silent error.

`verify_registry()` in the fetch driver must run at gate-open, before any
analysis, and reject any series whose returned title, units, or frequency does
not match its expectation.

## Open blockers

<!-- BEGIN GENERATED: blockers -->
| Series | Blocker |
|---|---|
| BIS US nonfinancial-corporations credit-to-GDP (contingency) | Do not fetch unless the coverage rule has actually fired, and record that it fired. |
| BIS US nonfinancial-corporations credit-to-GDP (contingency) | BORROWER CODE NOT PINNED. Domain 2 settled on TC_BORROWERS = P (private non-financial). The nonfinancial-corporations code for the GAP flow was NOT established - BIS may publish gaps for the total private non-financial sector only, in which case this contingency needs the total-credit RATIO flow instead and is a different quantity from domain 2's. Settle that BEFORE the coverage rule can be allowed to fire, not after. |
| Aggregate interest coverage ratio | Cannot be scripted. Requires manual transcription. |
| US nonfinancial net debt / EBITDA | Cannot be scripted. Requires manual transcription. |
| Hospital beds per 1,000 population | COVERAGE CLIFF - a data reality, not an identifier problem, and potentially decisive for the headline. US beds data currently ENDS AT 2022. The crisis-excluded third block B3ex is {2018, 2019, 2022, 2023, 2024, 2025}, so beds cover 3 of 6 years = 50 percent, BELOW spec v0.2 section 5's 60-percent block-coverage rule. On today's data domain 6 falls out of the verdict-bearing B3 block entirely. If OECD publishes US 2023 before Phase 3 the figure becomes 4 of 6 = 66.7 percent and it stays in. No route change fixes this; watch it at every OECD health release, and if it does not resolve, report domain 6 as excluded by the coverage rule rather than quietly carrying three points. |
| US grain stocks-to-use (corn, wheat, soybeans) | Do not improvise a denominator and do not substitute a published stocks-to-use figure for the frozen three-crop construction. The route is now sourced but NOT yet read: only the corn documentation was confirmed to describe a total-disappearance line. Open the wheat and soybean workbooks at gate-open and assert an EXPLICIT total-use column in each before building anything. |
| US grain stocks-to-use (corn, wheat, soybeans) | TAIL-YEAR VINTAGE DECISION, unresolved. The Oil Crops Yearbook revises annually in March, so the newest marketing year may exist only in current WASDE/PSD at retrieval. That is a vintage choice and the spec forbids vintage selection - so decide the rule in advance and record it, rather than picking whichever source happens to have the tail year. |
<!-- END GENERATED: blockers -->

## Column meanings

- **Candidate identifier** — recorded from prior knowledge, unverified. Where an
  endpoint is marked TBD, no route has been confirmed.
- **Units / Freq.** — what the series is *expected* to return. These are
  assertions to be tested at gate-open, not observations.
- **Retrieved** — retrieval date in UTC, filled at fetch time from the fetch
  script's own output. Backfilling this from memory later would make it
  worthless.

## Standing rules

1. Nothing enters `data/raw/` without a row here.
2. Files in `data/raw/` are never hand-edited. If a series is wrong, re-fetch and
   add a new row.
3. Tier is decided before retrieval. If a source's tier is unclear at fetch time,
   it is Tier 3 until proven otherwise.
4. Prefer the issuing agency over an aggregator; record the originating source,
   never merely "FRED".
