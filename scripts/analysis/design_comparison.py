#!/usr/bin/env python3
"""Exploratory comparison of candidate designs, before any real data contact.

This informs a HUMAN decision about whether the buffer-correlation question is
testable at adequate power with available series. It changes NOTHING in the
frozen specification and is not itself a pre-registration.

No real series is read, fetched, or opened. Everything is synthetic.

Candidates
    C-A  frozen annual 8-domain two-endpoint-block contrast (reference row)
    C-B  quarterly 4-domain endpoint contrast, 2001-2026
    C-C  quarterly 4-domain endpoint contrast, 1990-2026
    C-D  annual 8-domain, rolling-window trend statistic (all windows)
    C-E  quarterly 4-domain, rolling-window trend statistic (power ceiling)
    C-F  co-depletion: trend in the annual count of domains falling

Diagnostics
    D1   does a constant common drift contribute to the correlation statistic?
    D2   is a synchronized, time-varying drift in the late block detected?

Every candidate's decision rule is a ONE-SIDED LEVEL-0.10 TEST in the
hypothesized direction, so that false-positive rates and likelihood ratios are
comparable across rows. For C-A that is the frozen percentile bootstrap bound;
for the trend candidates it is a moving-block bootstrap null on the slope.

Usage:
    python scripts/analysis/design_comparison.py            # full run
    python scripts/analysis/design_comparison.py --quick    # smoke test
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from power_sim import (  # noqa: E402
    mean_pairwise_corr,
    mann_kendall_s,
    write_csv,
    interpolate_mde,
)

SEED = 2026072802

# --------------------------------------------------------------------------
# Shared assumptions (same as the frozen-design simulation, for comparability)
# --------------------------------------------------------------------------

RHO_BASE = 0.20
CRISIS_BOOST = 0.35
RHO_MAX = 0.95
CRISIS_YEARS = {2008, 2009, 2020, 2021, 2026}

DELTA_GRID = [0.00, 0.10, 0.15, 0.20, 0.30, 0.45, 0.60, 0.80]
KEY_DELTAS = [0.10, 0.15, 0.20]
LR_DELTA = 0.15
TARGET_POWER = 0.80
ALPHA = 0.10                      # one-sided level, every candidate
ROLLING_YEARS = 8                 # rolling window, in years

# --------------------------------------------------------------------------
# Worlds
#
# A "world" is a data-generating configuration: a frequency, a span, and the
# era boundaries between which the correlation rises. Candidates are statistics
# applied to a world. C-A, C-D and C-F share one world, so they are compared on
# identical data rather than on separate simulations.
# --------------------------------------------------------------------------


def build_world(name: str, first_year: int, last_year: int, per_year: int,
                early_end: int, late_start: int, n_domains: int) -> dict:
    years, periods = [], []
    for y in range(first_year, last_year + 1):
        for q in range(per_year):
            years.append(y)
            periods.append((y, q))
    return {
        "name": name,
        "years": np.array(years),
        "periods": periods,
        "per_year": per_year,
        "early_end": early_end,
        "late_start": late_start,
        "n_domains": n_domains,
        "n_obs": len(years),
    }


WORLDS = {
    # Annual difference sample 2001-2026 (26 observations). Thirds:
    # B1 2001-2009 (9), B2 2010-2017 (8), B3 2018-2026 (9).
    "annual2001": build_world("annual2001", 2001, 2026, 1, 2009, 2018, 8),
    # Quarterly analogue at 4x resolution, same span and era boundaries.
    "quarterly2001": build_world("quarterly2001", 2001, 2026, 4, 2009, 2018, 4),
    # Quarterly from 1990. Thirds by year: 1990-2002, 2003-2014, 2015-2026.
    "quarterly1990": build_world("quarterly1990", 1990, 2026, 4, 2002, 2015, 4),
}


def rho_path(world: dict, delta: float,
             crisis_boost: float = CRISIS_BOOST) -> np.ndarray:
    """True mean pairwise correlation at each observation."""
    years = world["years"]
    early_end, late_start = world["early_end"], world["late_start"]
    span = late_start - early_end
    level = np.where(
        years <= early_end, RHO_BASE,
        np.where(years >= late_start, RHO_BASE + delta,
                 RHO_BASE + (years - early_end) / span * delta))
    # Crisis-touched: this observation's year, or the previous observation's
    # year, is in the crisis set. The previous observation is the previous
    # quarter at quarterly frequency.
    in_e = np.isin(years, list(CRISIS_YEARS))
    prev_in_e = np.concatenate([[False], in_e[:-1]])
    level = level + np.where(in_e | prev_in_e, crisis_boost, 0.0)
    return np.minimum(level, RHO_MAX)


def simulate(rng: np.random.Generator, n_datasets: int, world: dict,
             delta: float, crisis_boost: float = CRISIS_BOOST,
             n_domains: int | None = None,
             drift: np.ndarray | None = None,
             sync_drift_delta: float | None = None,
             sync_phi: float = 0.7) -> np.ndarray:
    """Simulate differences. Returns (n_datasets, n_obs, n_domains).

    Equicorrelation via a single common factor:
        x_j = sqrt(rho) * f + sqrt(1 - rho) * e_j

    drift: optional (n_obs,) mean added to EVERY domain identically. Used by
        diagnostic D1 and by the co-depletion effect axis.

    sync_drift_delta: if set, the correlation rise in the late era is produced
        NOT by the common factor but by a persistent, synchronized common drift
        component m_t (AR(1)) shared across domains -- diagnostic D2. The
        variance is solved so the induced correlation rise equals the requested
        delta.
    """
    n_dom = n_domains or world["n_domains"]
    n_obs = world["n_obs"]

    if sync_drift_delta is not None:
        rho = rho_path(world, 0.0, crisis_boost)
        rho_b = rho[None, :, None]
        common = rng.standard_normal((n_datasets, n_obs, 1))
        idio = rng.standard_normal((n_datasets, n_obs, n_dom))
        x = np.sqrt(rho_b) * common + np.sqrt(1.0 - rho_b) * idio
        # corr becomes (rho + v) / (1 + v); solve for v giving a rise of delta.
        d = sync_drift_delta
        v = d / (1.0 - RHO_BASE - d) if (1.0 - RHO_BASE - d) > 0 else 50.0
        innov_sd = np.sqrt(v * (1.0 - sync_phi ** 2))
        m = np.zeros((n_datasets, n_obs))
        eps = rng.standard_normal((n_datasets, n_obs)) * innov_sd
        m[:, 0] = eps[:, 0] / np.sqrt(1.0 - sync_phi ** 2)
        for t in range(1, n_obs):
            m[:, t] = sync_phi * m[:, t - 1] + eps[:, t]
        late = (world["years"] >= world["late_start"])[None, :]
        x = x + (m * late)[:, :, None]
        return x

    rho = rho_path(world, delta, crisis_boost)
    rho_b = rho[None, :, None]
    common = rng.standard_normal((n_datasets, n_obs, 1))
    idio = rng.standard_normal((n_datasets, n_obs, n_dom))
    x = np.sqrt(rho_b) * common + np.sqrt(1.0 - rho_b) * idio
    if drift is not None:
        x = x + drift[None, :, None]
    return x


# --------------------------------------------------------------------------
# Index helpers
# --------------------------------------------------------------------------


def idx_years(world: dict, years) -> np.ndarray:
    return np.flatnonzero(np.isin(world["years"], list(years)))


def idx_retained(world: dict) -> np.ndarray:
    """All observations whose own year label is not a crisis year."""
    return np.flatnonzero(~np.isin(world["years"], list(CRISIS_YEARS)))


# --------------------------------------------------------------------------
# Bootstrap and test machinery
# --------------------------------------------------------------------------


def block_indices(rng: np.random.Generator, n_obs: int, n_reps: int,
                  block_len: int) -> np.ndarray:
    n_blocks = int(np.ceil(n_obs / block_len))
    n_starts = n_obs - block_len + 1
    starts = rng.integers(0, n_starts, size=(n_reps, n_blocks))
    offs = np.arange(block_len)
    return (starts[:, :, None] + offs[None, None, :]).reshape(n_reps, -1)[:, :n_obs]


def endpoint_test(rng: np.random.Generator, x: np.ndarray, b1: np.ndarray,
                  b3: np.ndarray, n_reps: int, block_len: int) -> tuple:
    """Frozen-style contrast: percentile bootstrap lower bound on delta_rho."""
    d1, d3 = x[b1], x[b3]
    est = float(mean_pairwise_corr(d3) - mean_pairwise_corr(d1))
    i1 = block_indices(rng, len(b1), n_reps, block_len)
    i3 = block_indices(rng, len(b3), n_reps, block_len)
    reps = mean_pairwise_corr(d3[i3]) - mean_pairwise_corr(d1[i1])
    lower = float(np.percentile(reps, 100 * ALPHA))
    return est, lower, bool(est > 0 and lower > 0)


def rolling_corr(x: np.ndarray, window: int) -> np.ndarray:
    """Rolling mean pairwise correlation. x is (n_obs, D) or (B, n_obs, D).

    Computed from cumulative sums rather than by materialising every window.
    The naive form builds a (B, n_windows, window, D) array, which for the
    quarterly trend candidate is 6.8 million elements per dataset and dominates
    the entire run; this is O(n) instead of O(n * window) and gives bitwise-
    comparable results (verified in --selftest).
    """
    single = x.ndim == 2
    if single:
        x = x[None]
    b, n_obs, n_dom = x.shape
    w = window
    iu = np.triu_indices(n_dom, k=1)

    def winsum(a: np.ndarray) -> np.ndarray:
        c = np.concatenate([np.zeros_like(a[:, :1]), np.cumsum(a, axis=1)], axis=1)
        return c[:, w:] - c[:, :-w]

    sx = winsum(x)                                   # (b, n_win, D)
    sxx = winsum(x * x)                              # (b, n_win, D)
    sxy = winsum(x[:, :, iu[0]] * x[:, :, iu[1]])    # (b, n_win, P)

    num = w * sxy - sx[:, :, iu[0]] * sx[:, :, iu[1]]
    var = w * sxx - sx ** 2
    den = np.sqrt(np.maximum(var[:, :, iu[0]] * var[:, :, iu[1]], 0.0))
    with np.errstate(invalid="ignore", divide="ignore"):
        r = np.where(den < 1e-12, np.nan, num / np.where(den < 1e-12, 1.0, den))
    out = np.nan_to_num(np.nanmean(r, axis=2), nan=0.0)
    return out[0] if single else out


def ols_slope(y: np.ndarray) -> np.ndarray:
    """Least-squares slope of y against its own index, along the last axis."""
    n = y.shape[-1]
    t = np.arange(n, dtype=float)
    tc = t - t.mean()
    return (y * tc).sum(axis=-1) / (tc ** 2).sum()


def mk_batch(y: np.ndarray) -> np.ndarray:
    """Mann-Kendall S along the last axis, for a batch."""
    d = y[..., None, :] - y[..., :, None]
    iu = np.triu_indices(y.shape[-1], k=1)
    return np.sign(d[..., iu[0], iu[1]]).sum(axis=-1)


def trend_test(rng: np.random.Generator, x: np.ndarray, window: int,
               n_reps: int, block_len: int) -> tuple:
    """Trend in the rolling correlation, against a moving-block bootstrap null.

    Resampling blocks destroys any trend, so the resampled slopes form a valid
    null distribution. The test rejects when the observed slope exceeds its
    upper (1 - alpha) quantile: a one-sided level-alpha test, matching the
    level used by every other candidate.
    """
    series = rolling_corr(x, window)
    slope = float(ols_slope(series))
    mk = float(mann_kendall_s(series))
    idx = block_indices(rng, x.shape[0], n_reps, block_len)
    null = ols_slope(rolling_corr(x[idx], window))
    crit = float(np.percentile(null, 100 * (1 - ALPHA)))
    return slope, mk, crit, bool(slope > 0 and slope > crit)


def count_trend_test(rng: np.random.Generator, x: np.ndarray, n_reps: int,
                     block_len: int) -> tuple:
    """C-F: trend in the count of domains recording a negative change."""
    counts = (x < 0).sum(axis=-1).astype(float)
    slope = float(ols_slope(counts))
    mk = float(mann_kendall_s(counts))
    idx = block_indices(rng, len(counts), n_reps, block_len)
    null = ols_slope(counts[idx])
    crit = float(np.percentile(null, 100 * (1 - ALPHA)))
    return slope, mk, crit, bool(slope > 0 and slope > crit), float(counts.mean())


# --------------------------------------------------------------------------
# Candidates
# --------------------------------------------------------------------------

B3EX_ANNUAL = [2018, 2019, 2022, 2023, 2024, 2025]
B1EX_ANNUAL = list(range(2001, 2008))
B3EX_1990 = [2015, 2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025]
B1EX_1990 = list(range(1990, 2003))


def candidates() -> dict:
    a = WORLDS["annual2001"]
    q = WORLDS["quarterly2001"]
    q90 = WORLDS["quarterly1990"]
    return {
        "C-A": {
            "world": a, "kind": "endpoint", "n_domains": 8, "block_len": 2,
            "b1": idx_years(a, B1EX_ANNUAL), "b3": idx_years(a, B3EX_ANNUAL),
            "label": "frozen annual 8-domain endpoint contrast",
        },
        "C-B": {
            "world": q, "kind": "endpoint", "n_domains": 4, "block_len": 4,
            "b1": idx_years(q, B1EX_ANNUAL), "b3": idx_years(q, B3EX_ANNUAL),
            "label": "quarterly 4-domain endpoint contrast, 2001-2026",
        },
        "C-C": {
            "world": q90, "kind": "endpoint", "n_domains": 4, "block_len": 4,
            "b1": idx_years(q90, B1EX_1990), "b3": idx_years(q90, B3EX_1990),
            "label": "quarterly 4-domain endpoint contrast, 1990-2026",
        },
        "C-D": {
            "world": a, "kind": "trend", "n_domains": 8, "block_len": 2,
            "keep": idx_retained(a), "window": ROLLING_YEARS,
            "label": "annual 8-domain rolling-window trend",
        },
        "C-E": {
            "world": q, "kind": "trend", "n_domains": 4, "block_len": 4,
            "keep": idx_retained(q), "window": ROLLING_YEARS * 4,
            "label": "quarterly 4-domain rolling-window trend",
        },
        "C-F": {
            "world": a, "kind": "count", "n_domains": 8, "block_len": 2,
            "keep": idx_retained(a),
            "label": "co-depletion: trend in count of falling domains",
        },
    }


def run_condition(rng: np.random.Generator, cand: dict, delta: float,
                  n_datasets: int, n_reps: int,
                  drift: np.ndarray | None = None,
                  sync: float | None = None,
                  crisis_boost: float = CRISIS_BOOST) -> dict:
    """Estimate the confirm rate for one candidate at one effect size.

    crisis_boost is exposed so diagnostics can switch the crisis elevation off.
    Leaving it on would contaminate them with the leakage bias, which is a
    separate effect and would be misread as the thing being diagnosed.
    """
    world = cand["world"]
    data = simulate(rng, n_datasets, world, delta, crisis_boost=crisis_boost,
                    n_domains=cand["n_domains"],
                    drift=drift, sync_drift_delta=sync)
    n_conf = 0
    mk_pos = 0
    ests = np.empty(n_datasets)
    extra = np.empty(n_datasets)
    for i in range(n_datasets):
        if cand["kind"] == "endpoint":
            est, _, conf = endpoint_test(rng, data[i], cand["b1"], cand["b3"],
                                         n_reps, cand["block_len"])
            ests[i], extra[i] = est, 0.0
        elif cand["kind"] == "trend":
            est, mk, _, conf = trend_test(rng, data[i][cand["keep"]],
                                          cand["window"], n_reps,
                                          cand["block_len"])
            ests[i], extra[i] = est, mk
            mk_pos += mk > 0
        else:
            est, mk, _, conf, lvl = count_trend_test(
                rng, data[i][cand["keep"]], n_reps, cand["block_len"])
            ests[i], extra[i] = est, lvl
            mk_pos += mk > 0
        n_conf += conf
    p = n_conf / n_datasets
    return {
        "power": p,
        "se": float(np.sqrt(max(p * (1 - p), 1e-12) / n_datasets)),
        "mean_stat": float(ests.mean()),
        "mean_extra": float(extra.mean()),
        "mk_positive_rate": mk_pos / n_datasets if cand["kind"] != "endpoint" else None,
    }


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------


def selftest() -> int:
    """Check the optimized rolling correlation against the naive construction.

    The naive version materialises every window and reuses mean_pairwise_corr
    from the frozen-design script, so agreement also confirms the two scripts
    compute the same statistic.
    """
    rng = np.random.default_rng(0)
    ok = True
    for n_dom, window, n_obs in ((4, 32, 84), (8, 8, 21), (3, 5, 12)):
        x = rng.standard_normal((7, n_obs, n_dom))
        fast = rolling_corr(x, window)
        n_win = n_obs - window + 1
        idx = np.arange(n_win)[:, None] + np.arange(window)[None, :]
        naive = np.stack([mean_pairwise_corr(x[b][idx, :]) for b in range(7)])
        close = np.allclose(fast, naive, atol=1e-10)
        worst = float(np.abs(fast - naive).max())
        ok = ok and close
        print("  D=%d window=%d n=%d  match=%s  max abs diff=%.3e"
              % (n_dom, window, n_obs, close, worst))
        # 2-D input must agree with the batched path.
        if not np.allclose(rolling_corr(x[0], window), fast[0], atol=1e-10):
            ok = False
            print("    2-D path disagrees with batched path")
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--selftest", action="store_true",
                    help="verify the optimized rolling correlation, then exit")
    ap.add_argument("--n-datasets", type=int, default=2000)
    ap.add_argument("--n-boot", type=int, default=5000)
    ap.add_argument("--n-boot-trend", type=int, default=1000)
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    n_data = 40 if args.quick else args.n_datasets
    n_boot = 200 if args.quick else args.n_boot
    n_boot_tr = 100 if args.quick else args.n_boot_trend
    grid = [0.0, 0.15] if args.quick else DELTA_GRID

    root = Path(__file__).resolve().parent.parent.parent
    outdir = root / "results" / "design-comparison"
    outdir.mkdir(parents=True, exist_ok=True)

    # The likelihood ratios are reported at LR_DELTA, so it must be simulated.
    assert LR_DELTA in grid, "LR_DELTA must be on the effect grid"
    assert 0.0 in grid, "the null must be on the effect grid"

    cands = candidates()
    # Structural sanity checks against the corrected layout.
    assert len(cands["C-A"]["b1"]) == 7, "C-A B1ex must be 7"
    assert len(cands["C-A"]["b3"]) == 6, "C-A B3ex must be 6"
    assert len(cands["C-B"]["b1"]) == 28 and len(cands["C-B"]["b3"]) == 24
    assert len(cands["C-C"]["b1"]) == 52 and len(cands["C-C"]["b3"]) == 36

    print("Design comparison (exploratory, pre-data-contact)")
    print("seed=%d  datasets=%d  boot=%d  boot_trend=%d" %
          (SEED, n_data, n_boot, n_boot_tr))
    for key, c in cands.items():
        if c["kind"] == "endpoint":
            print("  %s  %-52s n1=%d n3=%d D=%d" %
                  (key, c["label"], len(c["b1"]), len(c["b3"]), c["n_domains"]))
        else:
            nw = (len(c["keep"]) - c["window"] + 1) if c["kind"] == "trend" else len(c["keep"])
            print("  %s  %-52s n=%d windows=%s D=%d" %
                  (key, c["label"], len(c["keep"]),
                   nw if c["kind"] == "trend" else "n/a", c["n_domains"]))
    print("")

    t0 = time.time()
    ss = np.random.SeedSequence(SEED).spawn(12)
    rows: list[dict] = []
    per_cand: dict[str, list[dict]] = {}

    for ci, (key, cand) in enumerate(cands.items()):
        rng = np.random.default_rng(ss[ci])
        reps = n_boot if cand["kind"] == "endpoint" else n_boot_tr
        curve = []
        for d in grid:
            t1 = time.time()
            r = run_condition(rng, cand, d, n_data, reps)
            curve.append({"candidate": key, "true_delta_rho": d,
                          "power": r["power"], "se": r["se"],
                          "mean_stat": r["mean_stat"]})
            print("  %s delta=%.2f power=%.3f (se %.3f)  [%.0fs]" %
                  (key, d, r["power"], r["se"], time.time() - t1))
        per_cand[key] = curve
        rows.extend(curve)

    # ---------------- true size, per candidate ----------------
    #
    # fpr_at_zero conflates two different things: the test's actual SIZE, and
    # how much crisis contamination the design admits. Re-running each
    # candidate at delta=0 with the crisis elevation switched off separates
    # them. Without this split, a design is penalised on the "calibration" axis
    # for a contamination problem that has nothing to do with its inference.
    print("True size (crisis elevation OFF) per candidate")
    true_size: dict[str, float] = {}
    for ci, (key, cand) in enumerate(cands.items()):
        rng = np.random.default_rng(ss[9].spawn(len(cands))[ci])
        reps = n_boot if cand["kind"] == "endpoint" else n_boot_tr
        r = run_condition(rng, cand, 0.0, n_data, reps, crisis_boost=0.0)
        true_size[key] = r["power"]
        print("  %s true size=%.3f (se %.3f)" % (key, r["power"], r["se"]))

    # ---------------- summary per candidate ----------------
    summary_rows = []
    for key, cand in cands.items():
        curve = per_cand[key]
        by_d = {r["true_delta_rho"]: r["power"] for r in curve}
        p0 = by_d[0.0]
        p15 = by_d.get(LR_DELTA)
        mde = interpolate_mde([{"true_delta_rho": r["true_delta_rho"],
                                "power": r["power"]} for r in curve], "power")
        lr_conf = (p15 / p0) if p0 > 0 else float("inf")
        lr_disc = (1 - p15) / (1 - p0) if p0 < 1 else float("nan")
        summary_rows.append({
            "candidate": key,
            "label": cand["label"],
            "power_010": by_d.get(0.10),
            "power_015": p15,
            "power_020": by_d.get(0.20),
            "mde80": mde if mde is not None else "",
            "fpr_at_zero": p0,
            "true_size_no_crisis": true_size[key],
            "leak_contribution": p0 - true_size[key],
            "nominal_alpha": ALPHA,
            "lr_confirm_at_015": lr_conf,
            "lr_disconfirm_at_015": lr_disc,
            "meets_80_at_015": bool(p15 is not None and p15 >= TARGET_POWER),
        })
        print("  %s: power@0.15=%.3f  MDE80=%s  FPR=%.3f  LR+=%.2f  LR-=%.3f" %
              (key, p15, "none<=0.80" if mde is None else "%.3f" % mde,
               p0, lr_conf, lr_disc))

    # ---------------- C-F on its own effect axis ----------------
    print("C-F co-depletion, drift axis (co-movement axis above shows blindness)")
    a = WORLDS["annual2001"]
    n_obs_a = a["n_obs"]
    ramp = np.linspace(0.0, 1.0, n_obs_a)
    cf_rows = []
    rng = np.random.default_rng(ss[6])
    for m in ([0.0, 0.45] if args.quick else [0.0, 0.10, 0.20, 0.30, 0.45, 0.60]):
        r = run_condition(rng, cands["C-F"], 0.0, n_data, n_boot_tr,
                          drift=-m * ramp)
        from math import erf, sqrt as _s
        end_p = 0.5 * (1 + erf((-m) / _s(2))) if m else 0.5
        cf_rows.append({"drift_m": m,
                        "expected_end_count_of_8": 8 * (1 - end_p) if m else 4.0,
                        "power": r["power"], "se": r["se"],
                        "mean_count_level": r["mean_extra"]})
        print("  C-F drift m=%.2f  power=%.3f  mean count=%.2f" %
              (m, r["power"], r["mean_extra"]))

    # ---------------- diagnostics ----------------
    # D1 runs with the crisis elevation OFF. With it on, the leakage bias
    # (a separate effect, quantified elsewhere) would show up here and be
    # misread as a drift effect.
    print("D1. constant common drift, independent noise (crisis boost OFF)")
    rng = np.random.default_rng(ss[7])
    const = np.full(n_obs_a, -1.0)
    d1_base = run_condition(rng, cands["C-A"], 0.0, n_data, n_boot,
                            crisis_boost=0.0)
    d1_ca = run_condition(rng, cands["C-A"], 0.0, n_data, n_boot, drift=const,
                          crisis_boost=0.0)
    d1_cf_base = run_condition(rng, cands["C-F"], 0.0, n_data, n_boot_tr,
                               crisis_boost=0.0)
    d1_cf = run_condition(rng, cands["C-F"], 0.0, n_data, n_boot_tr,
                          drift=const, crisis_boost=0.0)
    print("  C-A no drift    : mean delta_rho=%+.4f  confirm rate=%.3f" %
          (d1_base["mean_stat"], d1_base["power"]))
    print("  C-A const drift : mean delta_rho=%+.4f  confirm rate=%.3f" %
          (d1_ca["mean_stat"], d1_ca["power"]))
    print("  C-F no drift    : mean count=%.2f/8  trend confirm=%.3f" %
          (d1_cf_base["mean_extra"], d1_cf_base["power"]))
    print("  C-F const drift : mean count=%.2f/8  trend confirm=%.3f" %
          (d1_cf["mean_extra"], d1_cf["power"]))

    # D2 runs BOTH families with the crisis elevation off, and reports the
    # REALIZED contrast rather than the nominal parameter. The AR(1) common
    # drift is persistent, and a persistent common component is partly absorbed
    # by within-block centring, so its realized effect is well below the value
    # solved for per-observation. Comparing power at equal NOMINAL values would
    # therefore compare two different effect sizes and overstate the deficit.
    print("D2. synchronized time-varying drift in the late block (crisis OFF)")
    rng = np.random.default_rng(ss[8])
    d2_rows = []
    for d in ([0.15] if args.quick else [0.10, 0.15, 0.20, 0.30]):
        rs = run_condition(rng, cands["C-A"], 0.0, n_data, n_boot, sync=d,
                           crisis_boost=0.0)
        re_ = run_condition(rng, cands["C-A"], d, n_data, n_boot,
                            crisis_boost=0.0)
        d2_rows.append({
            "nominal_parameter": d,
            "realized_delta_sync_drift": rs["mean_stat"],
            "realized_delta_equicorrelation": re_["mean_stat"],
            "power_sync_drift": rs["power"],
            "power_equicorrelation": re_["power"],
        })
        print("  nominal=%.2f | sync: realized=%.3f power=%.3f | equicorr: "
              "realized=%.3f power=%.3f" %
              (d, rs["mean_stat"], rs["power"], re_["mean_stat"], re_["power"]))

    # D1b. A shared drift that is NOT constant. D1 shows a constant common
    # drift is invisible, because differencing annihilates it. A drift with
    # curvature does NOT vanish under differencing: its first difference varies
    # over time and is shared across every domain, which is precisely a common
    # factor. Worse, the late block spans a wider index range than the early
    # one, so the shared component carries more variance there and the contrast
    # comes out positive with no change in genuine co-movement whatsoever.
    print("D1b. shared NON-constant drift (identical path, independent noise)")
    rng = np.random.default_rng(ss[10])
    t_norm = np.arange(n_obs_a) / (n_obs_a - 1)
    d1b_rows = []
    for c in ([0.0, 3.0] if args.quick else [0.0, 1.0, 2.0, 3.0, 5.0]):
        r = run_condition(rng, cands["C-A"], 0.0, n_data, n_boot,
                          drift=-c * t_norm ** 2, crisis_boost=0.0)
        d1b_rows.append({"curvature_c": c, "realized_delta_rho": r["mean_stat"],
                         "confirm_rate": r["power"], "se": r["se"]})
        print("  curvature=%.1f  realized delta_rho=%+.3f  confirm rate=%.3f" %
              (c, r["mean_stat"], r["power"]))

    elapsed = time.time() - t0

    write_csv(outdir / "power_curves.csv", rows)
    write_csv(outdir / "candidate_summary.csv", summary_rows)
    write_csv(outdir / "cf_drift_axis.csv", cf_rows)
    write_csv(outdir / "d2_sync_drift.csv", d2_rows)
    write_csv(outdir / "d1b_shared_curved_drift.csv", d1b_rows)

    any_meets = any(r["meets_80_at_015"] for r in summary_rows)
    summary = {
        "seed": SEED,
        "generated_by": "scripts/analysis/design_comparison.py",
        "quick_mode": bool(args.quick),
        "n_datasets": n_data,
        "n_bootstrap_endpoint": n_boot,
        "n_bootstrap_trend": n_boot_tr,
        "alpha_one_sided": ALPHA,
        "runtime_seconds": round(elapsed, 1),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "layout": {
            "note": "corrected layout supplied by the author 2026-07-28",
            "annual_diff_sample": "2001-2026 (26)",
            "B1ex": B1EX_ANNUAL, "B3ex": B3EX_ANNUAL,
            "crisis_set": sorted(CRISIS_YEARS),
        },
        "terminating_condition": {
            "requirement": "power >= 0.80 at delta_rho = 0.15",
            "any_candidate_meets_it": any_meets,
        },
        "candidate_summary": summary_rows,
        "power_curves": rows,
        "cf_drift_axis": cf_rows,
        "diagnostic_d1_constant_common_drift": {
            "drift_per_period_in_sd_units": -1.0,
            "crisis_boost": 0.0,
            "ca_mean_delta_rho_no_drift": d1_base["mean_stat"],
            "ca_mean_delta_rho_with_drift": d1_ca["mean_stat"],
            "ca_confirm_rate_no_drift": d1_base["power"],
            "ca_confirm_rate_with_drift": d1_ca["power"],
            "cf_mean_count_of_8_no_drift": d1_cf_base["mean_extra"],
            "cf_mean_count_of_8_with_drift": d1_cf["mean_extra"],
            "cf_trend_confirm_rate_no_drift": d1_cf_base["power"],
            "cf_trend_confirm_rate_with_drift": d1_cf["power"],
        },
        "diagnostic_d2_synchronized_drift": d2_rows,
        "diagnostic_d1b_shared_curved_drift": d1b_rows,
        "true_size_by_candidate": true_size,
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n",
                                         encoding="utf-8", newline="\n")

    print("")
    print("Any candidate reaching 80%% power at delta_rho=0.15: %s" % any_meets)
    print("elapsed: %.1f s" % elapsed)
    print("results in: %s" % outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
