# Domain 6 (health capacity) — substitution options

**Decision required from the author. Nothing has been chosen here.**

**Status:** written with the data gate closed. No source was fetched and no
series was inspected. Every coverage and frequency claim below is from prior
knowledge and is marked accordingly; **all of it must be verified at gate-open
before any option is adopted.** Treat the specifics as a starting point for
checking, not as findings.

---

## The problem

Index Spec v0.2 §3.1 specifies **hospital beds per 1,000 population**, sourced
from AHA Hospital Statistics or OECD. Two independent difficulties:

1. **AHA is Tier 3.** Per [`../DATA_TERMS.md`](../DATA_TERMS.md), AHA Hospital
   Statistics may contribute transcribed numeric values with citation only —
   never tables, never the publication. A Tier 3 source cannot anchor a
   reproducible fetch pipeline; it can only be hand-entered, which makes the
   series unauditable by anyone without a licence.

2. **Beds measure the wrong thing.** Beds per 1,000 counts *physical plant*. The
   binding constraint in an actual capacity crisis is *staffed* capacity — a bed
   without a nurse absorbs nothing. In 2020–21 US hospitals repeatedly reported
   adequate physical beds and inadequate staff. A buffer index whose health
   component cannot see that is measuring the wrong reservoir.

The spec already discloses a third issue: the secular decline in beds per 1,000
partly reflects the deliberate shift to outpatient care — a technological and
organisational change, not extraction. That confound attaches to the
physical-plant measure specifically.

## Options

### Option A — OECD Health Statistics, hospital beds per 1,000 (US)

| | |
|---|---|
| Measures | Physical plant, all hospital types |
| Frequency | Annual |
| Coverage *(unverified)* | Long; believed to extend well before 2000 |
| Tier | Tier 1-equivalent; OECD terms to confirm at gate |
| Redistributable | Believed yes — **verify** |

Closest to the spec's letter while avoiding AHA's licence problem. Carries the
outpatient-shift confound in full. Reporting basis is harmonised across
countries, which can differ from domestic definitions.

### Option B — BLS Occupational Employment Statistics, registered nurses per capita

| | |
|---|---|
| Measures | Staffed capacity — the constraint that actually binds |
| Frequency | Annual |
| Coverage *(unverified)* | Believed to start in the late 1990s — **the likely disqualifier** |
| Tier | Tier 1 (federal work) |
| Redistributable | Yes |

Measures the right thing. Requires a population denominator (Census/FRED), so
it is derived rather than fetched, and the denominator choice must be recorded.

**Its own confound, stated before adoption:** nurse employment reflects *demand*
as well as capacity. A hospital system that hires as admissions rise will show a
rising series in exactly the periods a buffer measure should show strain. That is
arguably worse than the outpatient confound in Option A, because it can move the
series in the wrong direction rather than merely adding trend.

**Coverage is the binding question.** If the series begins around 1997–1999, it
cannot support the early era of a within-domain early-versus-late comparison,
and it may not span the index window either. Verify first; if it starts post-2000
it is unusable as a primary series regardless of construct fit.

### Option C — ship both (recommended for consideration, not decided)

Adopt Option A as the primary series for continuity with the frozen spec, and
carry Option B as a documented secondary where its coverage allows.

The brief anticipated this. It is attractive here because the two series have
**confounds pointing in opposite directions**: A drifts down for reasons
unrelated to buffer depletion (outpatient shift), while B drifts up for reasons
unrelated to buffer strength (demand-driven hiring). Where they agree, the
agreement is informative. Where they diverge, the divergence localises the
confound rather than hiding it.

The cost is honest and should be weighed: two series invite selecting the more
congenial one after seeing both. If Option C is chosen, the primary must be
named **now**, in writing, before either is fetched.

## What is NOT recommended

- **CMS** (Provider of Services, Hospital Cost Reports) — contains staffed-bed
  counts and is public, but requires substantial construction from provider-level
  files. Index Spec v0.2 §3.0 criterion K2 bars researcher re-derivation, and
  domain 2's precedent is explicit: published values only. Building a national
  series from provider files is exactly what that rule excludes.
- **NCHS Health, United States** — a compilation that often reproduces AHA
  figures. Using it to sidestep AHA's Tier 3 status would be laundering the
  restriction rather than respecting it. If the underlying numbers are AHA's,
  the tier follows the numbers.

## What the author needs to decide

1. **Which series is primary** — A, B, or C with a named primary.
2. **If C: the named primary**, fixed before fetching.
3. **Whether a coverage failure in B changes the answer** — i.e. if B starts
   after 2000, is C still wanted as a partial secondary, or does that collapse
   to A?

## Substitution rationale, to be recorded as a pre-data decision

Whatever is chosen, the following should be written into the record before any
fetch, per the spec's own handling of the health substitution:

- that the spec's named source (AHA) was set aside for **licence** reasons, not
  because its numbers were inconvenient;
- what the replacement actually measures, and how that differs from beds per
  1,000;
- which confound the replacement carries, and in which direction it pushes;
- that the choice was made **before** any of the candidate series was seen.
