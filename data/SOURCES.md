# Data sources

One row per series. **Status: PLANNED. Nothing below has been retrieved.**

The data gate is closed. No series in this table has been fetched, opened, or
inspected, and no identifier has been verified against its source. Retrieval
dates are blank because no retrieval has occurred.

Machine-readable form: [`../scripts/fetch/series_registry.py`](../scripts/fetch/series_registry.py).
Fetch driver and gate guard: [`../scripts/fetch/fetch_all.py`](../scripts/fetch/fetch_all.py).

---

## Planned series

| Domain | Series | Source | Candidate identifier | Units (expected) | Freq. | Orient. | Tier | Retrieved |
|---|---|---|---|---|---|---|---|---|
| 1 | SPR crude stocks | EIA | `WCSSTUS1` | Thousands of barrels | Weekly | + | 1 | — |
| 1 | Refiner net crude input *(denominator)* | EIA | `WCRRIUS2` | Thou. bbl/day | Weekly | + | 1 | — |
| 2 | BIS credit-to-GDP gap, US private non-fin. | BIS | *(bulk download, endpoint TBD)* | pp of GDP | Quarterly | **−** | 2 | — |
| 3 | Federal debt held by the public, % GDP | OMB/CBO | `FYPUGDA188S` | Percent of GDP | Annual | **−** | 1 | — |
| 3 | Federal net interest outlays *(numerator)* | OMB/CBO | `FYOINT` | Millions USD | Annual | **−** | 1 | — |
| 3 | Federal receipts *(denominator)* | OMB/BEA | `FYFR` | Millions USD | Annual | + | 1 | — |
| 4 | Corporate net debt / EBITDA | IMF GFSR; S&P | *(transcribed)* | Ratio | Annual, sparse | **−** | **3** | — |
| 5 | Personal saving rate | BEA NIPA | `PSAVERT` | Percent | Monthly | + | 1 | — |
| 6 | **Health capacity — UNRESOLVED** | *(pending)* | *(pending)* | *(pending)* | Annual | + | *(pending)* | — |
| 7 | Union membership rate | BLS | `LUU0204899600` | Percent | Annual | + | 1 | — |
| 8 | Grain stocks-to-use (corn, wheat, soy) | USDA WASDE/NASS | *(WASDE tables, endpoint TBD)* | Ratio | Annual (mkt yr) | + | 1 | — |

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

| Series | Blocker |
|---|---|
| BIS credit gap | Tier 2 terms of use must be verified before any file is committed. Until verified, handle as Tier 3. |
| Corporate net debt/EBITDA | Tier 3 — transcription only, cannot be scripted. Spec v0.2 carries a mechanical substitution to BIS NFC credit-to-GDP if coverage falls below 60% of a block's usable years. |
| Health capacity | Author must choose the substitution. See [`../docs/domain-6-options.md`](../docs/domain-6-options.md). Not decided here. |

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
