# Data redistribution terms

What may and may not be committed to this repository, per source.

This file governs `data/`. It exists because a pre-registration that commits its
inputs for auditability can collide with the licence terms of those inputs. The
resolution used here is a split: freely redistributable sources are committed in
full; proprietary sources are represented only by transcribed numeric values
with a citation sufficient for a reader with their own licence to verify.

**Status of this document:** written before any data contact. No series listed
here has been retrieved. Rows marked UNDETERMINED are open items that must be
resolved before Phase 3.

---

## Tier 1 — Freely redistributable (US federal works)

Works of the US federal government are generally not subject to domestic
copyright protection. Raw files, derived tables, and transcribed values may all
be committed.

| Source | Domain use | Redistribution |
|---|---|---|
| EIA (Energy Information Administration) | Energy | Free |
| BEA (Bureau of Economic Analysis) | Macro accounts | Free |
| BLS (Bureau of Labor Statistics) | Labor | Free |
| OMB / CBO | Fiscal | Free |
| USDA | Food / agriculture | Free |
| NCHS (National Center for Health Statistics) | Health | Free |

**Caveat to verify at Phase 3:** federal *works* are unrestricted, but federal
publications sometimes embed third-party copyrighted material under licence.
Where a federal table is a repackaging of a commercial series, Tier 3 applies to
that series regardless of where it was obtained.

## Tier 2 — Redistributable with attribution

| Source | Domain use | Redistribution |
|---|---|---|
| BIS (Bank for International Settlements) | Credit / banking | Permitted **with attribution** |

BIS statistics are made available for use with attribution to the BIS.

**Verified 2026-08-20** against the BIS "Terms of permitted use of BIS
statistics" at <https://www.bis.org/terms_statistics.htm>, which reads:

> The use of the statistics is unrestricted, provided that: if the
> statistics are reproduced, the BIS must be cited in your publication or
> product as the source of the statistics; ... your use of the statistics
> must not be potentially misleading, for example by implying endorsement
> or affiliation with the BIS ...; if the statistics will be used in a
> commercial publication or product, their inclusion in the publication or
> product will not result in any additional charge to subscribers or other
> users; ... No other use is permissible.

Committing BIS credit-gap values to this public repository with attribution
sits inside "unrestricted ... provided" plus the citation condition. The
other operative conditions - no implied endorsement, no additional charge,
no warranty, not investment advice - are met by a non-commercial research
repository that cites the BIS as source.

**The Tier 3 holding rule is therefore lifted for BIS.** Redistribution with
attribution is permitted, and `data/raw/` may hold BIS files. This clears
the blocker that stood on the domain-2 credit gap.

## Tier 3 — Proprietary: transcribed values only

For these sources, **never commit** the source table, the source file, the PDF,
a scan, a screenshot, or a bulk extract. Commit only the specific numeric values
the analysis consumes, in a CSV under `data/processed/`, each with a citation
precise enough that a reader holding a licence can locate and check it.

| Source | Domain use | What may be committed |
|---|---|---|
| S&P / rating-agency corporate aggregates | Corporate credit (domain 4) | Transcribed numeric values + citation |
| AHA Hospital Statistics | Health capacity (domain 6) | Transcribed numeric values + citation |
| **IMF GFSR** | Corporate credit (domain 4) | Transcribed numeric values + citation. **Never** the GFSR chapter PDF, its tables, figures, or any bulk extract. |

A citation is sufficient if it names the publication, edition or year, table
number or identifier, and the row and column labels the value was taken from.

**Consequence for reproducibility, stated plainly:** a reader without a licence
to these sources cannot independently re-derive the Tier 3 inputs. They can
check internal consistency and re-run the analysis on the committed values, but
the transcription itself rests on the author's fidelity. This is a real
limitation of the audit trail and is disclosed rather than concealed.

## FRED — not tierable as a source

**FRED cannot be assigned a tier, and never will be.** It is an aggregator: the
redistribution terms of a FRED series are the terms of whoever *originally*
published it. Some FRED series are federal works and fall under Tier 1; others
are redistributed under licence from commercial providers and fall under Tier 3.
"Retrieved from FRED" therefore says nothing about what may be committed.

Two rules follow, both binding on Phase 3:

1. **Tier is determined by the underlying provider, per series, before
   retrieval.** Record the originating source in
   [`data/SOURCES.md`](data/SOURCES.md), not merely "FRED".
2. **Prefer the original source wherever one is available.** Spec v0.2 names
   primary feeds directly — EIA, BIS, OMB/CBO, BEA, BLS, AHA/OECD, USDA — and
   those should be fetched from the issuing agency rather than through FRED.
   FRED's convenience is not worth the provenance ambiguity in a repository
   whose entire value is provenance. Where the spec explicitly names a FRED
   mirror as acceptable (§3, the quarterly debt/GDP series for the companion),
   using it is fine; the originating agency still goes in the record.

## UNDETERMINED — resolve before Phase 3

None outstanding. IMF GFSR is classified Tier 3 above; FRED is handled by the
per-series rule above.

No series from an unclassified source may be committed until it has been
assigned a tier.

---

## Standing rules

1. Tier is decided **before** retrieval, not after. If a source's tier is
   unclear at fetch time, it is Tier 3 until proven otherwise.
2. Every committed series has a row in [`data/SOURCES.md`](data/SOURCES.md) and a
   tier recorded here.
3. If a source's terms change, the change is recorded here with a date. Prior
   commits are not rewritten to hide the earlier state.
