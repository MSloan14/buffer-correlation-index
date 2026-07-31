#!/usr/bin/env python3
"""Study 1 chart pipeline. Runs on SYNTHETIC PLACEHOLDERS until the gate opens.

Built with the data gate closed so that tomorrow is fetch-and-render rather than
fetch-and-then-build-a-renderer. Every chart produced today is drawn from
`numpy` noise and is watermarked as such; nothing here has seen a real series.

Design rules, all of which outlive the placeholders:

  - **Up is always more buffer.** Series requiring inversion are inverted before
    plotting and the panel says so, because a reader who has to remember which
    axis is flipped will eventually forget.
  - **Crisis years are shaded, never removed.** 2008-09, 2020-21, 2026.
  - **No cross-domain statistic is computed or drawn.** The z-scored overlay is
    labelled "visual comparison only". The index test was withdrawn for reaching
    beyond what the data identifies; a chart that quietly reintroduces a
    cross-domain claim would undo that.
  - **Source and retrieval date on every panel.** While the gate is closed these
    read PLACEHOLDER, which is the point.

Usage:
    python scripts/analysis/study1_charts.py              # synthetic placeholders
    python scripts/analysis/study1_charts.py --real       # refuses until gate open
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GATE_FILE = REPO_ROOT / "data" / ".gate-open"
OUTDIR = REPO_ROOT / "results" / "study1" / "placeholder-charts"

SEED = 2026073102

CRISIS_SPANS = [(2008, 2009), (2020, 2021), (2026, 2026)]
ROLLING_SLOPE_WINDOW = 10

# Muted, colour-blind-safe. Deliberately unsaturated: these are descriptive
# panels, and a palette that shouts implies a finding the chart does not carry.
INK = "#2b2b2b"
LINE = "#3c6e8f"
SHADE = "#c8c8c8"
ACCENT = "#a8562c"

DOMAINS = [
    (1, "Strategic reserve", "SPR stocks (mn bbl)", False),
    (2, "Financial", "Credit-to-GDP gap (inverted)", True),
    (3, "Fiscal", "Debt held by public, % GDP (inverted)", True),
    (4, "Corporate", "Net debt / EBITDA (inverted)", True),
    (5, "Household", "Personal saving rate (%)", False),
    (6, "Health capacity", "(domain 6 unresolved)", False),
    (7, "Social / associational", "Union membership rate (%)", False),
    (8, "Food", "Grain stocks-to-use ratio", False),
]


def synthetic_panel(rng: np.random.Generator, years: np.ndarray) -> np.ndarray:
    """A placeholder series. Shape is arbitrary and carries no claim."""
    t = (years - years[0]) / max(len(years) - 1, 1)
    level = 100.0 - 30.0 * t + 8.0 * np.sin(2 * np.pi * t * 1.5)
    for lo, hi in CRISIS_SPANS:
        mask = (years >= lo) & (years <= hi + 2)
        level = level - 6.0 * mask
    return level + rng.standard_normal(len(years)) * 2.0


def rolling_slope(y: np.ndarray, window: int = ROLLING_SLOPE_WINDOW) -> np.ndarray:
    """Least-squares slope over a trailing window; NaN until the window fills."""
    out = np.full(len(y), np.nan)
    x = np.arange(window, dtype=float)
    xc = x - x.mean()
    denom = (xc ** 2).sum()
    for i in range(window - 1, len(y)):
        seg = y[i - window + 1:i + 1]
        out[i] = ((seg - seg.mean()) * xc).sum() / denom
    return out


def make_charts(outdir: Path, placeholder: bool = True) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib unavailable; skipping charts")
        return False

    outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    years = np.arange(1970, 2027)
    stamp = "PLACEHOLDER - SYNTHETIC DATA" if placeholder else "(real data)"

    panels = {}
    for num, name, ylabel, inverted in DOMAINS:
        y = synthetic_panel(rng, years)
        panels[num] = y

        fig, ax = plt.subplots(figsize=(9, 4.2))
        for lo, hi in CRISIS_SPANS:
            ax.axvspan(lo - 0.5, hi + 0.5, color=SHADE, alpha=0.55, lw=0)
        ax.plot(years, y, color=LINE, lw=1.8)

        inset = ax.inset_axes([0.62, 0.08, 0.35, 0.28])
        inset.plot(years, rolling_slope(y), color=ACCENT, lw=1.2)
        inset.axhline(0, color=INK, lw=0.6)
        inset.set_title("%d-yr slope" % ROLLING_SLOPE_WINDOW, fontsize=7, color=INK)
        inset.tick_params(labelsize=6)

        title = "Domain %d - %s" % (num, name)
        if inverted:
            title += "   [INVERTED: up = more buffer]"
        ax.set_title(title, fontsize=11, color=INK)
        ax.set_ylabel(ylabel, fontsize=9, color=INK)
        ax.set_xlabel("Source: PLACEHOLDER | Retrieved: PLACEHOLDER", fontsize=8)
        ax.grid(alpha=0.25)
        fig.text(0.5, 0.5, stamp, fontsize=26, color="#d9534f", alpha=0.16,
                 ha="center", va="center", rotation=18, weight="bold")
        fig.tight_layout()
        fig.savefig(outdir / ("domain_%d.png" % num), dpi=140)
        plt.close(fig)

    # Overlay. Explicitly NOT a statistic -- see the module docstring.
    fig, ax = plt.subplots(figsize=(9.5, 5))
    for lo, hi in CRISIS_SPANS:
        ax.axvspan(lo - 0.5, hi + 0.5, color=SHADE, alpha=0.55, lw=0)
    for num, name, _, _ in DOMAINS:
        y = panels[num]
        z = (y - y.mean()) / y.std(ddof=1)
        ax.plot(years, z, lw=1.2, alpha=0.75, label="%d %s" % (num, name))
    ax.set_title("All domains, z-scored - VISUAL COMPARISON ONLY, no statistic computed",
                 fontsize=10, color=INK)
    ax.set_ylabel("z-score (up = more buffer)", fontsize=9)
    ax.set_xlabel("Source: PLACEHOLDER | Retrieved: PLACEHOLDER", fontsize=8)
    ax.legend(fontsize=7, ncol=4, loc="lower left")
    ax.grid(alpha=0.25)
    fig.text(0.5, 0.5, stamp, fontsize=30, color="#d9534f", alpha=0.14,
             ha="center", va="center", rotation=18, weight="bold")
    fig.tight_layout()
    fig.savefig(outdir / "overlay_zscored.png", dpi=140)
    plt.close(fig)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--real", action="store_true",
                    help="render from real data (requires the gate to be open)")
    args = ap.parse_args()

    if args.real:
        if not GATE_FILE.is_file():
            print("REFUSING: --real requires data/.gate-open, which does not exist.")
            print("Nothing was read and nothing was rendered.")
            return 1
        print("Gate is open, but the real-data path is deliberately unwritten;")
        print("it should be built against actual series at that point.")
        return 1

    print("Study 1 chart scaffolding - SYNTHETIC PLACEHOLDERS")
    print("seed=%d  domains=%d  years=1970-2026" % (SEED, len(DOMAINS)))
    ok = make_charts(OUTDIR, placeholder=True)
    print("charts written: %s" % ok)
    print("output: %s" % OUTDIR)
    print("")
    print("Every panel is watermarked SYNTHETIC and stamped Source/Retrieved =")
    print("PLACEHOLDER. No real series has been read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
