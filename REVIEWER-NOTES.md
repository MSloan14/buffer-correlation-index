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

## Correction notice (2026-07-28, same day)

An earlier draft of this document reported that the crisis-exclusion leakage was
**not distinguishable from zero**. That was wrong, on two independent counts,
and item 5 has been rewritten. Both errors are recorded here rather than
quietly amended, because a disclosure document that silently revises itself is
worth nothing.

1. **A code defect.** The no-contamination control accepted a `crisis_boost`
   argument that was never passed through to the data generator. Both arms of
   the control therefore produced *contaminated* data, and the reported "net
   leakage" was the difference between two independent draws of the same
   quantity — necessarily zero. The control was inert while appearing to work.
2. **A wrong calendar layout.** The layout had been inferred, not supplied. The
   author has since provided the actual one, and it reverses the conclusion.

Corrected, the leakage is **large, statistically unambiguous, and biases toward
CONFIRM** — the direction originally suspected. The earlier null result should
not be cited.

---

## Summary

| # | Limitation | Severity |
|---|---|---|
| 1 | Endpoint blocks hold 7 and 6 observations | Structural |
| 2 | Empirical MDE is delta rho ~= 0.52, far outside any plausible effect | **Severe** |
| 3 | The four-part conjunction adds almost nothing to C2 alone | Substantive |
| 4 | The test rejects 18.0% of the time when nothing is happening, against a 10% nominal | **Severe** |
| 5 | Crisis exclusion leaks one-sidedly into B3ex, biasing +0.053 toward CONFIRM | **Severe** |
| 6 | A noise domain shrinks the recovered effect ~25% | Substantive |
| 7 | The declined 1990-start extension cost ~30% of the standard error | Self-inflicted |
| 8 | The best-powered instrument is excluded from the verdict | Self-inflicted |

Items 4 and 5 are one problem seen twice: the leakage in item 5 is the largest
single contributor to the false-positive rate in item 4.

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
| 0.00 | 0.184 | 0.155 |
| 0.10 | 0.281 | 0.257 |
| 0.15 | 0.353 | 0.333 |
| 0.20 | 0.415 | 0.394 |
| 0.30 | 0.550 | 0.541 |
| 0.40 | 0.665 | 0.659 |
| 0.50 | **0.782** | **0.779** |

**80% power is not reached anywhere on the pre-specified grid.** At the top of
that grid, delta rho = 0.50, power is 0.782.

Extending the grid beyond the pre-specified range purely to locate the
threshold, the empirical MDE is:

- **delta rho ~= 0.515** for C1 and C2
- **delta rho ~= 0.517** for the full conjunction

**Do not read this as an improvement over the earlier draft's 0.59.** The entire
curve, including the row at delta rho = 0, sits higher than before because the
one-sided leakage in item 5 adds a positive bias to every estimate. A test that
rejects more often when nothing is happening will also cross any power threshold
sooner. Power bought with bias is not detection, and the correct summary is that
the design got *worse*, not better: the MDE fell only because the false-positive
rate nearly doubled.

Stated in the units that matter: with a baseline mean pairwise correlation of
0.20, detecting an effect at 80% power requires the mean pairwise correlation
across 28 domain pairs to rise to roughly **0.72**. That is not a plausible
effect size.

At effect sizes anyone would actually predict — say delta rho between 0.10 and
0.20 — **the design confirms 28% to 42% of the time.** But that figure cannot be
read as detection either, because it must be compared against the **18.4%** rate
at which the design confirms when there is *no effect at all*. At delta rho =
0.15 the design confirms 35.3% of the time against 18.4% under the null: a
likelihood ratio of about **1.9 for a confirmation**, and about **0.79 for a
non-confirmation**.

That second number is the one that matters. A non-confirmation from this design
shifts the odds against the hypothesis by a factor of roughly 0.8 — which is to
say, almost not at all. **The design is close to incapable of producing evidence
in either direction**, and a pre-commitment to it buys very little.

## 3. The conjunction costs almost nothing, which is itself the finding

The gap between P(C1 and C2) and P(CONFIRM) is **0.003 to 0.039**, and it
*shrinks* as the true effect grows: 0.029 at delta rho = 0, 0.021 at 0.20, and
0.003 at 0.50.

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
- At delta rho = 0 the extra criteria trim the false-positive rate only from
  0.184 to 0.155. They remove less than a fifth of the excess and leave the test
  badly anti-conservative. **The conjunction does not rescue the calibration**,
  and should not be cited as though it does.

## 4. Bootstrap calibration

At a true delta rho of zero, across 5,000 simulated datasets, the design as
specified excludes zero **18.0% of the time** against a nominal **10%** —
**nearly double the advertised rate**, with a Monte Carlo standard error of
0.005. Direction: **anti-conservative**.

Two distinct causes contribute, and they can be separated by re-running with the
crisis elevation switched off:

| Source | False-positive rate | Excess over nominal |
|---|---|---|
| Nominal | 0.100 | — |
| Small-sample bootstrap alone (no crisis elevation) | 0.1288 | +0.029 |
| Crisis-exclusion leakage, added on top | — | **+0.051** |
| **Design as specified** | **0.1796** | **+0.080** |

**The leakage is the larger cause.** It contributes more spurious rejections
than the bootstrap's small-sample failure does. This matters for triage: fixing
the exclusion rule is a bigger win than anything that could be done about the
bootstrap, and unlike block size it is a free choice rather than a constraint
imposed by the data.

The bootstrap component is the expected consequence of item 1 — with 3 to 4
resampled blocks per side, the moving-block bootstrap cannot represent the
sampling distribution well.

**This figure is optimistic.** The simulated differences are serially
independent, which is the most favourable case for a block bootstrap. The
moving-block scheme exists to accommodate serial dependence; if the real series
carry any, calibration will be worse than 13.2%, not better. The true
false-positive rate should be treated as **at least** 13%.

## 5. Crisis-exclusion leakage is one-sided and biases toward CONFIRM

The spec excludes crisis years by the **year label of the difference**, so a
difference reaching back into an excluded year survives. Under the authoritative
calendar layout, the consequence is asymmetric:

- `delta_2010 = z2010 - z2009` leaks from the 2008-09 crisis — but 2010 falls in
  **B2**, the middle third, which bears on nothing in the headline contrast.
- `delta_2022 = z2022 - z2021` leaks from the 2020-21 crisis — and 2022 **is in
  B3ex**.

So **B1ex contains zero contaminated differences and B3ex contains one.** Nothing
cancels. The contamination lands entirely on the late block, inflating
`rhobar(B3ex)`, and therefore inflating `delta_rho`.

| True delta rho | Raw spec-minus-clean | Sample-size artifact | **Net leakage** |
|---|---|---|---|
| 0.00 | +0.0595 | +0.0066 | **+0.0529** (se 0.0033) |
| 0.15 | +0.0604 | +0.0047 | **+0.0557** (se 0.0036) |

The net bias is roughly **sixteen standard errors from zero**. Its direction is
**toward CONFIRM**: the exclusion rule, as written, helps the thesis it is meant
to be testing.

The sample-size artifact is now small because B1ex and B1clean are the same 7
observations under this layout; only the B3 side differs (6 against 5). The
control is still necessary to establish that, but it no longer explains much.

**On magnitude:** +0.053 sits against an MDE of ~0.515, so the bias is about a
tenth of a detectable effect. That understates its importance. The bias applies
at *every* effect size including zero, which is why it contributes +0.051 of the
+0.080 excess false-positive rate in item 4. A design that manufactures a tenth
of its own detection threshold out of an exclusion rule is not neutral about the
answer.

**This is the one finding here with an obvious remedy.** Excluding a difference
when *either* endpoint year falls in the crisis set, rather than only its own
label, removes the contamination. It costs one observation in B3ex (6 down to
5), which is not free given item 1 — but a smaller unbiased block is worth more
than a larger block with a thesis-helping thumb on the scale. **That change is
not proposed here and has not been made**; the specification is frozen and this
document is disclosure, not revision.

## 6. Domain-8 dilution, and a mis-tagged domain

Replacing one of eight informative domains with a non-informative one (a
weather-driven proxy):

| True delta rho | 7 informative | 8 with noise | Shrinkage | Power |
|---|---|---|---|---|
| 0.10 | 0.1486 | 0.1085 | 27.0% | 0.265 -> 0.227 |
| 0.20 | 0.2403 | 0.1877 | 21.9% | 0.402 -> 0.393 |
| 0.30 | 0.3318 | 0.2535 | 23.6% | 0.555 -> 0.498 |

The measured shrinkage matches the arithmetic. A noise domain contributes 7 null
pairs to the 28, so the unweighted mean is multiplied by 21/28 = 0.75.
**Any true effect is attenuated by roughly 25%, and the power already reported
in item 2 is reduced by a further 1 to 6 points.**

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
error, so a 30% reduction would move the empirical MDE from **~0.52 to roughly
~0.36** — an approximation, not a simulated result. That remains a large effect
and would not on its own rescue the design. But it would materially improve the
bootstrap calibration in item 4 by supplying more blocks, and the candidate
comparison in [`results/design-comparison/`](results/design-comparison/)
quantifies what a longer sample actually buys.

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
an equicorrelation factor structure, and **no serial dependence**. All are
documented in
[`results/power-simulation/README.md`](results/power-simulation/README.md).

The calendar layout is **no longer** among these assumptions: it was supplied by
the author on 2026-07-28 and is authoritative. The leakage magnitude in item 5
does still scale with the assumed crisis elevation of +0.35 — a smaller
elevation would produce a proportionally smaller bias — but its *direction* and
one-sidedness follow from the layout and the exclusion rule alone, not from any
simulation assumption.

Two of these push the reported numbers in a known direction: the absence of
serial dependence flatters the bootstrap, and the main power curve assumes all
eight domains are informative when item 6 shows one likely is not. **The power
and calibration figures above are therefore optimistic on two independent
counts.**
