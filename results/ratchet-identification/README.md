# Ratchet criterion — synthetic identification check

**Verdict: the criterion does not discriminate. Per §8.2 of the draft
specification, it should not be frozen and H-R should not be tested by this
route.**

Run before any contact with real data. Everything here is synthetic.
Produced by [`../../scripts/analysis/ratchet_identification.py`](../../scripts/analysis/ratchet_identification.py),
seed `2026073101`, 2,000 series per world, 400 per sensitivity cell.
Reproduce with `python scripts/analysis/ratchet_identification.py`.

---

## The question

Not "does the criterion have power". The question is whether it can tell a
**ratchet** apart from an **ordinary secular decline** — because the index test
was withdrawn for exactly this class of failure, and asking the same question of
the replacement before freezing it is the entire point of running this.

## Headline

| | |
|---|---|
| Best-performing genuine ratchet world | **R-10, 9.1%** ratchet signature |
| Pure accelerating decline (S-acc) | **15.6%** ratchet signature |
| **Separation (best R − S-acc)** | **−6.5 points** |
| Criterion discriminates? | **No** |

**The separation is negative.** A world with no ratchet at all — just a decline
whose slope steepens — produces the ratchet signature *more often* than the best
genuine ratchet world does. On the discrimination that matters, the criterion is
not merely uninformative; it points the wrong way.

## Full results

| World | What it is | Ratchet sig. | Uninformative | Against H-R | Mixed |
|---|---|---|---|---|---|
| R-05 | genuine ratchet, 5% permanent step | 0.5% | 0.0% | **96.9%** | 2.6% |
| R-10 | genuine ratchet, 10% step | **9.1%** | 0.0% | 67.8% | 22.6% |
| R-15 | genuine ratchet, 15% step | 4.2% | 5.9% | 36.0% | 53.0% |
| R-20 | genuine ratchet, 20% step | 0.8% | 11.4% | 21.1% | 65.2% |
| R-decl | 15% step on a declining baseline | 4.3% | 4.8% | 34.0% | 56.4% |
| M-flat | full recovery, flat baseline | 0.0% | 0.0% | 99.7% | 0.3% |
| M-decl | full recovery, declining baseline | 0.1% | 0.0% | 99.7% | 0.2% |
| S-lin | pure linear decline, no episodes | 0.1% | 0.0% | 99.4% | 0.2% |
| S-acc | **pure accelerating decline, no episodes** | **15.6%** | 0.0% | 49.5% | 34.5% |

The criterion does one thing well: it correctly rejects H-R in the
mean-reversion worlds (M-flat, M-decl at ~99.7% "against"). If buffers genuinely
rebuild, this criterion will say so. That is worth something, and it is the only
thing that survives.

## Three distinct failures

### 1. Accelerating decline is mistaken for ratcheting

S-acc contains no episodes and no ratchet — only noise on a decline whose slope
steepens. It yields 15.6% ratchet signatures. The mechanism is the same one that
killed the index test: **early in the sample the trend is nearly flat, so
noise-driven dips recover; late in the sample the trend is steep, so they do
not.** The early-versus-late comparison in §6 reads that as a regime change in
rebuild behaviour, which is precisely the ratchet signature it was built to
detect.

### 2. A shallow but real ratchet is reported as evidence *against* the hypothesis

R-05 is a genuine ratchet — every episode steps the buffer permanently down by
5% — and the criterion returns "against H-R" **96.9%** of the time.

This is not a missed detection. It is a confident, wrong answer in the opposite
direction. The cause is arithmetic: the rebuild bar is 90% of the pre-episode
peak, so any permanent step smaller than 10% leaves the series above the bar and
scores as "rebuilt". **The criterion is structurally blind to ratchets shallower
than `1 − REBUILD_FRACTION`, and reports that blindness as refutation.**

### 3. The confound control makes a *consistent* ratchet invisible

R-20 — the most severe ratchet simulated — yields 0.8% ratchet signatures, 11.4%
uninformative, and 65.2% mixed.

The reason is a logical flaw in §6, not a tuning problem. The early-versus-late
rule detects a **change** in rebuild behaviour: rebuilt early, not rebuilt late.
But H-R as written claims buffers *systematically* fail to rebuild — a
**consistent** ratchet, which fails to rebuild in both eras and therefore scores
uninformative or mixed under the very rule designed to protect against secular
decline.

**§6 protects against the confound by making the hypothesis untestable.** A
consistent ratchet and a secular decline are observationally identical to this
criterion, which is the same identification problem the index test died of,
reappearing in a different statistic.

## Sensitivity: the failure is not a tuning artifact

Across the 27-cell grid (σ ∈ {1.0, 1.5, 2.0} × rebuild ∈ {80%, 90%, 95%} ×
window ∈ {5, 7, 10} years):

| | |
|---|---|
| Cells where S-acc ≥ R-15 (criterion inverted) | **22 of 27** |
| Cells with separation ≥ +20 points | **0 of 27** |
| Separation range | **−67.8 to +2.0 points** |
| Worst cell (σ=1.0, 95%, 7yr) | R-15 0.5% vs S-acc **68.2%** |
| Best cell (σ=2.0, 80%, 5yr) | R-15 2.0% vs S-acc 0.0% |

**No parameter combination achieves useful separation.** The single best cell
manages +2.0 points, driven by both worlds detecting almost nothing rather than
by discrimination. Tightening the rebuild bar — the intuitive fix for failure 2 —
makes failure 1 dramatically worse, because a stricter bar means noise-driven
dips on a steepening trend rebuild even less often.

## What this does and does not license

**Does not license:** freezing this specification, or running Study 2 against
real data on these terms. §8.2 of the draft committed in advance to publishing
this outcome rather than proceeding, and the check returned the outcome that
triggers it.

**Does license:** the finding itself. That a natural, mechanically-specified
ratchet criterion cannot separate ratcheting from accelerating decline — and
that the standard confound control for secular decline makes a consistent
ratchet untestable — is a real methodological result, obtained before data
contact and at the cost of one day.

**An amendment would have to solve identification, not tuning.** §9 permits one
documented amendment. The grid shows no parameter setting rescues this, so any
amendment would need to change the *statistic*, not its constants — for example
by modelling the trend explicitly and testing for a step in its level, rather
than inferring ratcheting from rebuild-versus-not counts. Whether that is worth
doing, or whether Study 2 is abandoned, is a decision for the author. **No
amendment has been made here.**

## Files

| File | Contents |
|---|---|
| `summary.json` | Seed, environment, criterion constants, all worlds, full grid, headline. |
| `worlds.csv` | Per-world detection and verdict distribution. |
| `sensitivity_grid.csv` | All 27 parameter cells. |

## Simulation assumptions

Annual series 1950–2026 (77 observations), base level 100, noise SD 2.0,
episodes roughly once per decade with drawdowns of 14–20% of the pre-episode
level over 1–2 years and recovery over 3–5 years. Ratchet severity is
parameterised directly as the permanent step-down after each episode, as a
fraction of the pre-episode level, because that is the quantity the rebuild
criterion actually keys on.

S-lin declines 0.45 units/year; S-acc declines as 0.010·t², reaching a similar
endpoint by a curved path. **S-acc is not in the original brief.** It was added
because curvature in a shared trend is what defeated the index test, and a
replacement criterion that had not been tested against it would have been
accepted on incomplete evidence.
