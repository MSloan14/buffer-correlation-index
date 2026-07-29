# Buffer-Correlation Index — pre-registration

A pre-registered test of the hypothesis that **US collective buffers have been
depleting in increasingly correlated fashion over 2000–2026**, together with a
slate of dated, scoreable predictions that divide that thesis from an
adaptive-resilience null.

The point of this repository is that the specification and the predictions were
frozen and published **before** the data that will test them was touched. That
ordering is the whole warrant. Everything else here exists to make it checkable.

---

## The one fact that matters most

**No historical joint series data had been examined at the time of this commit.**
No component series was fetched, opened, or inspected. Every number in the power
simulation is **synthetic** — generated from a specified data-generating process
to measure what the design can detect, not what the world contains.

The specification's own blindness disclosure (Spec v0.2 §2) is franker than this
summary and should be read instead of it: perfect blindness is not claimed, the
residual contamination is named, and the mitigations are stated.

## Binding status — read this before citing anything

The two frozen documents do **not** have the same standing.

### Prediction Slate v1.1 — binding

[`prereg/slate-v1.1.md`](prereg/slate-v1.1.md) **is the binding
pre-registration.** Its predictions, conditional probabilities, resolution dates
and resolution feeds are fixed as of this commit.

**P5's resolution window opened 2026-07-28** and runs to 2026-12-31.

### Index Spec v0.2 — frozen, but superseded pending design review

[`prereg/spec-v0.2.md`](prereg/spec-v0.2.md) is frozen, and it is **superseded
pending a pre-data design review.**

A synthetic power simulation — run before any contact with real data — found the
design **severely underpowered**. Against a true rise in mean pairwise
correlation of 0.15:

| | Result |
|---|---|
| P(CONFIRM) when the effect is real | **0.287** |
| P(CONFIRM) when there is **no effect at all** | **0.124** |
| Minimum detectable effect at 80% power | **Δρ ≈ 0.52** |
| **Likelihood ratio for a non-confirmation** | **0.81** |

That last row is the one that matters. A disconfirmation from this design shifts
the odds against the hypothesis by about a fifth — which is to say, almost not at
all. The instrument is close to incapable of producing evidence in either
direction, and pre-committing to it buys correspondingly little.

A revised specification **v0.3**, or a documented finding that the claim is **not
testable at adequate power with available annual series**, will follow. Either
outcome will be published here.

The design review also found a confounder that no amount of extra data would fix:
a shared depletion path with **curvature** is read by this statistic as rising
co-movement, even when genuine co-movement is unchanged. See
[`REVIEWER-NOTES.md`](REVIEWER-NOTES.md), item 9.

### v0.1 and v1.0 — provenance only

[`prereg/spec-v0.1.md`](prereg/spec-v0.1.md) and
[`prereg/slate-v1.0.md`](prereg/slate-v1.0.md) are included **solely as
provenance** for a single pre-timestamp revision cycle. Neither was ever
externally timestamped. They are here so the v0.1→v0.2 and v1.0→v1.1 deltas are
auditable rather than asserted; each superseding document carries a change log
tagging every change as thesis-helping, null-helping, or neutral-precision.

### P6's instrument is pinned

P6 measures the **quarterly companion as defined in Spec v0.2 §7 (S8)** —
the quarterly-native subset of strategic reserve, financial, fiscal debt/GDP and
household, 6 pairs, 40-quarter trailing windows.

**That instrument remains pinned regardless of any later revision to the
specification**, including v0.3. The slate is the binding document; a prediction
whose measuring instrument could be redefined after the fact would not be a
prediction.

## The disconfirmation commitment

Quoted verbatim from Spec v0.2 §0:

> *If the pre-specified analysis returns flat or domain-idiosyncratic
> cross-domain covariance over 2000–2026, the correlated-drain claim is withdrawn
> from the framework. No hedging into "not yet measurable."*

Operationally: **anything short of all four CONFIRM criteria is a
disconfirmation.** There is no intermediate verdict, and no "underpowered"
escape hatch — the withdrawal happens whether the record shows "flat and
well-powered" or "flat and unpowered."

The branch language for both outcomes is already written, blind, in
[`phase-4-precommitment.md`](phase-4-precommitment.md).

## Contents

| Path | What it is |
|---|---|
| [`prereg/`](prereg/) | The frozen documents. Append-only: never edited, only superseded by a new dated version. |
| [`REVIEWER-NOTES.md`](REVIEWER-NOTES.md) | Known limitations, disclosed before data contact. **Not part of the pre-registration.** Includes a correction notice for a defect found in the simulation itself. |
| [`results/power-simulation/`](results/power-simulation/) | What the frozen design can and cannot detect. Synthetic data only. |
| [`results/design-comparison/`](results/design-comparison/) | Six candidate designs compared, to inform whether a revision can reach adequate power. Exploratory; changes nothing frozen. |
| [`phase-4-precommitment.md`](phase-4-precommitment.md) | Results-blind branch language for the write-up. **Explicitly not part of the pre-registration**; a self-binding writing constraint, drafted before the result exists. |
| [`DATA_TERMS.md`](DATA_TERMS.md) | What may be committed, per source. |
| [`CHECKSUMS.sha256`](CHECKSUMS.sha256) | SHA-256 of every file in `prereg/`. Verify with `sha256sum -c` or [`scripts/checksums.py`](scripts/checksums.py). |
| [`scripts/`](scripts/) | All analysis code. Fetch scripts will be committed alongside the data when Phase 3 runs. |

Data and code are committed deliberately. An audit trail that omits its inputs
is not an audit trail. The exception is proprietary data that cannot be
redistributed; [`DATA_TERMS.md`](DATA_TERMS.md) states what is committed instead
and what that costs.

## Licensing

| What | Licence |
|---|---|
| Code — [`scripts/`](scripts/) and any other source | **MIT**, see [`LICENSE`](LICENSE) |
| Prose and outputs — [`prereg/`](prereg/), [`results/`](results/), documentation | **CC BY 4.0**, see [`LICENSE-DOCS`](LICENSE-DOCS) |

Third-party data under `data/` is covered by **neither**; each series carries its
own source's terms.

## How to verify the timestamp

The claim is: *the specification and the slate were fixed before the data was
touched.* Three ways to check, weakest first.

1. **Commit dates.** `git log --format='%H %ad %s' --date=iso`. Weakest form:
   git commit dates are supplied by the committer's machine and can be set to
   anything. Listed only for completeness — **this proves nothing on its own.**
2. **The GitHub release.** The tag `prereg-v1` and its release are timestamped by
   GitHub, a third party with no stake in the outcome, and the release body
   restates the binding status.
3. **The OSF registration.** *(placeholder — URL and DOI to be inserted)*
   Open-Ended Registration at [osf.io](https://osf.io), containing the same five
   documents. **OSF registrations are immutable**, which makes this the strongest
   link in the chain: unlike a git history, it cannot be rewritten by the author.

   > **OSF URL: _to be added_**
   > **OSF DOI: _to be added_**

To check the frozen documents are unaltered since the freeze:

```
python scripts/checksums.py verify
```

## Score us

The slate is public, dated, and third-party timestamped. Every prediction carries
an exactly-defined YES event, a resolution date, a resolution feed, and both
conditional probabilities — P(YES | thesis) and P(YES | null) — so the gap
between them can be scored against us rather than argued about.

Resolutions are adjudicated strictly against the written definitions.
Annotations are permitted; redefinitions are not. Disputes go to an adversarial
review, never to the pro-case.

**The standing offer, which prints with the slate wherever it appears: score us.**
