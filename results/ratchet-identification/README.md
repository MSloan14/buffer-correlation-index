# Ratchet criterion — synthetic identification check

**Verdict: the criterion discriminates, for the pattern it is actually defined to
detect.** Separation between a late-onset ratchet and a pure accelerating
decline is **+78.0 points**, against a required threshold of +20.

Three genuine limitations survive and must be disclosed with any result. One
requires an amendment to the specification before freezing.

Run before any contact with real data. Everything here is synthetic.
Produced by [`../../scripts/analysis/ratchet_identification.py`](../../scripts/analysis/ratchet_identification.py),
seed `2026073101`, 2,000 series per world, 400 per sensitivity cell.

---

## Correction notice

**An earlier version of this document reported the opposite conclusion** — that
the criterion could not discriminate, with a separation of −6.5 points, and
recommended that Study 2 not proceed. That conclusion was wrong, and the error
was in the simulation, not the criterion.

The earlier run simulated ratchets in which **every episode from 1955 onward
stepped the buffer permanently down** — a *constant-in-time* ratchet. But §6's
signature is defined as **rebuilt early, not rebuilt late**. A constant ratchet
produces (0, 0) rebuild rates, which §6 deliberately scores "uninformative" in
order to dodge the secular-decline confound. **The earlier run therefore tested
the criterion exclusively against the one ratchet family it is designed to
exclude, and reported the resulting ~0% detection as a failure of the criterion.**

Taking the maximum over that family and calling it "the most generous reading
available" compounded the error: it presented a structurally impossible result
as a best case.

Found by independent verification. The corrected run adds the **late-onset**
family — episodes recovering fully before the era split and stepping down after —
which is the pattern §6, §7 (late-era-only sign test), and §8.1 all
operationally target. The numbers below are from that corrected run.

## Headline

| | |
|---|---|
| Best late-onset ratchet (R-late-20) | **90.2%** ratchet signature |
| Pure accelerating decline (S-acc) | **12.2%** |
| **Separation** | **+78.0 points** |
| Required for discrimination | +20 points |
| **Criterion discriminates?** | **Yes** |

## Full results

| World | What it is | Ratchet sig. | Uninformative | Against H-R | Mixed |
|---|---|---|---|---|---|
| **R-late-20** | ratchet switching on at the era split, 20% step | **90.2%** | 0.0% | 0.7% | 9.2% |
| **R-late-15** | same, 15% step | **78.3%** | 0.0% | 7.6% | 14.1% |
| **R-late-10** | same, 10% step — exactly on the rebuild bar | 10.4% | 0.0% | 69.8% | 19.7% |
| R-const-05 | constant ratchet, 5% step | 0.7% | 0.0% | **97.0%** | 2.3% |
| R-const-10 | constant ratchet, 10% step | 9.7% | 0.0% | 67.3% | 22.6% |
| R-const-15 | constant ratchet, 15% step | 3.4% | 6.1% | 35.1% | 54.5% |
| R-const-20 | constant ratchet, 20% step | 0.5% | 12.9% | 20.4% | 64.5% |
| M-flat | full recovery, flat baseline | 0.1% | 0.0% | **99.6%** | 0.3% |
| M-decl | full recovery, declining baseline | 0.0% | 0.0% | **99.6%** | 0.4% |
| S-lin | pure linear decline, no episodes | 0.1% | 0.0% | 99.5% | 0.2% |
| S-acc | pure accelerating decline, no episodes | 12.2% | 0.0% | 48.6% | 38.9% |

The criterion is **specific**: it correctly returns "against H-R" 99.6% of the
time in both mean-reversion worlds, and 99.5% under linear decline. If buffers
genuinely rebuild, this criterion says so.

It is **sensitive** to late-onset ratchets at or above 15% (78–90%), and drops
sharply at 10% — which sits exactly on the rebuild bar and is discussed below.

## Sensitivity

Across the 27-cell grid (σ ∈ {1.0, 1.5, 2.0} × rebuild ∈ {80%, 90%, 95%} ×
window ∈ {5, 7, 10} years), measured on R-late-15:

| | |
|---|---|
| Cells with separation ≥ +20 points | **13 of 27** |
| Cells inverted (S-acc ≥ R) | 6 of 27 |
| Separation range | **−15.5 to +76.8** |
| Worst cell (σ=1.0, 95%, 5yr) | R 50.5% vs S-acc **66.0%** |

**The spec's chosen constants (1.5σ, 90%, 7yr) sit in the good region.** But the
grid is not uniformly safe, and two failure regions are real:

- **σ = 1.0 with a 95% rebuild bar** genuinely destroys separation. A loose
  drawdown threshold on a steepening trend generates many pseudo-episodes, and a
  strict rebuild bar ensures the late ones fail. That combination should be
  avoided and the avoidance recorded.
- **σ = 1.0 with an 80% bar and a 5-year window** detects almost nothing in
  either world (0.8% vs 7.0%) — separation is negative but both arms are near
  the floor, so it is uninformative rather than misleading.

## Three limitations that survive

### 1. The criterion is blind to ratchets shallower than the rebuild bar

A genuine 5% permanent step is reported as evidence **against** H-R **97.0%** of
the time. This is structural, not tuning: any step smaller than
`1 − REBUILD_FRACTION` = 10% leaves the series above the bar and scores
"rebuilt" everywhere.

**Consequence for reporting.** An "against H-R" verdict from this criterion means
*"no ratchet of 10% or more"* — it does **not** refute shallower ratcheting. Any
write-up must say so in those words, because the natural reading of "against"
is stronger than what the test supports.

### 2. A *consistent* ratchet is scored uninformative — a spec inconsistency

A constant-in-time ratchet yields (0, 0) rebuild rates, which is definitionally
identical to secular decline, and §6 assigns that "uninformative" (12.9% at the
deepest, with 64.5% landing in "mixed").

This is a real logical property of §6, provable from the rule text rather than
from simulation. **But it is a scope inconsistency in the specification, not a
demonstration that the question is untestable.** §1 words H-R timelessly — *"each
episode steps the buffer permanently lower"* — while §6, §7 and §8.1 all
operationally test a **late-onset** pattern. Those are different hypotheses, and
the document currently claims one and tests the other.

**This is what the single amendment permitted by §9 should be spent on**:
re-scope H-R to late-onset ratcheting, consistent with the machinery already
written. The alternative — testing timeless ratcheting — would require
abandoning §6's confound control, which is the only thing standing between this
study and the error that killed the index test.

### 3. The episode detector fires on trending series with no episodes

S worlds show **~11 detected episodes per series** against ~6 in the R and M
worlds — and in S worlds *every one is a false alarm*, since nothing was
injected. The S-acc false signatures ride entirely on these trend-plus-noise
pseudo-episodes.

§8.3 of the draft commits to reporting implausible detector output as a detector
failure. One "episode" per seven years on an episode-free series meets that bar.
**Episode counts should be reported as a diagnostic alongside any result**, and a
trend-aware drawdown screen is worth considering before freezing.

A further disclosable limit, found by verification: a *violent smooth late
collapse* — no episodes, just a steep late fall — fakes the signature 40–79% of
the time. The criterion cannot distinguish "episodic permanent loss after 2000"
from "smooth collapse after 2000". That is a genuine identification boundary and
belongs in the disclosure.

## What this licenses

**Freezing the criterion is defensible**, provided:

1. the §9 amendment re-scopes H-R to late-onset ratcheting (limitation 2);
2. the write-up states that "against H-R" means "no ratchet ≥ 10%"
   (limitation 1);
3. episode counts are reported as a detector diagnostic, and the σ=1.0/95% cell
   is documented as avoided (limitation 3);
4. the smooth-late-collapse boundary is disclosed.

**It does not license** running Study 2 on the current text unamended, because
§1 and §6 describe different hypotheses and the record should not be ambiguous
about which was tested.

## Files

| File | Contents |
|---|---|
| `summary.json` | Seed, environment, criterion constants, all worlds, full grid, headline. |
| `worlds.csv` | Per-world detection and verdict distribution. |
| `sensitivity_grid.csv` | All 27 parameter cells, measured on R-late-15. |

## Simulation assumptions

Annual series 1950–2026 (77 observations), base level 100, noise SD 2.0, episodes
roughly once per decade with drawdowns of 14–20% of the pre-episode level over
1–2 years and recovery over 3–5 years.

Ratchet severity is parameterised as the permanent step-down after each episode,
as a fraction of the pre-episode level, because that is the quantity the rebuild
criterion keys on. **Two families are simulated** — `R-const-*`, where every
episode steps down, and `R-late-*`, where the step applies only from the era
split onward. The distinction is the subject of the correction notice above.

S-lin declines 0.45 units/year; S-acc as 0.010·t², reaching a similar endpoint by
a curved path. S-acc was added beyond the original brief because curvature in a
shared trend is what defeated the index test.
