#!/usr/bin/env python3
"""Power and calibration simulation for the frozen buffer-correlation design.

Run BEFORE data contact. This estimates what the pre-registered design can and
cannot detect, using synthetic data only. No real series is read, fetched, or
touched by this script.

The design being simulated (frozen; this script does not modify it):
    - 8 domains, annual observations, first differences of z-scored series
    - test statistic: unweighted mean of the 28 pairwise Pearson correlations
    - crisis-excluded blocks B1ex (7 observations) and B3ex (6 observations)
    - headline contrast: delta_rho = rhobar(B3ex) - rhobar(B1ex)
    - inference: moving-block bootstrap, block length 2, 5000 replications,
      one-sided 90 percent bound

Five experiments:
    A  power curve         P(C1 and C2) across true delta_rho, and the MDE
    B  bootstrap coverage  false-positive rate of the 90 percent bound at zero
    C  crisis leakage      bias from excluding by year label
    D  domain dilution     8 domains where one is noise, versus 7 informative
    (full-criteria power P(CONFIRM) is computed alongside A)

Usage:
    python scripts/analysis/power_sim.py              # full run
    python scripts/analysis/power_sim.py --quick      # smoke test

Outputs land in results/power-simulation/.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------
# Reproducibility
# --------------------------------------------------------------------------

SEED = 20260728

# --------------------------------------------------------------------------
# Frozen design constants
# --------------------------------------------------------------------------

N_DOMAINS = 8
N_PAIRS = N_DOMAINS * (N_DOMAINS - 1) // 2      # 28
BLOCK_LENGTH = 2
N_BOOTSTRAP = 5000
BOUND_PERCENTILE = 10.0                          # one-sided 90 percent lower bound
N_DIRICHLET = 1000
DIRICHLET_SIGN_THRESHOLD = 0.90
ROLLING_WINDOW = 7                               # for the C4 Mann-Kendall series

# --------------------------------------------------------------------------
# Year layout -- CORRECTED 2026-07-28
#
# This is the actual layout of the frozen design, supplied by the author. It
# supersedes the layout previously inferred here, which was wrong.
#
# Difference sample 2001-2026 (26 observations), split into thirds:
#     B1 = 2001-2009 (9), B2 = 2010-2017 (8), B3 = 2018-2026 (9)
# Crisis set E = {2008, 2009, 2020, 2021, 2026}; 2001 is deliberately NOT in E.
#
# The correction matters for one reason, and it is not cosmetic. Exclusion is
# by the difference's own year label, so a difference reaching back into an
# excluded year survives. Under this layout:
#     delta_2010 leaks from 2009 -- but 2010 falls in B2, which is NOT an
#                                   endpoint block and bears on nothing
#     delta_2022 leaks from 2021 -- and 2022 IS in B3ex
# So contamination is ONE-SIDED: zero leaked differences in B1ex, one in B3ex.
# Under the previously assumed layout it entered both blocks and cancelled.
# --------------------------------------------------------------------------

DIFF_YEARS = list(range(2001, 2027))             # delta_t = z_t - z_{t-1}, 26 diffs
B1_YEARS = list(range(2001, 2010))               # 9 diffs
B2_YEARS = list(range(2010, 2018))               # 8 diffs (middle third)
B3_YEARS = list(range(2018, 2027))               # 9 diffs
CRISIS_YEARS = {2008, 2009, 2020, 2021, 2026}

# Exclusion as the spec performs it: drop a difference when its own year LABEL
# is a crisis year. A difference reaching back into an excluded year survives.
B1EX_YEARS = [y for y in B1_YEARS if y not in CRISIS_YEARS]          # 7
B3EX_YEARS = [y for y in B3_YEARS if y not in CRISIS_YEARS]          # 6

# Exclusion as it would be done cleanly: drop a difference if EITHER endpoint
# falls in a crisis year. This is the benchmark experiment C measures against.
B1CLEAN_YEARS = [y for y in B1_YEARS
                 if y not in CRISIS_YEARS and (y - 1) not in CRISIS_YEARS]   # 6
B3CLEAN_YEARS = [y for y in B3_YEARS
                 if y not in CRISIS_YEARS and (y - 1) not in CRISIS_YEARS]   # 5

# --------------------------------------------------------------------------
# Data-generating process parameters
#
# The spec fixes the test but not the world it is tested against. These are
# simulation assumptions, not pre-registered quantities, and every headline
# number below is conditional on them.
# --------------------------------------------------------------------------

RHO_BASE = 0.20          # mean pairwise correlation in the B1 era
CRISIS_BOOST = 0.35      # elevation of cross-domain correlation in crisis years
RHO_MAX = 0.95           # cap, since equicorrelation must stay a valid correlation

DELTA_GRID = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

# Grid beyond the pre-specified range. Used only to locate the MDE when power
# does not reach the target anywhere on DELTA_GRID. Reporting "not reached" is
# honest but uninformative; a reader deserves to know where it IS reached, even
# when the answer is an implausibly large effect.
EXTENSION_GRID = [0.55, 0.60, 0.65, 0.70, 0.80, 0.90]

TARGET_POWER = 0.80

# --------------------------------------------------------------------------
# Statistic
# --------------------------------------------------------------------------


def _standardize(x: np.ndarray) -> np.ndarray:
    """Standardize along the observation axis (-2), with ddof=1.

    A guard is applied for zero-variance columns. These are not hypothetical
    here: with 6 observations and 3 resampled blocks, the moving-block
    bootstrap draws the same block three times about 4 percent of the time.
    """
    mean = x.mean(axis=-2, keepdims=True)
    std = x.std(axis=-2, ddof=1, keepdims=True)
    std = np.where(std < 1e-12, 1.0, std)
    return (x - mean) / std


def mean_pairwise_corr(x: np.ndarray) -> np.ndarray:
    """Unweighted mean of all pairwise Pearson correlations.

    x has shape (..., n_obs, n_domains); the return has shape (...).

    Uses the identity sum_ij R_ij = ||sum_j u_j||^2 / (n - 1) for standardized
    columns u_j, which avoids forming the correlation matrix. With 5000
    bootstrap replications per dataset and tens of thousands of datasets, the
    difference is the difference between minutes and hours.
    """
    n_obs = x.shape[-2]
    n_dom = x.shape[-1]
    u = _standardize(x)
    s = u.sum(axis=-1)                            # (..., n_obs)
    total = (s ** 2).sum(axis=-1) / (n_obs - 1)   # sum over the full matrix
    return (total - n_dom) / (n_dom * (n_dom - 1))


def pairwise_corrs(x: np.ndarray) -> np.ndarray:
    """All pairwise correlations. x is (n_obs, n_domains); returns (n_pairs,)."""
    u = _standardize(x)
    r = (u.T @ u) / (x.shape[-2] - 1)
    iu = np.triu_indices(x.shape[-1], k=1)
    return r[iu]


# --------------------------------------------------------------------------
# Data generation
# --------------------------------------------------------------------------


def rho_schedule(delta_rho: float,
                 crisis_boost: float = CRISIS_BOOST) -> np.ndarray:
    """True mean pairwise correlation for each difference year.

    Flat at RHO_BASE through the B1 era, linearly rising across the untested
    middle years, flat at RHO_BASE + delta_rho through the B3 era. The linear
    middle exists so that the Mann-Kendall leg of C4 is testing something
    coherent rather than a step function.

    A difference is crisis-touched when either endpoint year is a crisis year,
    and is elevated by CRISIS_BOOST. This is what makes leakage possible: the
    spec excludes on the difference's own label, not on its endpoints.
    """
    rho = np.empty(len(DIFF_YEARS))
    for i, year in enumerate(DIFF_YEARS):
        if year <= B1_YEARS[-1]:
            level = RHO_BASE
        elif year >= B3_YEARS[0]:
            level = RHO_BASE + delta_rho
        else:
            span = B3_YEARS[0] - B1_YEARS[-1]
            frac = (year - B1_YEARS[-1]) / span
            level = RHO_BASE + frac * delta_rho
        if year in CRISIS_YEARS or (year - 1) in CRISIS_YEARS:
            level += crisis_boost
        rho[i] = min(level, RHO_MAX)
    return rho


def simulate(rng: np.random.Generator, n_datasets: int, delta_rho: float,
             noise_domain: bool = False, n_domains: int = N_DOMAINS,
             crisis_boost: float = CRISIS_BOOST) -> np.ndarray:
    """Simulate differenced data. Returns (n_datasets, n_years, n_domains).

    Equicorrelation is induced by a single common factor:
        x_j = sqrt(rho) * f + sqrt(1 - rho) * e_j
    which gives corr(x_i, x_j) = rho exactly for i != j.

    Note on z-scoring: the frozen design z-scores each series before
    differencing. That is a pure scale change, and Pearson correlation is
    scale-invariant, so it has no effect on any statistic computed here. The
    simulation therefore works directly in differences.

    If noise_domain is True, the last domain is generated as independent noise
    regardless of rho -- the weather-driven-proxy case in experiment D.
    """
    rho = rho_schedule(delta_rho, crisis_boost)               # (n_years,)
    n_years = len(DIFF_YEARS)
    rho_b = rho[None, :, None]

    common = rng.standard_normal((n_datasets, n_years, 1))
    idio = rng.standard_normal((n_datasets, n_years, n_domains))
    x = np.sqrt(rho_b) * common + np.sqrt(1.0 - rho_b) * idio

    if noise_domain:
        x[:, :, -1] = rng.standard_normal((n_datasets, n_years))
    return x


def year_index(years: list[int]) -> np.ndarray:
    base = DIFF_YEARS[0]
    return np.array([y - base for y in years], dtype=np.intp)


# --------------------------------------------------------------------------
# Moving-block bootstrap
# --------------------------------------------------------------------------


def block_starts(n_obs: int) -> int:
    """Number of distinct overlapping blocks available."""
    return n_obs - BLOCK_LENGTH + 1


def bootstrap_indices(rng: np.random.Generator, n_obs: int,
                      n_reps: int) -> np.ndarray:
    """Moving-block bootstrap index matrix of shape (n_reps, n_obs)."""
    n_blocks_needed = int(np.ceil(n_obs / BLOCK_LENGTH))
    n_starts = block_starts(n_obs)
    starts = rng.integers(0, n_starts, size=(n_reps, n_blocks_needed))
    offsets = np.arange(BLOCK_LENGTH)
    idx = (starts[:, :, None] + offsets[None, None, :]).reshape(n_reps, -1)
    return idx[:, :n_obs]


def bootstrap_lower_bound(rng: np.random.Generator, b1: np.ndarray,
                          b3: np.ndarray, n_reps: int) -> float:
    """One-sided lower confidence bound on delta_rho by percentile bootstrap.

    The two blocks are resampled independently. The spec fixes the bootstrap
    scheme, replication count, and confidence level, but not which bootstrap
    interval to construct; the percentile interval is used here and that choice
    is recorded in the results README.
    """
    i1 = bootstrap_indices(rng, b1.shape[0], n_reps)
    i3 = bootstrap_indices(rng, b3.shape[0], n_reps)
    stat = mean_pairwise_corr(b3[i3]) - mean_pairwise_corr(b1[i1])
    return float(np.percentile(stat, BOUND_PERCENTILE))


# --------------------------------------------------------------------------
# Criteria
# --------------------------------------------------------------------------


def mann_kendall_s(series: np.ndarray) -> float:
    """Mann-Kendall S = sum over i<j of sign(x_j - x_i)."""
    diff = series[None, :] - series[:, None]
    return float(np.sign(diff[np.triu_indices(len(series), k=1)]).sum())


def rolling_mean_corr(data: np.ndarray) -> np.ndarray:
    """Rolling mean pairwise correlation over the full differenced series."""
    n_years = data.shape[0]
    n_windows = n_years - ROLLING_WINDOW + 1
    windows = np.stack([data[i:i + ROLLING_WINDOW] for i in range(n_windows)])
    return mean_pairwise_corr(windows)


def evaluate_criteria(rng: np.random.Generator, data: np.ndarray,
                      n_reps: int) -> dict:
    """Evaluate C1-C4 on one simulated dataset. data is (n_years, n_domains)."""
    n_dom = data.shape[1]
    b1 = data[year_index(B1EX_YEARS)]
    b3 = data[year_index(B3EX_YEARS)]

    r1 = pairwise_corrs(b1)
    r3 = pairwise_corrs(b3)
    delta_hat = float(r3.mean() - r1.mean())

    # C1: positive point estimate.
    c1 = delta_hat > 0.0

    # C2: one-sided 90 percent bound excludes zero.
    lower = bootstrap_lower_bound(rng, b1, b3, n_reps)
    c2 = lower > 0.0

    # C3a: sign survives dropping each domain in turn.
    iu = np.triu_indices(n_dom, k=1)
    drop_ok = True
    drop_deltas = []
    for d in range(n_dom):
        keep = (iu[0] != d) & (iu[1] != d)
        dd = float(r3[keep].mean() - r1[keep].mean())
        drop_deltas.append(dd)
        if np.sign(dd) != np.sign(delta_hat) or dd == 0.0:
            drop_ok = False

    # C3b: sign survives reweighting the pairs.
    #
    # For weights w summing to 1, the weighted contrast is sum_p w_p * g_p with
    # g = r3 - r1. A symmetric Dirichlet(1) draw is a normalized vector of unit
    # exponentials, and the normalizer is positive, so the SIGN of the weighted
    # contrast is the sign of the unnormalized dot product. That lets the 1000
    # reweightings collapse to a single matrix-vector product.
    g = r3 - r1
    e = rng.standard_exponential((N_DIRICHLET, len(g)))
    weighted = e @ g
    frac_same = float(np.mean(np.sign(weighted) == np.sign(delta_hat)))
    c3b = frac_same >= DIRICHLET_SIGN_THRESHOLD
    c3 = bool(drop_ok and c3b)

    # C4: crisis-INCLUDED contrast non-negative, and a non-negative
    # Mann-Kendall on the rolling series.
    b1_all = data[year_index(B1_YEARS)]
    b3_all = data[year_index(B3_YEARS)]
    incl = float(mean_pairwise_corr(b3_all) - mean_pairwise_corr(b1_all))
    mk = mann_kendall_s(rolling_mean_corr(data))
    c4 = bool(incl >= 0.0 and mk >= 0.0)

    return {
        "delta_hat": delta_hat,
        "lower": lower,
        "c1": bool(c1),
        "c2": bool(c2),
        "c3": c3,
        "c3_drop": bool(drop_ok),
        "c3_weight": bool(c3b),
        "c4": c4,
        "incl_contrast": incl,
        "mk": mk,
        "min_drop_delta": float(min(drop_deltas)),
    }


# --------------------------------------------------------------------------
# Experiments
# --------------------------------------------------------------------------


def experiment_power(rng: np.random.Generator, n_datasets: int,
                     n_reps: int, grid: list[float] | None = None) -> list[dict]:
    """A: power curve and full-criteria power across the delta_rho grid."""
    rows = []
    for delta in (DELTA_GRID if grid is None else grid):
        t0 = time.time()
        data = simulate(rng, n_datasets, delta)
        acc = {k: 0 for k in ("c1", "c2", "c12", "c3", "c4", "confirm")}
        deltas = np.empty(n_datasets)
        lowers = np.empty(n_datasets)
        for i in range(n_datasets):
            res = evaluate_criteria(rng, data[i], n_reps)
            deltas[i] = res["delta_hat"]
            lowers[i] = res["lower"]
            acc["c1"] += res["c1"]
            acc["c2"] += res["c2"]
            acc["c12"] += res["c1"] and res["c2"]
            acc["c3"] += res["c3"]
            acc["c4"] += res["c4"]
            acc["confirm"] += res["c1"] and res["c2"] and res["c3"] and res["c4"]
        rows.append({
            "true_delta_rho": delta,
            "n_datasets": n_datasets,
            "mean_delta_hat": float(deltas.mean()),
            "sd_delta_hat": float(deltas.std(ddof=1)),
            "mean_lower_bound": float(lowers.mean()),
            "p_c1": acc["c1"] / n_datasets,
            "p_c2": acc["c2"] / n_datasets,
            "power_c1_c2": acc["c12"] / n_datasets,
            "p_c3": acc["c3"] / n_datasets,
            "p_c4": acc["c4"] / n_datasets,
            "power_confirm": acc["confirm"] / n_datasets,
        })
        print("  delta=%.2f  power(C1&C2)=%.3f  power(CONFIRM)=%.3f  [%.0fs]"
              % (delta, rows[-1]["power_c1_c2"], rows[-1]["power_confirm"],
                 time.time() - t0))
    return rows


def _coverage_rate(rng: np.random.Generator, n_datasets: int, n_reps: int,
                   crisis_boost: float) -> tuple[float, float]:
    data = simulate(rng, n_datasets, 0.0, crisis_boost=crisis_boost)
    n_reject = 0
    lowers = np.empty(n_datasets)
    for i in range(n_datasets):
        b1 = data[i][year_index(B1EX_YEARS)]
        b3 = data[i][year_index(B3EX_YEARS)]
        lower = bootstrap_lower_bound(rng, b1, b3, n_reps)
        lowers[i] = lower
        n_reject += lower > 0.0
    return n_reject / n_datasets, float(lowers.mean())


def experiment_coverage(rng: np.random.Generator, n_datasets: int,
                        n_reps: int) -> dict:
    """B: false-positive rate of the one-sided bound when the truth is zero.

    Run twice. The design as specified carries crisis elevation, and under the
    corrected layout that leaks one-sidedly into B3ex. Re-running with the
    elevation switched off isolates how much of the anti-conservatism is the
    small-sample bootstrap alone, and how much the exclusion rule adds on top.
    Without this split the two causes are indistinguishable in the headline
    number.
    """
    rate, mean_lower = _coverage_rate(rng, n_datasets, n_reps, CRISIS_BOOST)
    rate_no_leak, _ = _coverage_rate(rng, n_datasets, n_reps, 0.0)
    se = float(np.sqrt(rate * (1 - rate) / n_datasets))
    return {
        "empirical_rate_no_crisis_elevation": rate_no_leak,
        "leakage_contribution": rate - rate_no_leak,
        "n_datasets": n_datasets,
        "nominal_rate": 0.10,
        "empirical_rate": rate,
        "monte_carlo_se": se,
        "miscalibration": rate - 0.10,
        "direction": ("anti-conservative" if rate > 0.10 else
                      "conservative" if rate < 0.10 else "exact"),
        "mean_lower_bound": mean_lower,
        "n_blocks_b1": block_starts(len(B1EX_YEARS)),
        "n_blocks_b3": block_starts(len(B3EX_YEARS)),
        "blocks_drawn_b1": int(np.ceil(len(B1EX_YEARS) / BLOCK_LENGTH)),
        "blocks_drawn_b3": int(np.ceil(len(B3EX_YEARS) / BLOCK_LENGTH)),
    }


def _spec_minus_clean(rng: np.random.Generator, n_datasets: int, delta: float,
                      crisis_boost: float) -> tuple[np.ndarray, np.ndarray]:
    """Paired difference between the two exclusion rules on identical data."""
    data = simulate(rng, n_datasets, delta, crisis_boost=crisis_boost)
    spec = (mean_pairwise_corr(data[:, year_index(B3EX_YEARS)])
            - mean_pairwise_corr(data[:, year_index(B1EX_YEARS)]))
    clean = (mean_pairwise_corr(data[:, year_index(B3CLEAN_YEARS)])
             - mean_pairwise_corr(data[:, year_index(B1CLEAN_YEARS)]))
    return spec, clean


def experiment_leakage(rng: np.random.Generator, n_datasets: int) -> list[dict]:
    """C: bias from excluding crisis years by label rather than by endpoint.

    Label-based exclusion keeps B1ex=7 and B3ex=6; clean exclusion keeps 6 and
    5. Those differ in TWO ways, not one: contamination, and sample size. Small
    samples attenuate Pearson correlations toward zero, and they attenuate the
    smaller block more, so a raw spec-minus-clean comparison confounds leakage
    with an arithmetic artifact of the differing n.

    The confound is removed by re-running with the crisis elevation switched
    off. That control has identical block sizes and no contamination, so
    whatever spec-minus-clean it produces is pure sample-size artifact. The
    leakage effect is the difference between the two.
    """
    rows = []
    for delta in (0.00, 0.15):
        spec, clean = _spec_minus_clean(rng, n_datasets, delta, CRISIS_BOOST)
        raw = spec - clean
        # Control: same design, same block sizes, no crisis elevation.
        c_spec, c_clean = _spec_minus_clean(rng, n_datasets, delta, 0.0)
        artifact = c_spec - c_clean
        net = raw.mean() - artifact.mean()
        se_net = float(np.sqrt(raw.var(ddof=1) / n_datasets
                               + artifact.var(ddof=1) / n_datasets))
        rows.append({
            "true_delta_rho": delta,
            "n_datasets": n_datasets,
            "mean_delta_spec_exclusion": float(spec.mean()),
            "mean_delta_clean_exclusion": float(clean.mean()),
            "raw_spec_minus_clean": float(raw.mean()),
            "sample_size_artifact": float(artifact.mean()),
            "net_leakage_bias": float(net),
            "se_net_leakage_bias": se_net,
            "bias_direction": ("toward CONFIRM" if net > 0
                               else "away from CONFIRM"),
            "retained_leaked_diffs_b1": [y for y in B1EX_YEARS
                                         if (y - 1) in CRISIS_YEARS],
            "retained_leaked_diffs_b3": [y for y in B3EX_YEARS
                                         if (y - 1) in CRISIS_YEARS],
        })
        print("  delta=%.2f  raw=%+.4f  artifact=%+.4f  net leakage=%+.4f (se %.4f)"
              % (delta, raw.mean(), artifact.mean(), net, se_net))
    return rows


def experiment_dilution(rng: np.random.Generator, n_datasets: int,
                        n_reps: int) -> list[dict]:
    """D: 7 informative domains versus 8 where the eighth is pure noise."""
    rows = []
    for delta in (0.10, 0.20, 0.30):
        # 7 informative domains.
        d7 = simulate(rng, n_datasets, delta, n_domains=7)
        s7 = (mean_pairwise_corr(d7[:, year_index(B3EX_YEARS)])
              - mean_pairwise_corr(d7[:, year_index(B1EX_YEARS)]))

        # 8 domains, the eighth pure noise.
        d8 = simulate(rng, n_datasets, delta, noise_domain=True, n_domains=8)
        s8 = (mean_pairwise_corr(d8[:, year_index(B3EX_YEARS)])
              - mean_pairwise_corr(d8[:, year_index(B1EX_YEARS)]))

        # Power for each, on a subsample to keep the bootstrap affordable.
        n_pow = min(n_datasets, 600)
        pow7 = pow8 = 0
        for i in range(n_pow):
            b1 = d7[i][year_index(B1EX_YEARS)]
            b3 = d7[i][year_index(B3EX_YEARS)]
            est = float(mean_pairwise_corr(b3) - mean_pairwise_corr(b1))
            pow7 += est > 0 and bootstrap_lower_bound(rng, b1, b3, n_reps) > 0
            b1 = d8[i][year_index(B1EX_YEARS)]
            b3 = d8[i][year_index(B3EX_YEARS)]
            est = float(mean_pairwise_corr(b3) - mean_pairwise_corr(b1))
            pow8 += est > 0 and bootstrap_lower_bound(rng, b1, b3, n_reps) > 0

        rows.append({
            "true_delta_rho": delta,
            "n_datasets": n_datasets,
            "mean_delta_7_informative": float(s7.mean()),
            "mean_delta_8_with_noise": float(s8.mean()),
            "shrinkage_ratio": float(s8.mean() / s7.mean()),
            "shrinkage_pct": float(100 * (1 - s8.mean() / s7.mean())),
            "n_power_datasets": n_pow,
            "power_7_informative": pow7 / n_pow,
            "power_8_with_noise": pow8 / n_pow,
            "power_loss": (pow7 - pow8) / n_pow,
        })
        print("  delta=%.2f  7dom=%.4f  8dom=%.4f  shrink=%.1f%%  power %.3f->%.3f"
              % (delta, s7.mean(), s8.mean(), rows[-1]["shrinkage_pct"],
                 rows[-1]["power_7_informative"], rows[-1]["power_8_with_noise"]))
    return rows


# --------------------------------------------------------------------------
# Reporting helpers
# --------------------------------------------------------------------------


def interpolate_mde(rows: list[dict], key: str,
                    target: float = TARGET_POWER) -> float | None:
    """Smallest true delta_rho reaching target power, by linear interpolation."""
    for prev, cur in zip(rows, rows[1:]):
        if prev[key] < target <= cur[key]:
            span = cur[key] - prev[key]
            if span <= 0:
                return cur["true_delta_rho"]
            frac = (target - prev[key]) / span
            return prev["true_delta_rho"] + frac * (
                cur["true_delta_rho"] - prev["true_delta_rho"])
    if rows and rows[-1][key] >= target:
        return rows[-1]["true_delta_rho"]
    return None


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    keys = list(rows[0].keys())
    lines = [",".join(keys)]
    for row in rows:
        vals = []
        for k in keys:
            v = row[k]
            if isinstance(v, list):
                v = " ".join(str(x) for x in v)
            if isinstance(v, float):
                v = "%.6f" % v
            vals.append(str(v))
        lines.append(",".join(vals))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def make_plots(outdir: Path, power_rows: list[dict], leak_rows: list[dict],
               dil_rows: list[dict], coverage: dict) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False

    d = [r["true_delta_rho"] for r in power_rows]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(d, [r["power_c1_c2"] for r in power_rows], marker="o",
            label="P(C1 and C2)")
    ax.plot(d, [r["power_confirm"] for r in power_rows], marker="s",
            label="P(CONFIRM, all four)")
    ax.axhline(TARGET_POWER, ls="--", lw=1, color="grey", label="0.80 target")
    ax.set_xlabel("true delta rho")
    ax.set_ylabel("probability")
    ax.set_title("Power of the frozen design")
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / "power_curve.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for key, label in (("p_c1", "C1 sign"), ("p_c2", "C2 bound"),
                       ("p_c3", "C3 robustness"), ("p_c4", "C4 corroboration")):
        ax.plot(d, [r[key] for r in power_rows], marker=".", label=label)
    ax.set_xlabel("true delta rho")
    ax.set_ylabel("pass rate")
    ax.set_title("Individual criterion pass rates")
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / "criteria_components.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(["nominal", "empirical"], [coverage["nominal_rate"],
                                      coverage["empirical_rate"]],
           color=["grey", "firebrick"])
    ax.set_ylabel("false-positive rate at true delta rho = 0")
    ax.set_title("Bootstrap calibration of the one-sided 90 percent bound")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(outdir / "bootstrap_coverage.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    xs = np.arange(len(leak_rows))
    ax.bar(xs - 0.2, [r["sample_size_artifact"] for r in leak_rows],
           width=0.4, label="sample-size artifact", color="lightsteelblue")
    ax.bar(xs + 0.2, [r["net_leakage_bias"] for r in leak_rows],
           width=0.4, label="net leakage", color="darkorange")
    ax.set_xticks(xs)
    ax.set_xticklabels([str(r["true_delta_rho"]) for r in leak_rows])
    ax.axhline(0, color="black", lw=1)
    ax.set_xlabel("true delta rho")
    ax.set_ylabel("bias in delta rho")
    ax.set_title("Crisis-exclusion leakage, decomposed")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(outdir / "crisis_leakage.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    xs = np.arange(len(dil_rows))
    ax.bar(xs - 0.2, [r["mean_delta_7_informative"] for r in dil_rows],
           width=0.4, label="7 informative domains")
    ax.bar(xs + 0.2, [r["mean_delta_8_with_noise"] for r in dil_rows],
           width=0.4, label="8 domains, one noise")
    ax.set_xticks(xs)
    ax.set_xticklabels([str(r["true_delta_rho"]) for r in dil_rows])
    ax.set_xlabel("true delta rho")
    ax.set_ylabel("recovered delta rho")
    ax.set_title("Dilution from a non-informative eighth domain")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(outdir / "domain_dilution.png", dpi=150)
    plt.close(fig)
    return True


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true",
                        help="tiny run for smoke-testing the pipeline")
    parser.add_argument("--n-datasets", type=int, default=2000)
    parser.add_argument("--n-boot", type=int, default=N_BOOTSTRAP)
    parser.add_argument("--n-coverage", type=int, default=5000)
    args = parser.parse_args()

    n_datasets = 40 if args.quick else args.n_datasets
    n_reps = 200 if args.quick else args.n_boot
    n_cov = 60 if args.quick else args.n_coverage

    repo_root = Path(__file__).resolve().parent.parent.parent
    outdir = repo_root / "results" / "power-simulation"
    outdir.mkdir(parents=True, exist_ok=True)

    # Sanity checks on the frozen block sizes. If these fail, the year layout
    # has drifted from the spec and every number below would be meaningless.
    assert len(B1EX_YEARS) == 7, "B1ex must have 7 observations"
    assert len(B3EX_YEARS) == 6, "B3ex must have 6 observations"

    print("Buffer-correlation power simulation")
    print("seed=%d  datasets/condition=%d  bootstrap reps=%d"
          % (SEED, n_datasets, n_reps))
    print("B1ex years: %s" % B1EX_YEARS)
    print("B3ex years: %s" % B3EX_YEARS)
    print("")

    t_start = time.time()
    seeds = np.random.SeedSequence(SEED).spawn(5)

    print("A. power curve")
    power_rows = experiment_power(np.random.default_rng(seeds[0]),
                                  n_datasets, n_reps)

    # If the target power is never reached on the pre-specified grid, extend it
    # to locate the MDE. This is reporting, not a change to the design.
    ext_rows: list[dict] = []
    if interpolate_mde(power_rows, "power_c1_c2") is None:
        ext_grid = EXTENSION_GRID if not args.quick else [0.7, 0.9]
        print("A2. target power not reached on the pre-specified grid; "
              "extending to locate the MDE")
        ext_rows = experiment_power(np.random.default_rng(seeds[4]),
                                    n_datasets, n_reps, grid=ext_grid)

    print("B. bootstrap coverage at delta_rho = 0")
    coverage = experiment_coverage(np.random.default_rng(seeds[1]),
                                   n_cov, n_reps)
    print("  empirical=%.4f (nominal 0.10), %s"
          % (coverage["empirical_rate"], coverage["direction"]))
    print("C. crisis-exclusion leakage")
    leak_rows = experiment_leakage(np.random.default_rng(seeds[2]), n_datasets)
    print("D. domain-8 dilution")
    dil_rows = experiment_dilution(np.random.default_rng(seeds[3]),
                                   n_datasets, n_reps)

    combined = power_rows + ext_rows
    mde_c12 = interpolate_mde(combined, "power_c1_c2")
    mde_conf = interpolate_mde(combined, "power_confirm")
    mde_on_grid = interpolate_mde(power_rows, "power_c1_c2") is not None

    elapsed = time.time() - t_start

    write_csv(outdir / "power_curve.csv", power_rows)
    if ext_rows:
        write_csv(outdir / "power_curve_extended.csv", ext_rows)
    write_csv(outdir / "crisis_leakage.csv", leak_rows)
    write_csv(outdir / "domain_dilution.csv", dil_rows)

    summary = {
        "seed": SEED,
        "generated_by": "scripts/analysis/power_sim.py",
        "quick_mode": bool(args.quick),
        "n_datasets_per_condition": n_datasets,
        "n_bootstrap_replications": n_reps,
        "n_coverage_datasets": n_cov,
        "runtime_seconds": round(elapsed, 1),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "design": {
            "n_domains": N_DOMAINS,
            "n_pairs": N_PAIRS,
            "block_length": BLOCK_LENGTH,
            "b1ex_n": len(B1EX_YEARS),
            "b3ex_n": len(B3EX_YEARS),
            "b1ex_years": B1EX_YEARS,
            "b3ex_years": B3EX_YEARS,
            "crisis_years": sorted(CRISIS_YEARS),
            "rho_base": RHO_BASE,
            "crisis_boost": CRISIS_BOOST,
            "rolling_window": ROLLING_WINDOW,
        },
        "headline": {
            "mde_power80_c1_c2": mde_c12,
            "mde_power80_confirm": mde_conf,
            "mde_within_prespecified_grid": mde_on_grid,
            "prespecified_grid_max": DELTA_GRID[-1],
            "power_at_grid_max_c1_c2": power_rows[-1]["power_c1_c2"],
            "power_at_grid_max_confirm": power_rows[-1]["power_confirm"],
            "coverage": coverage,
            "conjunction_cost": [
                {
                    "true_delta_rho": r["true_delta_rho"],
                    "power_c1_c2": r["power_c1_c2"],
                    "power_confirm": r["power_confirm"],
                    "gap": r["power_c1_c2"] - r["power_confirm"],
                }
                for r in power_rows
            ],
            "leakage": leak_rows,
            "dilution": dil_rows,
        },
        "power_curve": power_rows,
        "power_curve_extended": ext_rows,
    }
    (outdir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")

    plotted = make_plots(outdir, combined, leak_rows, dil_rows, coverage)

    print("")
    print("MDE at power 0.80, C1 and C2 only : %s"
          % ("not reached on grid" if mde_c12 is None else "%.3f" % mde_c12))
    print("MDE at power 0.80, all four       : %s"
          % ("not reached on grid" if mde_conf is None else "%.3f" % mde_conf))
    print("plots written: %s" % plotted)
    print("elapsed: %.1f s" % elapsed)
    print("results in: %s" % outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
