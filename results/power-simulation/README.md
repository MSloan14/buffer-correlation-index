# Power simulation

What the frozen design can and cannot detect, estimated **before data contact**
using synthetic data only. No real series was read, fetched, or opened to
produce anything in this directory.

Headline numbers are summarised in [`../../REVIEWER-NOTES.md`](../../REVIEWER-NOTES.md).
This file explains how to reproduce them.

## Reproduce

```
python scripts/analysis/power_sim.py
```

From the repository root. Runtime is on the order of tens of minutes on a
desktop CPU; add `--quick` for a fast smoke test that exercises every code path
with far too few replications to interpret.

Requirements: Python 3, `numpy`, and optionally `matplotlib` for the PNGs. If
matplotlib is absent the script skips plotting and reports `plots written:
False` rather than failing.

**Seed: `20260728`**, set at the top of the script. Independent streams for the
four experiments are derived with `numpy.random.SeedSequence(SEED).spawn(4)`, so
each experiment is reproducible on its own and adding one does not perturb the
others. Re-running with the same seed on the same numpy version reproduces every
number exactly. The exact versions used are recorded in `summary.json`.

## Files

| File | Contents |
|---|---|
| `summary.json` | Everything, machine-readable. Seed, environment, design constants, all curves, all headline figures. |
| `power_curve.csv` | Per true delta rho: pass rate of each criterion, power for C1&C2, power for the full conjunction, mean estimate and its spread. |
| `power_curve_extended.csv` | Same, on effect sizes **beyond** the pre-specified grid. Written only when 80% power is not reached within it — which is what happened. Present so the MDE can be located rather than reported as "not reached". |
| `crisis_leakage.csv` | Label-based exclusion versus clean exclusion, paired on identical data. |
| `domain_dilution.csv` | Seven informative domains versus eight where the eighth is noise. |
| `power_curve.png` | Both power curves against the 0.80 target. |
| `criteria_components.png` | Pass rate of C1, C2, C3, C4 separately — shows which criterion is binding. |
| `bootstrap_coverage.png` | Nominal versus empirical false-positive rate. |
| `crisis_leakage.png` | Signed bias from the exclusion rule. |
| `domain_dilution.png` | Recovered effect with and without the noise domain. |

## What is simulated

The design is taken as frozen and is **not** modified anywhere in this script:
8 domains, annual, first differences of z-scored series; test statistic the
unweighted mean of 28 pairwise Pearson correlations; B1ex of 7 observations and
B3ex of 6; headline contrast `delta_rho = rhobar(B3ex) - rhobar(B1ex)`;
inference by moving-block bootstrap with block length 2 and 5,000 replications
at a one-sided 90 percent bound.

### Calendar layout

The spec fixes the block sizes and gives two worked leakage examples
(`delta_2010 = z2010 - z2009`, `delta_2022 = z2022 - z2021`). It does not state
the calendar layout outright. The layout used here is the one consistent with
all of that, and it is an assumption:

- differences span 2004–2023
- B1 window gives differences 2004–2012; B3 window gives 2016–2023
- crisis years 2008, 2009, 2020, 2021
- excluding by year **label**: B1ex = 2004–2007, 2010–2012 (**7**);
  B3ex = 2016–2019, 2022–2023 (**6**)
- the differences that leak are exactly `delta_2010` and `delta_2022`, matching
  the two stated examples

### Assumptions that are not in the spec

Every number here is conditional on these. They are simulation choices, made to
have something concrete to simulate, and a reader should treat them as the main
soft spot in the exercise:

| Assumption | Value | Why it matters |
|---|---|---|
| Baseline mean pairwise correlation in the B1 era | 0.20 | Sets the scale the contrast is measured against. |
| Crisis-year correlation elevation | +0.35 | Drives the size of the leakage bias. |
| Correlation path through the untested middle years | linear | Makes the C4 Mann–Kendall leg meaningful rather than a step. |
| Cross-domain structure | single common factor (equicorrelation) | Real domains would have block structure; equicorrelation is the tractable idealisation. |
| Serial dependence within a block | **none** | See the warning below. |
| Rolling window for the C4 trend series | 7 years | Not specified by the design. |
| Bootstrap interval type | percentile | The spec fixes the scheme, replication count, and level, but not which interval to construct. |

The leakage experiment carries a control that matters for reading it. Label
exclusion leaves blocks of 7 and 6; clean exclusion leaves 6 and 5. Because
Pearson correlations attenuate more at smaller *n*, comparing the two directly
confounds contamination with a sample-size artifact. Each condition is therefore
re-run with the crisis elevation switched off, isolating the artifact, and net
leakage is reported as the difference. The raw and controlled figures differ
enough to reverse the conclusion; see item 5 of the reviewer notes.

**The serial-dependence point is important and cuts against the design.** The
simulated differences are independent across years, which is the most
favourable case for a block bootstrap. The moving-block bootstrap exists
precisely to handle serial dependence; if the real series have any, the
calibration reported here is an **upper bound on how well the procedure
behaves**, not an estimate of it. Real calibration would be worse.

Similarly, the main power curve uses 8 genuinely informative domains. Experiment
D shows what happens when one is not. The headline power figures are therefore
optimistic on two independent counts.

## Interpretation guidance

Monte Carlo error on a power estimate from 2,000 datasets is about ±0.011 at
worst (at power 0.5), so differences smaller than roughly 0.03 between grid
points are noise. The coverage experiment uses 5,000 datasets, giving a standard
error near 0.004 on the false-positive rate.

The power curve is not guaranteed to be perfectly monotonic in the simulation
output even though the true power is; small non-monotonicities between adjacent
grid points are Monte Carlo error, not a finding.
