# Ratchet Pre-Specification v1.0 — DRAFT

> # IDENTIFICATION CHECK PASSED — one amendment required before freezing
>
> The synthetic check required by §8.2 has been run. **The criterion
> discriminates**: a late-onset ratchet is separated from a pure accelerating
> decline by **+78.0 points** (90.2% versus 12.2%), against a required +20. It
> is also specific — 99.6% "against H-R" in both mean-reversion worlds. The
> spec's constants (1.5σ, 90%, 7yr) sit in a good region of the parameter grid.
>
> **An earlier version of this banner said the opposite.** That was an error in
> the simulation, not the criterion: it tested only *constant-in-time* ratchets,
> which §6 deliberately scores "uninformative", and read the resulting ~0%
> detection as failure. Caught by independent verification. Full account in
> [`../results/ratchet-identification/README.md`](../results/ratchet-identification/README.md).
>
> **Three limitations survive, and one blocks freezing:**
>
> 1. **§1 and §6 describe different hypotheses.** §1 words H-R timelessly —
>    "each episode steps the buffer permanently lower" — while §6, §7 and §8.1
>    all test a **late-onset** pattern. The single amendment permitted by §9
>    should re-scope §1 to late-onset ratcheting. **Do not freeze until this is
>    resolved**; the record must be unambiguous about which hypothesis was tested.
> 2. **Blind below a 10% step.** "Against H-R" means "no ratchet ≥ 10%", not
>    refutation of shallower ratcheting. Must be stated in those words.
> 3. **The detector fires on episode-free trending series** (~11 pseudo-episodes
>    per series, all false alarms). Report episode counts as a diagnostic. A
>    violent smooth late collapse also fakes the signature 40–79% of the time —
>    a genuine identification boundary to disclose.

---

> **DRAFT. NOT FROZEN. NOT BINDING.**
> Every parameter below is fixed *in this draft* before any real series has been
> seen, but the draft awaits ratification. On ratification it is renamed
> `ratchet-spec-v1.0.md`, committed with a freeze sentence, and registered
> externally. Until then it binds nothing.
>
> **The synthetic identification check ([`../results/ratchet-identification/`](../results/ratchet-identification/))
> must be read before ratifying.** If that check shows the criterion cannot
> separate ratcheting from ordinary secular decline, this specification is not
> frozen and the ratchet question is not tested — the negative result is
> published instead. That outcome is a legitimate finding, not a failure to be
> worked around.

**Status:** written before any contact with real data. **Date drafted:**
2026-07-31.

**Why this document exists.** The correlated-drain index test has been withdrawn
as not identified (see [`../results/withdrawal-note.md`](../results/withdrawal-note.md)).
The ratchet question survives that withdrawal because it does not depend on
cross-domain covariance, and it is the one remaining confirmatory element — but
only if its criterion is frozen before data contact. A criterion chosen after
seeing recovery trajectories is not a test.

---

## 1. The claim under test

**H-R (ratchet):** following stress episodes, buffers systematically fail to
rebuild to pre-episode levels. Depletion ratchets — each episode steps the buffer
permanently lower.

**Null (mean reversion):** buffers recover after episodes, consistent with a
system that draws down under stress and rebuilds afterwards.

The unit of analysis is **the episode**, not the year and not the domain. The
question is what happens *after* a drawdown, not whether drawdowns happen.

## 2. Knowledge-state disclosure

Stated plainly, because the value of a pre-specification depends on what its
author already knew.

**Known at drafting time:** current endpoint levels of several series are public
and known to the author — the SPR sits at multi-decade lows; federal debt/GDP and
net-interest share are historically elevated; union density has declined
secularly. The project exists *because* those levels are known. Perfect blindness
is not available and is not claimed.

**Not examined:** episode-level recovery *trajectories* for any series. Whether a
given buffer rebuilt after 1980, or after 2008, or after 2020 — and how that
compares within a domain across eras — has not been looked at, for any domain,
at any point.

**Why the distinction carries the test.** The criterion below is blind to
trajectories, not to endpoints, and **the test statistic depends only on
trajectories.** Knowing that a buffer is low today says nothing about whether it
recovered from its previous drawdowns; a buffer can be at a record low having
rebuilt fully from every prior episode, or high having ratcheted down repeatedly
from a much higher base. That gap is what makes freezing this criterion
meaningful despite the disclosure above.

A hostile reader should still note the residual channel: a macro-literate author
has impressions of how 2008 and 2020 played out. The mitigations are that every
parameter below is mechanical, and that the early-vs-late comparison in §6 is the
primary result rather than the raw tally.

## 3. Domains and orientation

The eight domains carried from Index Spec v0.2 §3.1, with the same feeds. The
food domain and the health substitution question are handled at data-collection
time and documented there.

**Orientation is applied first, before any other computation.** Every series is
signed so that **higher = more buffer**. Series requiring inversion:

- federal debt held by the public as % of GDP → inverted
- federal net interest as % of revenues → inverted
- BIS credit-to-GDP gap → inverted
- corporate net-debt/EBITDA → inverted

Any series whose orientation is ambiguous at collection time is reported and not
scored until the ambiguity is resolved in writing.

## 4. Episode definition (mechanical)

An **episode** is a peak-to-trough drawdown in an oriented series where:

1. the decline from local peak to local trough is **≥ 1.5σ**, where σ is the
   standard deviation of that series' own year-over-year changes computed over
   its **full available history**; and
2. the trough occurs **within 3 years** of the peak.

**Merging:** episodes whose peak-to-trough windows overlap are merged into a
single episode, taking the earliest peak and the lowest trough.

**Cross-check, secondary and non-binding:** detected episodes should broadly
align with NBER recession dates plus named shocks (1973 and 1979 oil, 2008,
2020, 2026). **Misalignment is reported, not corrected.** The detector is not
tuned to match the calendar; where it disagrees, the disagreement is the finding.

## 5. Rebuild definition (mechanical)

An episode is scored **rebuilt** if the series recovers to **≥ 90% of the
pre-episode peak within 7 years of the trough**. Otherwise **not rebuilt**.

Percentage is computed on the oriented series in its native units, relative to
the peak level, not to the drawdown depth.

**Right-censoring:** episodes with fewer than 7 post-trough years of available
data are **censored — reported, not scored.** This necessarily includes anything
involving 2026 and, depending on retrieval date, 2020–21. Censored episodes
appear in the tally with their partial trajectory and are excluded from
inference. They are not scored as "not rebuilt"; an incomplete recovery is not
a failed one.

## 6. The secular-decline confound, and the primary comparison

A domain in long-run structural decline will show unrebuilt episodes throughout
its history for reasons that have nothing to do with ratcheting. Treating that as
support for H-R would repeat exactly the error that killed the index test:
mistaking a shared trend for the mechanism under study.

**The primary comparison is therefore within-domain, early episodes versus late
episodes.**

- A domain that **rebuilt after its 20th-century episodes but not its
  21st-century ones** shows the ratchet signature.
- A domain that **never rebuilds, in any era**, is consistent with secular
  decline and scores as **uninformative for H-R** — not as support.
- A domain that rebuilds throughout is evidence **against** H-R.

The era split is at **2000**, fixed now: episodes with troughs before 2000 are
early, from 2000 onward are late. Chosen to match the index window's start and to
predate every crisis in the frozen crisis set.

Domains with no early episodes cannot support the within-domain comparison and
are reported as such.

## 7. Tally and inference

**Per episode**, one of four scores: `rebuilt`, `not rebuilt`, `censored`,
`uninformative` (the §6 secular-decline case).

**Reporting:** the full episode table — domain, peak year, trough year, drawdown
in σ, recovery ratio at 7 years, score — plus per-domain and aggregate counts.
The table is published whatever it shows.

**Inference:** a **two-sided sign test on late-era episodes only**, testing
whether the rebuilt/not-rebuilt split departs from chance. Exact p reported.

**Explicitly labeled weak evidence.** Expected n is 20–40 episodes in total
across all domains, of which late-era scored episodes will be a fraction.
Episodes within a domain are not independent, and episodes across domains during
a shared macro shock are certainly not. The sign test does not model this and
will overstate its own confidence; the p-value is a summary, not a verdict.

**Explicitly prohibited:** no composite index, no regression, no cross-domain
correlation, covariance, or factor statistic, no aggregation of recovery rates
into a single number presented as an effect size. The index test was withdrawn
for reaching beyond what the data identifies; this specification does not
reintroduce the same reach in a new form.

## 8. Outcome commitments

Fixed now, before any data contact.

1. **If late-era episodes predominantly rebuild, H-R is wrong** and will be
   stated as wrong, in those words, in the results write-up and anywhere the
   ratchet claim has been made.
2. **If the synthetic identification check cannot separate World R from World S**
   (see the banner above), this specification is **not frozen**, H-R is **not
   tested**, and the negative methodological result is published instead.
3. **If the episode detector produces implausible results** — near-zero episodes,
   or episodes in nearly every year — that is reported as a detector failure.
   The threshold is not retuned to produce a workable count, because a threshold
   chosen to make the test run is a threshold chosen by the data.
4. **Censored episodes stay censored.** They are not promoted to "not rebuilt"
   to increase n, however tempting the direction.

## 9. Tunables, and the one permitted amendment

Three parameters are chosen without data: **1.5σ**, **90%**, **7 years**. Each is
defensible and none is uniquely correct. Sensitivity to all three is reported by
the synthetic check across a small grid.

**One amendment cycle is permitted**, before freezing and before any data
contact, in response to the synthetic check only. Any amendment is recorded in
this file with its rationale and its direction of effect. After freezing, no
amendment: a new versioned specification citing this one would be required.

---

**Version: v1.0-DRAFT · Drafted 2026-07-31 · NOT FROZEN**
On ratification: rename, add the freeze sentence, register externally.
