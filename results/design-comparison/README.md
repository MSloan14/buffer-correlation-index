# Candidate design comparison

**Exploratory. Pre-data-contact. Changes nothing in the frozen specification.**

This exists to inform a human decision about whether the buffer-correlation
question is testable at adequate power with available series. Every number is
from synthetic data; no real series was fetched, opened, or examined.

Produced by [`../../scripts/analysis/design_comparison.py`](../../scripts/analysis/design_comparison.py),
seed `2026072802`, 2,000 simulated datasets per condition, 5,000 bootstrap
replications for endpoint candidates and 1,000 for trend candidates.
Reproduce with `python scripts/analysis/design_comparison.py` from the repo root;
`--selftest` checks the optimized rolling-correlation routine against a naive
construction.

---

## The answer, up front

**No candidate reaches 80% power at delta rho = 0.15.** The terminating
condition is not met by any design examined. The best is C-C at 0.556, and it
gets there by answering a narrower question.

## Comparison table

Every candidate uses the same decision rule — a **one-sided level-0.10 test** in
the hypothesized direction — so false-positive rates and likelihood ratios are
directly comparable.

| | Design | P@0.10 | **P@0.15** | P@0.20 | MDE80 | **FPR at zero** | LR+ | **LR-** |
|---|---|---|---|---|---|---|---|---|
| **C-A** | frozen annual, 8 domains, endpoint blocks | 0.295 | **0.326** | 0.396 | 0.530 | **0.186** | 1.75 | **0.83** |
| **C-B** | quarterly, 4 domains, 2001-2026 | 0.317 | **0.471** | 0.570 | 0.295 | 0.156 | 3.02 | 0.63 |
| **C-C** | quarterly, 4 domains, 1990-2026 | 0.377 | **0.556** | 0.684 | 0.252 | 0.127 | **4.38** | **0.51** |
| **C-D** | annual, 8 domains, rolling-window trend | 0.208 | **0.238** | 0.303 | 0.589 | **0.099** | 2.42 | 0.85 |
| **C-E** | quarterly, 4 domains, rolling-window trend | 0.269 | **0.379** | 0.477 | 0.338 | 0.108 | 3.51 | 0.70 |
| **C-F** | co-depletion count trend | 0.125 | **0.115** | 0.104 | none | 0.111 | **1.04** | **1.00** |

Nominal false-positive rate is 0.10 throughout. Monte Carlo standard error is
about 0.011 at mid-range power and 0.007 near the null.

`LR+` = P(confirm | delta rho = 0.15) / P(confirm | 0).
`LR-` = P(not confirm | 0.15) / P(not confirm | 0).

## What the columns mean, and which one to read

**Read the LR- column.** Power alone is misleading when candidates differ in
false-positive rate, and here they differ by nearly a factor of two. A design
that rejects 18.6% of the time under the null is not "36% powered" in any useful
sense — much of that 36% is the same reflex firing.

- **LR+** is how much a confirmation should move your belief.
- **LR-** is how much a *non-confirmation* should move it. Values near 1.0 mean
  the result carries no information.

The frozen design (C-A) has **LR- = 0.83**: a disconfirmation shifts the odds
against the hypothesis by about a sixth. C-D is worse at 0.85. Both sit at or
past the threshold the design brief identified as not worth pre-committing to.

## Calibration is the sharpest separator

| Candidate | FPR at true zero |
|---|---|
| C-D (annual trend) | **0.099** |
| C-E (quarterly trend) | 0.108 |
| C-F (count trend) | 0.111 |
| C-C (quarterly endpoint, 1990) | 0.127 |
| C-B (quarterly endpoint, 2001) | 0.156 |
| C-A (frozen) | **0.186** |

The three **trend** statistics are essentially exactly calibrated. The three
**endpoint-contrast** statistics are all anti-conservative, and the frozen design
worst of all.

This is not a coincidence of construction. The endpoint contrast inherits both
problems documented in the reviewer notes: a moving-block bootstrap with 3-4
blocks per side, and one-sided crisis leakage into B3ex. The trend statistics
use every window, so they have far more blocks, and their bootstrap-null
construction is valid by design. **C-A's excess false-positive rate is roughly
double C-D's, on the same data, from the same 8 domains.**

## Candidate by candidate, in plain language

**C-A — the frozen design.** *What it can answer:* did mean cross-domain
correlation differ between 2001-2007 and 2018-2025? *What it gives up:* almost
everything. With 7 and 6 observations it needs an effect of 0.53 to detect
reliably, and it fires 18.6% of the time when nothing is happening. A
non-confirmation from C-A is close to meaningless.

**C-B — quarterly, four domains, 2001-2026.** *Can answer:* did quarterly
co-movement among strategic reserve, financial, fiscal and household buffers
rise? *Gives up:* **half the domains, and with them the actual claim.**
[NARROWING] Its power comes from 28 and 24 quarterly observations instead of 7
and 6 — but also from dropping to four buffers that are mostly financial.

**C-C — quarterly, four domains, from 1990.** *Can answer:* the same narrower
question over a longer history. *Gives up:* the same four domains, plus it
assumes the pre-2000 period is comparable. [NARROWING] Best numbers in the table
— LR- of 0.51 means a disconfirmation halves the odds. **But it is the same
narrowing as C-B with more of it.**

**C-D — annual, eight domains, trend across all windows.** *Can answer:* is
cross-domain correlation *trending* across 2001-2026, using all eight domains?
*Gives up:* the specific before-and-after framing, in exchange for using every
window instead of two endpoints. **This is the only candidate that both keeps all
eight domains and is properly calibrated.** It is not a narrowing — it measures
the same construct better. Its problem is simply power: 0.238 at delta rho =
0.15.

**C-E — quarterly, four domains, trend.** *Can answer:* is quarterly co-movement
among the four financial-ish buffers trending? *Gives up:* four domains.
[NARROWING] Intended as the power ceiling, and it does not reach 80% at 0.15
either (0.379). **The ceiling is lower than hoped.**

**C-F — co-depletion count.** *Can answer:* is the number of buffers
simultaneously falling in a given year rising over time? *Gives up:* the
co-movement question entirely. **C-F is blind to correlation**: its power is flat
at ~0.11 across every effect size from 0 to 0.80, and LR+ = 1.04, LR- = 1.00. It
carries essentially zero information about the co-movement hypothesis. See the
dedicated section below — it is not useless, it just answers a different
question.

## The two diagnostics, and why they matter more than the table

### D1 — a constant common drift contributes nothing

Simulating identical steady depletion in every domain, with independent noise
and no crisis elevation:

| Condition | mean delta rho | confirm rate |
|---|---|---|
| No drift | -0.0025 | 0.137 |
| Constant common drift (-1.0 sd per year, every domain) | **+0.0001** | 0.118 |

**A constant common drift moves the test statistic by essentially nothing.** This
is not a quirk of the simulation; it is arithmetic. Pearson correlation centres
each series within the window, and a constant added to every observation of
every domain is removed by that centring.

**Stated plainly: if every buffer in the system is steadily draining, year after
year, at a constant rate, this design detects nothing at all.** It does not
measure depletion. It measures *changes in the co-movement of the deviations
around* depletion. Those are different claims, and the second is considerably
narrower than the thesis as usually stated.

The same run shows the complement. Under that constant drift, C-F's count of
falling domains sits at **6.72 out of 8** — the system is visibly draining — and
C-F's trend test still confirms only 11.3% of the time, indistinguishable from
its 11.8% baseline. **A high count restates known depletion. Only a rising trend
in the count is new information**, and C-F correctly reports no trend when there
is none.

### D2 — synchronized drift is detected, but less efficiently

Simulating a regime where the drift itself becomes synchronized in the late
block — persistent common shocks to the depletion rate, noise still independent:

| Induced delta rho | Power, synchronized drift | Power, plain equicorrelation |
|---|---|---|
| 0.10 | 0.228 | 0.295 |
| 0.15 | **0.248** | 0.326 |
| 0.20 | 0.292 | 0.396 |
| 0.30 | 0.377 | 0.537 |

**Yes, the frozen statistic detects synchronized drift** — but at roughly 25-30%
lower power than an equivalent rise in contemporaneous correlation. The
persistence of the common component is serial dependence, which widens the block
bootstrap and makes short blocks noisier. So the mechanism most naturally
described as "shared shocks to how fast buffers drain" is detected *worse* than
the abstract correlation rise the design was powered against.

## C-F: what it can and cannot distinguish

C-F responds only to its own effect axis — a rising proportion of domains
recording negative changes:

| Drift ramp | Mean count of 8 falling | Power |
|---|---|---|
| 0.00 | 3.99 | 0.115 |
| 0.20 | 4.28 | 0.204 |
| 0.30 | 4.45 | 0.255 |
| 0.45 | 4.67 | 0.391 |
| 0.60 | 4.86 | 0.509 |

Even a drift carrying the expected count from 4.0 to 4.86 out of 8 is detected
only about half the time. C-F is not well powered either.

**What it cannot distinguish.** A high count is not evidence of anything new — a
descriptive layer that already establishes buffers are depleting predicts a high
count trivially. Only the *trend* in the count is additional information, and D1
confirms C-F correctly reports no trend under constant depletion. A red team will
press exactly here, and the honest answer is that C-F's level is redundant with
the descriptive layer while its trend is a genuine, if weakly powered, test.

## Where the decision rule does not resolve

The pre-committed decision table keys its rows on C-D, with a fallback row for
"nothing >= 55%". The observed results fall between rows:

- C-D is **0.238**, far below the 55% band.
- The row requiring C-B/C-C/C-E >= 80% is **not met** (0.471, 0.556, 0.379).
- The final row requires "nothing >= 55%", but **C-C is 0.556** — above 55% by
  0.006, against a Monte Carlo standard error of **0.011**.

**C-C's position relative to the 55% threshold is not statistically resolvable at
this sample size.** It is half a standard error above the line. Treating it as
"above 55%" or "below" is a coin flip on Monte Carlo noise, not a finding. This
should be decided on the substantive ground — whether the four-domain narrowing
is acceptable — rather than by the threshold.

## What this supports

Stated as plainly as the evidence allows:

1. **The eight-domain cross-domain claim is not testable at adequate power with
   available annual series.** C-A and C-D are the only candidates that preserve
   it, and they return 0.326 and 0.238 at delta rho = 0.15, with LR- of 0.83 and
   0.85. Neither can produce an informative disconfirmation.

2. **The candidates that reach usable power do so by narrowing the question, not
   by measuring better.** C-B, C-C and C-E all drop to four mostly-financial
   buffers. Financial buffers co-moving is an established result; the
   distinctive claim is that energy, health, fiscal and social buffers move
   together. Power on the narrow question is not a substitute.

3. **The one genuine methodological improvement available is C-D**, which keeps
   all eight domains, is exactly calibrated at 0.099, and uses every window
   rather than two endpoints. It is a better instrument. It is still
   underpowered.

4. **Two findings are independent of power and would survive any redesign:** a
   constant common drift is invisible to this statistic (D1), and the crisis
   exclusion rule as written biases toward confirmation (reviewer notes item 5).

The publishable finding, if the decision goes that way, is **"not testable at
adequate power with available annual series"** — which the design brief already
identifies as legitimate. Nothing in these results contradicts it.

## Files

| File | Contents |
|---|---|
| `summary.json` | Everything machine-readable: seed, environment, layout, all curves, LRs, diagnostics. |
| `power_curves.csv` | Power at each effect size for every candidate. |
| `candidate_summary.csv` | The comparison table above. |
| `cf_drift_axis.csv` | C-F on its own effect axis. |
| `d2_sync_drift.csv` | Synchronized-drift diagnostic. |

## Assumptions

Identical to the frozen-design simulation and documented in
[`../power-simulation/README.md`](../power-simulation/README.md): baseline mean
pairwise correlation 0.20, crisis elevation +0.35, equicorrelation factor
structure, no serial dependence in the baseline DGP, percentile bootstrap
interval, rolling window 8 years (32 quarters), annual block length 2 and
quarterly 4.

Quarterly candidates are given the **same delta rho** as annual ones. That is
favourable to them: it assumes a quarterly co-movement shift of the same
magnitude as the annual one, which need not hold and is not measurable before
data contact. Their advantage in this table should be read as an upper bound.

The 1990-start candidate (C-C) uses the same crisis set, which contains no
pre-2000 years. Adding early-1990s crisis years would reduce its advantage.
