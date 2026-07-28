# Reviewer notes

> **This file is NOT part of the pre-registration.**
> It is a disclosure document, written before data contact, recording known
> limitations of the frozen design. It proposes no change to the frozen
> criteria and none has been made. Where a limitation is severe, it is stated
> plainly rather than softened.

**Date:** 2026-07-28. **Status:** written before any data has been fetched,
opened, or inspected. Every number below comes from simulation on synthetic
data, produced by [`scripts/analysis/power_sim.py`](scripts/analysis/power_sim.py)
with seed `20260728`. Full outputs and reproduction instructions are in
[`results/power-simulation/`](results/power-simulation/).

---

## Summary

| # | Limitation | Severity |
|---|---|---|
| 1 | Endpoint blocks hold 7 and 6 observations | Structural |
| 2 | Empirical MDE is delta rho ~= 0.59, far outside any plausible effect | **Severe** |
| 3 | The four-part conjunction adds almost nothing to C2 alone | Substantive |
| 4 | Bootstrap bound is anti-conservative: 13.2% actual against 10% nominal | Substantive |
| 5 | Crisis-exclusion leakage is small and not distinguishable from zero | Minor — **and contrary to prior expectation** |
| 6 | A noise domain shrinks the recovered effect ~25% | Substantive |
| 7 | The declined 1990-start extension cost ~30% of the standard error | Self-inflicted |
| 8 | The best-powered instrument is excluded from the verdict | Self-inflicted |

---

## 1. Endpoint block sizes

The crisis-excluded blocks hold **7 observations (B1ex)** and **6 observations
(B3ex)**. Every headline quantity in this design is a contrast between two
correlation matrices estimated from fewer than eight annual differences each.

This is the root cause of items 2 and 4. It is not a flaw introduced by the
analysis; it is what the available annual history permits once crisis years are
removed. It is recorded here because a reader should encounter it before the
power figures rather than after.

Consequence for the bootstrap: with block length 2, B1ex admits **6 distinct
overlapping blocks and draws 4**; B3ex admits **5 and draws 3**. Roughly **4% of
B3ex resamples draw the same block three times**, producing a resample with only
two distinct rows and correlations of exactly +/-1.

## 2. Statistical power and the empirical MDE

**The design is severely underpowered.** Across 2,000 simulated datasets per
condition, with 5,000 bootstrap replications each:

| True delta rho | P(C1 and C2) | P(CONFIRM, all four) |
|---|---|---|
| 0.00 | 0.136 | 0.104 |
| 0.10 | 0.204 | 0.176 |
| 0.20 | 0.321 | 0.301 |
| 0.30 | 0.454 | 0.435 |
| 0.40 | 0.588 | 0.579 |
| 0.50 | **0.720** | **0.714** |

**80% power is not reached anywhere on the pre-specified grid.** At the top of
that grid, delta rho = 0.50, power is 0.720.

Extending the grid beyond the pre-specified range purely to locate the
threshold, the empirical MDE is:

- **delta rho ~= 0.593** for C1 and C2
- **delta rho ~= 0.595** for the full conjunction

Stated in the units that matter: with a baseline mean pairwise correlation of
0.20, detecting an effect at 80% power requires the mean pairwise correlation
across 28 domain pairs to rise to roughly **0.79**. That is not a plausible
effect size. It is close to the ceiling of the statistic.

At effect sizes anyone would actually predict — say delta rho between 0.10 and
0.20 — **the design has a 20% to 32% chance of confirming a real effect.** A
non-confirmation from this design is therefore close to uninformative: it is the
expected outcome whether or not the hypothesis is true.

## 3. The conjunction costs almost nothing, which is itself the finding

The gap between P(C1 and C2) and P(CONFIRM) is **0.006 to 0.032**, and it
*shrinks* as the true effect grows: 0.032 at delta rho = 0, 0.020 at 0.20, and
0.006 at 0.50.

The intended reading of a four-part conjunction is that it is demanding. It is
not. **C3 and C4 are very nearly implied by C1 and C2**: once the point estimate
is positive and the bootstrap bound clears zero, the drop-one reruns, the
Dirichlet reweightings, the crisis-included contrast, and the Mann-Kendall trend
almost always agree. They are correlated with the headline statistic by
construction, being recomputations of it on overlapping data.

Two honest consequences:

- The design's apparent stringency is largely decorative. Reporting "all four
  pre-registered criteria were met" conveys materially less independent
  corroboration than the phrase implies.
- One incidental effect is real: at delta rho = 0 the extra criteria trim the
  false-positive rate from 0.136 to 0.104, which happens to offset the
  bootstrap's anti-conservatism (item 4) and land near the nominal 10%. **This
  is a coincidence, not a design feature**, and it should not be cited as
  evidence the procedure is calibrated.

## 4. Bootstrap calibration

At a true delta rho of zero, across 5,000 simulated datasets, the one-sided 90%
bound excludes zero **13.2% of the time** against a nominal **10%**.

- Absolute miscalibration: **+3.2 percentage points**
- Relative inflation of the false-positive rate: **~32%**
- Monte Carlo standard error: ~0.005, so the discrepancy is real, not noise
- Direction: **anti-conservative** — the procedure rejects the null more often
  than advertised

This is the expected consequence of item 1. A moving-block bootstrap with 3 to 4
resampled blocks per side cannot represent the sampling distribution well.

**This figure is optimistic.** The simulated differences are serially
independent, which is the most favourable case for a block bootstrap. The
moving-block scheme exists to accommodate serial dependence; if the real series
carry any, calibration will be worse than 13.2%, not better. The true
false-positive rate should be treated as **at least** 13%.

## 5. Crisis-exclusion leakage — contrary to the prior expectation

The spec excludes crisis years by the **year label of the difference**, so a
difference reaching back into an excluded year survives: `delta_2010 = z2010 -
z2009` and `delta_2022 = z2022 - z2021` both remain in the analysed blocks
despite spanning an excluded year.

The expectation recorded before this simulation was that the leakage biases
**toward CONFIRM**, i.e. that it is thesis-helping. **The simulation does not
support that**, and the correct finding is reported here in preference to the
expectation.

| True delta rho | Raw spec-minus-clean | Sample-size artifact | **Net leakage** |
|---|---|---|---|
| 0.00 | +0.0110 | +0.0150 | **-0.0040** (se 0.0050) |
| 0.15 | +0.0175 | +0.0129 | **+0.0046** (se 0.0050) |

**Neither net figure is distinguishable from zero**; both are within one
standard error.

Why the naive comparison misleads: label-based exclusion leaves blocks of 7 and
6, while clean exclusion leaves 6 and 5. Pearson correlations attenuate toward
zero more severely at smaller *n*, and the two schemes have different *n*, so a
raw comparison confounds contamination with an arithmetic artifact. Re-running
with the crisis elevation switched off isolates that artifact — identical block
sizes, no contamination — and it accounts for essentially the whole raw
difference. **A reviewer told only the raw number would conclude the design has a
thesis-helping bias of +0.011 to +0.018 that it does not have.**

The mechanism behind the near-cancellation: under the calendar layout assumed
here, contamination enters **both** blocks — one leaked difference in B1ex and
one in B3ex — and largely cancels in the contrast. The small residual comes from
B3ex being the smaller block, so its single contaminated observation carries more
weight.

**This result is conditional on that layout and should not be generalised.** The
calendar layout is an assumption (see the results README); it was chosen to
reproduce the two stated block sizes and both stated leakage examples. **If the
real layout leaves leaked differences in only one block, they would not cancel,
and the bias could be substantial and thesis-helping as originally expected.**
Confirming the actual layout is a genuine open item, and the original concern is
not disposed of — only shown not to apply under the layout modelled.

## 6. Domain-8 dilution, and a mis-tagged domain

Replacing one of eight informative domains with a non-informative one (a
weather-driven proxy):

| True delta rho | 7 informative | 8 with noise | Shrinkage | Power |
|---|---|---|---|---|
| 0.10 | 0.0972 | 0.0693 | 28.7% | 0.227 -> 0.197 |
| 0.20 | 0.1894 | 0.1404 | 25.9% | 0.322 -> 0.290 |
| 0.30 | 0.2946 | 0.2222 | 24.6% | 0.432 -> 0.395 |

The measured shrinkage matches the arithmetic exactly. A noise domain
contributes 7 null pairs to the 28, so the unweighted mean is multiplied by
21/28 = 0.75. **Any true effect is attenuated by 25%, and the power already
reported in item 2 is reduced by a further 3 to 4 points.**

**On the "neutral-precision" tag.** The food domain was tagged
*neutral-precision* in the design. That tag is incorrect, and demonstrably so
**a priori** — this is arithmetic, not an empirical result requiring data. A
weather-dominated series cannot be neutral: it can only add null pairs, which
shrink the statistic toward zero. It is **null-helping in expectation**, meaning
it biases the design against confirming. The direction happens to be
conservative rather than self-serving, but the tag was wrong at the time it was
applied, and it was knowable then.

## 7. The declined 1990-start window extension

An extension of the window to a 1990 start was considered and declined. The
documented effect of that extension at the time was a **~30% reduction in the
standard error**. (That figure is carried from the design record; it was not
re-derived by this simulation.)

Given item 2, the cost is not marginal. The MDE scales roughly with the standard
error, so a 30% reduction would move the empirical MDE from **~0.59 to roughly
~0.41** — an approximation, not a simulated result. That remains a large effect
and would not rescue the design. But it would roughly halve the required effect
relative to the baseline correlation, and it would materially improve the
bootstrap calibration in item 4 by supplying more blocks.

Declining it made an already underpowered design meaningfully weaker, for
reasons that should be stated explicitly in the pre-registration.

## 8. The best-powered instrument does not bear on the verdict

The quarterly companion is, by observation count, the **best-powered instrument
in the design** — more observations, more bootstrap blocks, better calibration,
higher power. It is **deliberately non-verdict-bearing**.

The consequence, stated plainly: **the verdict rests on the weakest instrument
available while the strongest is held to one side.** There may be a defensible
reason — quarterly data may not measure the same construct, or may have been
judged more vulnerable to confounding. Whatever the reason, it should be written
down in the pre-registration, because a reader will otherwise reasonably ask why
the more informative test is not the deciding one. As it stands the arrangement
also has an unfortunate property: a confirmation can be reported from the
low-powered instrument while the high-powered one is exempt from contradicting
it.

---

## What this document does not do

It does not revise the pre-registration. Criteria C1 through C4, the block
definitions, the exclusion rule, the bootstrap scheme, and the domain set are
frozen as specified and are unchanged. Everything above is disclosure written
before data contact so that a reader can discount the eventual result
appropriately.

If the design is to be changed, that must happen as an explicit, dated,
disclosed amendment **before** data contact — not as a quiet edit, and not in
response to anything seen in the data.

## Caveats on the simulation itself

The findings depend on assumptions the frozen spec does not fix, chief among
them a baseline mean pairwise correlation of 0.20, a crisis elevation of +0.35,
an equicorrelation factor structure, **no serial dependence**, and the calendar
layout discussed in item 5. All are documented in
[`results/power-simulation/README.md`](results/power-simulation/README.md).

Two of these push the reported numbers in a known direction: the absence of
serial dependence flatters the bootstrap, and the main power curve assumes all
eight domains are informative when item 6 shows one likely is not. **The power
and calibration figures above are therefore optimistic on two independent
counts.**
