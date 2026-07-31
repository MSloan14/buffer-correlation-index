#!/usr/bin/env python3
"""Synthetic identification check for the ratchet criterion.

Run BEFORE the ratchet specification is frozen, and before any contact with real
data. Everything here is synthetic. No real series is read, fetched, or opened.

The question this answers is NOT "does the criterion have power". It is: **can
the criterion tell a ratchet apart from an ordinary secular decline?** The index
test was withdrawn because it could not distinguish rising co-movement from a
shared curved trend. Asking the same question of the replacement, before
freezing it, is the whole point.

Worlds simulated:
    R-flat   ratchet on a flat baseline: episodes recover partially, then plateau
    R-decl   ratchet on a mildly declining baseline
    M-flat   mean reversion on a flat baseline: episodes recover fully
    M-decl   mean reversion on a mildly declining baseline
    S-lin    pure secular decline, linear, no episode structure beyond noise
    S-acc    pure secular decline, ACCELERATING

S-acc is not in the original brief and is the most important row. A linear
decline is easy to render uninformative. A decline whose slope steepens over time
can rebuild early and fail to rebuild late for reasons that have nothing to do
with ratcheting -- which is exactly the failure mode that killed the index test.
If the criterion cannot separate R from S-acc, the ratchet question is not
testable by this route either.

Usage:
    python scripts/analysis/ratchet_identification.py            # full
    python scripts/analysis/ratchet_identification.py --quick    # smoke test
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
from power_sim import write_csv  # noqa: E402

SEED = 2026073101

# --------------------------------------------------------------------------
# Criterion parameters -- the three tunables named in the draft specification
# --------------------------------------------------------------------------

SIGMA_THRESHOLD = 1.5      # peak-to-trough drawdown, in sd of YoY changes
TROUGH_WITHIN = 3          # years from peak to trough
REBUILD_FRACTION = 0.90    # recovery to this fraction of the pre-episode peak
REBUILD_WINDOW = 7         # years after the trough

ERA_SPLIT = 2000           # trough year < 2000 is early, >= 2000 is late

FIRST_YEAR = 1950
LAST_YEAR = 2026
N_YEARS = LAST_YEAR - FIRST_YEAR + 1

BASE_LEVEL = 100.0
NOISE_SD = 2.0
MILD_DECLINE_PER_YEAR = 0.25     # units per year on a base of 100

# --------------------------------------------------------------------------
# Episode detection and scoring -- a direct transcription of the draft spec
# --------------------------------------------------------------------------


def detect_episodes(x: np.ndarray, sigma_threshold: float = SIGMA_THRESHOLD,
                    trough_within: int = TROUGH_WITHIN) -> list[tuple[int, int]]:
    """Return merged (peak_index, trough_index) pairs.

    Spec section 4: a drawdown of at least sigma_threshold standard deviations
    of the series' own year-over-year changes, with the trough within
    trough_within years of the peak. Overlapping episodes are merged, taking the
    earliest peak and the lowest trough.
    """
    diffs = np.diff(x)
    sigma = diffs.std(ddof=1)
    if sigma <= 0:
        return []
    threshold = sigma_threshold * sigma

    candidates = []
    for peak in range(len(x) - 1):
        best_drop, best_trough = 0.0, None
        for h in range(1, trough_within + 1):
            t = peak + h
            if t >= len(x):
                break
            drop = x[peak] - x[t]
            if drop >= threshold and drop > best_drop:
                best_drop, best_trough = drop, t
        if best_trough is not None:
            candidates.append((peak, best_trough))

    if not candidates:
        return []

    # Merge overlapping windows: earliest peak, lowest trough.
    merged = []
    cur_peak, cur_trough = candidates[0]
    for peak, trough in candidates[1:]:
        if peak <= cur_trough:                       # windows overlap
            if x[trough] < x[cur_trough]:
                cur_trough = trough
        else:
            merged.append((cur_peak, cur_trough))
            cur_peak, cur_trough = peak, trough
    merged.append((cur_peak, cur_trough))
    return merged


def score_episode(x: np.ndarray, peak: int, trough: int,
                  rebuild_fraction: float = REBUILD_FRACTION,
                  rebuild_window: int = REBUILD_WINDOW) -> str:
    """'rebuilt', 'not_rebuilt', or 'censored'. Spec section 5."""
    end = trough + rebuild_window
    if end >= len(x):
        return "censored"
    target = rebuild_fraction * x[peak]
    return "rebuilt" if x[trough + 1:end + 1].max() >= target else "not_rebuilt"


def classify_series(x: np.ndarray, years: np.ndarray, **kw) -> dict:
    """Score every episode, then apply the section 6 within-domain comparison."""
    eps = detect_episodes(x, kw.get("sigma_threshold", SIGMA_THRESHOLD),
                          kw.get("trough_within", TROUGH_WITHIN))
    rows = []
    for peak, trough in eps:
        rows.append({
            "peak": peak, "trough": trough,
            "era": "early" if years[trough] < ERA_SPLIT else "late",
            "score": score_episode(x, peak, trough,
                                   kw.get("rebuild_fraction", REBUILD_FRACTION),
                                   kw.get("rebuild_window", REBUILD_WINDOW)),
        })

    scored = [r for r in rows if r["score"] in ("rebuilt", "not_rebuilt")]
    early = [r for r in scored if r["era"] == "early"]
    late = [r for r in scored if r["era"] == "late"]

    def rate(group):
        return None if not group else sum(r["score"] == "rebuilt" for r in group) / len(group)

    e_rate, l_rate = rate(early), rate(late)

    # Section 6. A domain that never rebuilds in ANY era is consistent with
    # secular decline and is uninformative for H-R -- NOT support for it.
    if not early or not late or e_rate is None or l_rate is None:
        verdict = "insufficient"
    else:
        e_val, l_val = float(e_rate), float(l_rate)
        if e_val == 0.0 and l_val == 0.0:
            verdict = "uninformative"
        elif e_val > 0.5 and l_val == 0.0:
            verdict = "ratchet_signature"
        elif l_val > 0.5:
            verdict = "against_HR"
        else:
            verdict = "mixed"

    return {
        "n_episodes": len(rows),
        "n_scored": len(scored),
        "n_censored": sum(r["score"] == "censored" for r in rows),
        "early_rebuild_rate": e_rate,
        "late_rebuild_rate": l_rate,
        "verdict": verdict,
        "episodes": rows,
    }


# --------------------------------------------------------------------------
# Worlds
# --------------------------------------------------------------------------


def _episode_times(rng: np.random.Generator) -> list[int]:
    """Injected episode onsets, roughly one per decade, jittered."""
    onsets = []
    for decade_start in range(5, N_YEARS - 12, 10):
        onsets.append(decade_start + int(rng.integers(0, 7)))
    return onsets


def simulate_series(rng: np.random.Generator, world: str) -> tuple[np.ndarray, list[int]]:
    """Return (series, injected_trough_indices). Injected list is empty for S.

    Ratchet severity is parameterised directly as the PERMANENT step-down after
    each episode, expressed as a fraction of the pre-episode level. That is the
    quantity the rebuild criterion actually keys on: a step smaller than
    (1 - REBUILD_FRACTION) leaves the series above the rebuild bar and is
    invisible to the criterion by construction, regardless of how deep the
    drawdown was. Sweeping it is the only way to say what the criterion can see.
    """
    t = np.arange(N_YEARS, dtype=float)
    injected: list[int] = []

    if world.startswith("S"):
        if world == "S-lin":
            level = BASE_LEVEL - 0.45 * t
        else:                                     # S-acc: accelerating decline
            level = BASE_LEVEL - 0.010 * t ** 2
        x = level + rng.standard_normal(N_YEARS) * NOISE_SD
        return x, injected

    step_pct = RATCHET_STEPS.get(world, 0.0)      # 0.0 for the M worlds
    decline = MILD_DECLINE_PER_YEAR if world.endswith("decl") else 0.0

    x = np.full(N_YEARS, BASE_LEVEL) - decline * t
    for onset in _episode_times(rng):
        if onset + 2 >= N_YEARS:
            break
        pre_level = x[onset]
        depth = pre_level * float(rng.uniform(0.14, 0.20))   # clearly >= 1.5 sigma
        fall = int(rng.integers(1, 3))
        trough = min(onset + fall, N_YEARS - 1)
        plateau = pre_level * (1.0 - step_pct)               # permanent level after
        for i in range(onset + 1, trough + 1):
            x[i:] = pre_level - depth * ((i - onset) / max(fall, 1))
        rec_years = int(rng.integers(3, 6))
        bottom = x[trough]
        for j in range(1, rec_years + 1):
            i = trough + j
            if i >= N_YEARS:
                break
            x[i:] = bottom + (plateau - bottom) * (j / rec_years)
        injected.append(trough)

    x = x - decline * 0.0 + rng.standard_normal(N_YEARS) * NOISE_SD
    return x, injected


# Permanent step-down per episode, as a fraction of the pre-episode level.
# The rebuild bar is 1 - REBUILD_FRACTION = 0.10, so R-05 sits below what the
# criterion can detect and R-20 well above it. That is the point of the sweep.
RATCHET_STEPS = {
    "R-05": 0.05, "R-10": 0.10, "R-15": 0.15, "R-20": 0.20, "R-decl": 0.15,
}

WORLDS = ["R-05", "R-10", "R-15", "R-20", "R-decl",
          "M-flat", "M-decl", "S-lin", "S-acc"]


# --------------------------------------------------------------------------
# Experiments
# --------------------------------------------------------------------------


def run_world(rng: np.random.Generator, world: str, n_series: int, **kw) -> dict:
    years = np.arange(FIRST_YEAR, LAST_YEAR + 1)
    verdicts: dict[str, int] = {}
    n_eps, n_scored, n_cens = [], [], []
    hits, misses, false_alarms = 0, 0, 0
    rebuilt_scored, total_scored = 0, 0

    for _ in range(n_series):
        x, injected = simulate_series(rng, world)
        res = classify_series(x, years, **kw)
        verdicts[res["verdict"]] = verdicts.get(res["verdict"], 0) + 1
        n_eps.append(res["n_episodes"])
        n_scored.append(res["n_scored"])
        n_cens.append(res["n_censored"])
        for r in res["episodes"]:
            if r["score"] in ("rebuilt", "not_rebuilt"):
                total_scored += 1
                rebuilt_scored += r["score"] == "rebuilt"

        # Detection accuracy, only meaningful where episodes were injected.
        if injected:
            detected = [r["trough"] for r in res["episodes"]]
            matched = set()
            for inj in injected:
                near = [d for d in detected if abs(d - inj) <= 2 and d not in matched]
                if near:
                    matched.add(near[0])
                    hits += 1
                else:
                    misses += 1
            false_alarms += len([d for d in detected if d not in matched])

    n = float(n_series)
    out = {
        "world": world,
        "n_series": n_series,
        "mean_episodes_detected": float(np.mean(n_eps)),
        "mean_scored": float(np.mean(n_scored)),
        "mean_censored": float(np.mean(n_cens)),
        "rebuild_rate_all_scored": (rebuilt_scored / total_scored) if total_scored else None,
        "pct_ratchet_signature": 100 * verdicts.get("ratchet_signature", 0) / n,
        "pct_uninformative": 100 * verdicts.get("uninformative", 0) / n,
        "pct_against_HR": 100 * verdicts.get("against_HR", 0) / n,
        "pct_mixed": 100 * verdicts.get("mixed", 0) / n,
        "pct_insufficient": 100 * verdicts.get("insufficient", 0) / n,
    }
    if injected:
        out["detection_hit_rate"] = hits / max(hits + misses, 1)
        out["false_alarms_per_series"] = false_alarms / n
    else:
        out["detection_hit_rate"] = None
        out["false_alarms_per_series"] = float(np.mean(n_eps))
    return out


def sensitivity_grid(rng: np.random.Generator, n_series: int) -> list[dict]:
    rows = []
    for sig in (1.0, 1.5, 2.0):
        for frac in (0.80, 0.90, 0.95):
            for win in (5, 7, 10):
                kw = dict(sigma_threshold=sig, rebuild_fraction=frac,
                          rebuild_window=win)
                cell = {"sigma": sig, "rebuild_fraction": frac,
                        "rebuild_window": win}
                for world in ("R-15", "M-flat", "S-acc"):
                    r = run_world(rng, world, n_series, **kw)
                    cell["%s_ratchet_pct" % world] = r["pct_ratchet_signature"]
                    cell["%s_uninformative_pct" % world] = r["pct_uninformative"]
                rows.append(cell)
                print("  sigma=%.1f frac=%.2f win=%d | R-15 %.1f%% | "
                      "M %.1f%% | S-acc %.1f%% | separation %+.1f"
                      % (sig, frac, win, cell["R-15_ratchet_pct"],
                         cell["M-flat_ratchet_pct"], cell["S-acc_ratchet_pct"],
                         cell["R-15_ratchet_pct"] - cell["S-acc_ratchet_pct"]))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--n-series", type=int, default=2000)
    args = ap.parse_args()
    n_series = 60 if args.quick else args.n_series
    n_grid = 25 if args.quick else 400

    root = Path(__file__).resolve().parent.parent.parent
    outdir = root / "results" / "ratchet-identification"
    outdir.mkdir(parents=True, exist_ok=True)

    print("Ratchet criterion - synthetic identification check")
    print("seed=%d  series/world=%d  years=%d-%d  era split=%d"
          % (SEED, n_series, FIRST_YEAR, LAST_YEAR, ERA_SPLIT))
    print("criterion: %.1f sigma drawdown, trough within %d yr, rebuild to "
          "%.0f%% within %d yr" % (SIGMA_THRESHOLD, TROUGH_WITHIN,
                                   100 * REBUILD_FRACTION, REBUILD_WINDOW))
    print("")

    t0 = time.time()
    ss = np.random.SeedSequence(SEED).spawn(2)

    print("Main worlds")
    rng = np.random.default_rng(ss[0])
    main_rows = []
    for world in WORLDS:
        r = run_world(rng, world, n_series)
        main_rows.append(r)
        print("  %-7s eps=%.1f scored=%.1f cens=%.1f | ratchet %.1f%% "
              "uninf %.1f%% against %.1f%% mixed %.1f%%"
              % (world, r["mean_episodes_detected"], r["mean_scored"],
                 r["mean_censored"], r["pct_ratchet_signature"],
                 r["pct_uninformative"], r["pct_against_HR"], r["pct_mixed"]))

    print("")
    print("Sensitivity grid (R-15 / M-flat / S-acc)")
    rng = np.random.default_rng(ss[1])
    grid_rows = sensitivity_grid(rng, n_grid)

    elapsed = time.time() - t0

    by_world = {r["world"]: r for r in main_rows}
    # Take the BEST-performing ratchet severity, which is the most generous
    # reading available to the criterion. If it cannot separate even there, it
    # cannot separate anywhere.
    r_worlds = {k: v for k, v in by_world.items() if k.startswith("R-")}
    best_r = max(r_worlds.values(), key=lambda v: v["pct_ratchet_signature"])
    r_sig = best_r["pct_ratchet_signature"]
    s_acc_sig = by_world["S-acc"]["pct_ratchet_signature"]
    s_lin_uninf = by_world["S-lin"]["pct_uninformative"]
    discriminates = (r_sig - s_acc_sig) >= 20.0
    # A shallow but genuine ratchet that the criterion reads as evidence
    # AGAINST the hypothesis is a false negative that actively misleads.
    shallow_against = by_world["R-05"]["pct_against_HR"]
    deep_uninformative = by_world["R-20"]["pct_uninformative"]

    write_csv(outdir / "worlds.csv", main_rows)
    write_csv(outdir / "sensitivity_grid.csv", grid_rows)
    summary = {
        "seed": SEED,
        "generated_by": "scripts/analysis/ratchet_identification.py",
        "quick_mode": bool(args.quick),
        "n_series_per_world": n_series,
        "n_series_per_grid_cell": n_grid,
        "runtime_seconds": round(elapsed, 1),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "criterion": {
            "sigma_threshold": SIGMA_THRESHOLD,
            "trough_within_years": TROUGH_WITHIN,
            "rebuild_fraction": REBUILD_FRACTION,
            "rebuild_window_years": REBUILD_WINDOW,
            "era_split": ERA_SPLIT,
            "first_year": FIRST_YEAR,
            "last_year": LAST_YEAR,
        },
        "headline": {
            "best_ratchet_world": best_r["world"],
            "ratchet_signature_pct_best_R": r_sig,
            "ratchet_signature_pct_S_acc": s_acc_sig,
            "uninformative_pct_S_lin": s_lin_uninf,
            "separation_bestR_minus_Sacc": r_sig - s_acc_sig,
            "criterion_discriminates": bool(discriminates),
            "pct_shallow_ratchet_read_as_against_HR": shallow_against,
            "pct_deep_ratchet_read_as_uninformative": deep_uninformative,
        },
        "worlds": main_rows,
        "sensitivity_grid": grid_rows,
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n",
                                         encoding="utf-8", newline="\n")

    print("")
    print("HEADLINE")
    print("  best ratchet world          : %s at %.1f%%" % (best_r["world"], r_sig))
    print("  ratchet signature in S-acc  : %.1f%%   <- FALSE POSITIVES" % s_acc_sig)
    print("  separation (best R - S-acc) : %+.1f points" % (r_sig - s_acc_sig))
    print("  S-lin rendered uninformative: %.1f%%" % s_lin_uninf)
    print("  shallow ratchet read as AGAINST H-R : %.1f%%" % shallow_against)
    print("  deep ratchet read as uninformative  : %.1f%%" % deep_uninformative)
    print("  CRITERION DISCRIMINATES     : %s" % discriminates)
    print("")
    print("elapsed: %.1f s" % elapsed)
    print("results in: %s" % outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
