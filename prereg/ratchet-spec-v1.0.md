# Ratchet Pre-Specification v1.0 — DRAFT

# Ratchet Pre-Specification v1.0 (FROZEN)

> **FROZEN 2026-08-01, before any contact with real data.**
> No edits after external timestamp; amendments require a new versioned
> specification citing this one. The single revision permitted by §9 has been
> spent on Amendment 1 in §1 and is recorded there.

**Status:** frozen. **Drafted** 2026-07-31, **amended and frozen** 2026-08-01.
No real series has been fetched, opened, or inspected at any point.

## Validation record (§8.2 satisfied)

The synthetic identification check required before freezing has been run.
Full results: [`../results/ratchet-identification/`](../results/ratchet-identification/),
seed `2026073101`, 2,000 series per world.

**The criterion discriminates.** A late-onset ratchet is separated from a pure
accelerating decline by **+78.0 points** (90.2% versus 12.2%), against the +20
required. It is specific: **99.6%** "against H-R" in both mean-reversion worlds
and 99.5% under linear decline. The constants below (1.5σ, 90%, 7 years) sit in
a good region of the parameter grid; 13 of 27 cells clear +20.

An earlier run of this check reported the opposite and recommended abandoning
the study. That was an error in the simulation, not the criterion: it tested
only constant-in-time ratchets, which §6 deliberately scores uninformative, and
read the resulting near-zero detection as failure. It was caught by independent
verification and is documented in the results README rather than removed.

## Known limitations, binding on any result from this specification

These are part of the frozen record. Any write-up reporting a result under this
specification must carry them.

1. **Blind below a 10% permanent step.** A genuine ratchet shallower than
   `1 − REBUILD_FRACTION` leaves the series above the rebuild bar and scores
   "rebuilt" everywhere; in simulation a 5% ratchet was read as evidence
   *against* H-R **97.0%** of the time. **An "against H-R" verdict from this
   specification means "no ratchet of 10% or more". It does not refute
   shallower ratcheting**, and must not be reported as though it does.
2. **Consistent ratchets are invisible.** Per Amendment 1, a domain that has
   ratcheted in every era scores uninformative, by design.
3. **The episode detector fires on episode-free trending series** — roughly 11
   pseudo-episodes per series against 6 in episode-bearing worlds, all false
   alarms. Per §8.3, **episode counts are reported as a diagnostic with every
   result**, and an implausible count is reported as detector failure rather
   than analysed.
4. **A violent smooth late collapse fakes the signature** 40–79% of the time.
   The criterion cannot distinguish "episodic permanent loss after the era
   split" from "smooth collapse after the era split". This is an identification
   boundary and is disclosed with any positive result.
5. **Avoid σ = 1.0 with a 95% rebuild bar.** That cell destroys separation
   (R 50.5% versus S-acc 66.0%). It is not the frozen setting and is recorded
   so the avoidance is deliberate rather than lucky.

**Why this document exists.** The correlated-drain index test has been withdrawn
as not identified (see [`../results/withdrawal-note.md`](../results/withdrawal-note.md)).
The ratchet question survives that withdrawal because it does not depend on
cross-domain covariance, and it is the one remaining confirmatory element — but
only if its criterion is frozen before data contact. A criterion chosen after
seeing recovery trajectories is not a test.

---

## 1. The claim under test

**H-R (late-onset ratchet):** buffers that formerly rebuilt after stress
episodes have stopped doing so. Within a domain, episodes before the era split
recover to pre-episode levels and episodes after it do not — the system's
capacity to rebuild has degraded, and depletion now ratchets where it
previously did not.

**Null (mean reversion):** buffers recover after episodes in both eras,
consistent with a system that draws down under stress and rebuilds afterwards.

The unit of analysis is **the episode**, not the year and not the domain. The
question is what happens *after* a drawdown, not whether drawdowns happen.

> **Amendment 1, 2026-08-01 — the single revision permitted by §9.**
>
> **Before:** *"following stress episodes, buffers systematically fail to
> rebuild to pre-episode levels. Depletion ratchets — each episode steps the
> buffer permanently lower."*
>
> **Why.** That wording is timeless: it claims every episode ratchets, in every
> era. §6, §7 and §8.1 do not test it. They test a *change* in rebuild
> behaviour — early-rebuilt versus late-not — and a consistently ratcheting
> domain yields (0, 0) rebuild rates, which §6 deliberately scores
> **uninformative** to avoid confusing ratcheting with secular decline. The
> document therefore claimed one hypothesis and tested another. The synthetic
> check surfaced this: a constant-in-time ratchet was scored uninformative or
> mixed in 77% of runs at the deepest severity simulated.
>
> **Direction of effect: null-helping.** This narrows the claim. Timeless
> ratcheting is the broader hypothesis; late-onset ratcheting is a strict
> subset, and a domain that has ratcheted consistently since 1950 now scores
> uninformative rather than supporting H-R. The amendment makes the claim
> harder to support, not easier.
>
> **The alternative was worse.** Re-scoping §6 to detect timeless ratcheting
> would mean abandoning the early-versus-late comparison, which is the only
> control standing between this study and the confound that killed the index
> test. Given a choice between a narrower claim and a weaker control, the
> narrower claim is correct.
>
> **What is given up, stated plainly.** A domain that has been ratcheting
> steadily for seventy years is invisible to this test. That is a real
> limitation of what H-R can now claim, not a technicality, and it must be
> carried into any write-up.

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
2. **If the synthetic identification check cannot separate World R from World S**,
   this specification is **not frozen**, H-R is **not tested**, and the negative
   methodological result is published instead. **SATISFIED before freezing** —
   see the validation record above: separation +78.0 points against a +20
   requirement. This commitment was live, not decorative: an earlier run of the
   check returned a negative verdict and the study was, for several hours, going
   to be abandoned under this clause.
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

**SPENT.** Amendment 1 (§1, 2026-08-01) re-scoped H-R from timeless to
late-onset ratcheting, in response to the synthetic check, before any data
contact. Rationale and direction of effect (null-helping) are recorded with it.
**No further amendment is available under this specification.** The constants
1.5σ, 90% and 7 years are unchanged from the draft and were not retuned; the
grid showing where they fail is published rather than used to select them.

---

**Version: v1.0 · FROZEN 2026-08-01 · Drafted 2026-07-31**
No edits after external timestamp; amendments require a new versioned
specification citing this one.
