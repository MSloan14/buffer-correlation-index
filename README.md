# Buffer depletion — pre-registration, chartbook, and prediction slate

**Stated prior.** The author expected to find that collective buffers — strategic
reserves, fiscal room, hospital capacity, associational capacity — are depleted,
and believes buffer-holding is systematically undervalued. That prior motivated
the project and is not neutral. The methods here exist to make the work usable
by a reader who holds the opposite prior: criteria frozen before data contact,
failures published rather than buried, findings checked by adversarial
verification that has already overturned one of them, and the competing
efficiency explanation printed beside every chart rather than in a footnote.
Judge the process; the conclusions are downstream of it.

---

## What this is

Three components, with three different standings. Conflating them would be the
easiest way to misread this repository.

| | Component | Status |
|---|---|---|
| **Study 1** | Descriptive chartbook — are buffers thin, thinning, and thinning faster? | **Exploratory**, and labelled as such throughout |
| **Study 2** | The ratchet question — after stress episodes, do buffers rebuild or step permanently lower? | **Criterion failed its identification check.** Not frozen, not running |
| **Study 3** | The frozen prediction slate | **Public, binding, timestamped** |

And one component that has been removed:

| | Component | Status |
|---|---|---|
| ~~Index test~~ | Cross-domain buffer-correlation index | **WITHDRAWN as not identified** |

## The index test is withdrawn

The pre-registered correlated-drain test has been withdrawn. Not as
underpowered — though it was — but as **not identified**: the statistic cannot
distinguish the effect it was built to detect from an artifact it generates
itself.

The headline statistic differences each series to strip out shared trend. That
works only if the shared trend is linear. A shared depletion path with
**curvature** survives differencing, and is read as rising co-movement. In
simulation, identical depletion paths across every domain with fully independent
noise and no rise in genuine co-movement produced Δρ of **+0.358** and confirmed
**33%** of the time.

The confound is a property of the differencing family, so no candidate design
examined escapes it. More data estimates the confounded quantity more precisely
without separating it.

The withdrawal is in [`results/withdrawal-note.md`](results/withdrawal-note.md).
The commitment it honours, quoted verbatim from Index Spec v0.2 §0:

> *If the pre-specified analysis returns flat or domain-idiosyncratic
> cross-domain covariance over 2000–2026, the correlated-drain claim is
> withdrawn from the framework. No hedging into "not yet measurable."*

**The data was never fetched.** The withdrawal rests entirely on synthetic
evidence about the instrument, generated before the gate opened. No result,
favourable or otherwise, informed it.

## Study 2 failed its identification check, and is not running

The ratchet question survived the index withdrawal because it does not depend on
cross-domain covariance. A criterion was drafted and — before freezing — tested
against synthetic worlds.

**It does not discriminate.** Pure accelerating decline, containing no ratchet at
all, produced the ratchet signature **15.6%** of the time against **9.1%** for
the best genuine ratchet world. The separation is **negative**. No cell in a
27-point parameter grid achieved useful separation; 22 of 27 were inverted.

Two further failures: a genuine ratchet shallower than the rebuild bar is
reported as evidence *against* the hypothesis 96.9% of the time, and the
standard control for secular decline makes a *consistent* ratchet — which is
what the hypothesis actually claims — score uninformative.

The draft specification committed in advance to publishing this outcome rather
than proceeding. Full results:
[`results/ratchet-identification/`](results/ratchet-identification/).

## Study 3 — the prediction slate — is unaffected

**Prediction Slate v1.1 is the binding pre-registration**, frozen and publicly
timestamped. Predictions, conditional probabilities, resolution dates and feeds
are fixed. **P5's resolution window opened 2026-07-28** and runs to 2026-12-31.

**P6 stands.** It is measured by the quarterly companion of Index Spec v0.2 §7
(S8) and will be scored at resolution exactly as defined, on 2029-03-31. A
frozen prediction does not get withdrawn because the project around it changed
shape. The disclosed caveat is that the curvature confound applies to it too, so
a RISE outcome will be consistent with rising co-movement *and* with shared
acceleration — recorded now, before resolution, rather than raised afterwards by
whichever side it suits.

Spec v0.1 and Slate v1.0 are retained solely as provenance for a single
pre-timestamp revision cycle.

## The data gate

**No real series has been fetched, opened, or inspected at any point.** Every
number in this repository is synthetic.

The gate is enforced in code, not by good intentions:
[`scripts/fetch/fetch_all.py`](scripts/fetch/fetch_all.py) requires both an
explicit `--apply` flag and a `data/.gate-open` file created by hand. Identifiers
in [`data/SOURCES.md`](data/SOURCES.md) are recorded as **unverified**, because
verifying them against source pages would itself have been data contact — a
series page renders the current value and the full history.

## Contents

| Path | What it is |
|---|---|
| [`prereg/`](prereg/) | Frozen documents. Append-only: never edited, only superseded. |
| [`results/withdrawal-note.md`](results/withdrawal-note.md) | Why the index test was withdrawn. |
| [`results/ratchet-identification/`](results/ratchet-identification/) | Why Study 2's criterion was not frozen. |
| [`results/power-simulation/`](results/power-simulation/) | What the withdrawn design could and could not detect. |
| [`results/design-comparison/`](results/design-comparison/) | Six candidate designs compared. None rescued it. |
| [`REVIEWER-NOTES.md`](REVIEWER-NOTES.md) | Known limitations, and an errata for a published finding that was wrong. Not part of the pre-registration. |
| [`docs/domain-6-options.md`](docs/domain-6-options.md) | Open decision on the health-capacity series. |
| [`phase-4-precommitment.md`](phase-4-precommitment.md) | Results-blind branch language, drafted before any result existed. Explicitly not part of the pre-registration. |
| [`DATA_TERMS.md`](DATA_TERMS.md) | What may be committed, per source. |
| [`CHECKSUMS.sha256`](CHECKSUMS.sha256) | SHA-256 of everything in `prereg/`. |

## What went wrong, kept in the open

Two published findings in this repository were wrong and have been corrected in
place, with the originals legible:

- A crisis-exclusion leakage result was reported as null. The control that
  produced it was inert — it accepted a parameter it never passed to the data
  generator, so both arms ran contaminated data and differenced to zero by
  construction. Corrected, the bias is **+0.053 toward confirmation**. See the
  errata in [`REVIEWER-NOTES.md`](REVIEWER-NOTES.md).
- A machine-readable export mis-parsed, inverting a calibration ranking, while
  the rendered tables it was derived from were correct.

Both were found by adversarial verification rather than by the analysis that
produced them. That is the argument for the method, and it is why the failures
are documented rather than tidied away.

## Licensing

| What | Licence |
|---|---|
| Code — [`scripts/`](scripts/) | **MIT**, see [`LICENSE`](LICENSE) |
| Prose and outputs — [`prereg/`](prereg/), [`results/`](results/), documentation | **CC BY 4.0**, see [`LICENSE-DOCS`](LICENSE-DOCS) |

Third-party data under `data/` is covered by neither; each series carries its own
source's terms.

## How to verify the timestamp

1. **Commit dates.** `git log --format='%H %ad %s' --date=iso`. Weakest form —
   commit dates come from the committer's machine and can be set to anything.
   **This proves nothing on its own.**
2. **The GitHub release.** Tag `prereg-v1`, timestamped by a third party.
3. **The OSF registration.** *(placeholder — URL and DOI to be inserted)*
   **OSF registrations are immutable**, which makes this the strongest link:
   unlike a git history, the author cannot rewrite it.

   > **OSF URL: _to be added_**
   > **OSF DOI: _to be added_**

To check the frozen documents are unaltered:

```
python scripts/checksums.py verify
```

## Score it

Every prediction carries an exactly-defined YES event, a resolution date, a
resolution feed, and both conditional probabilities — P(YES | thesis) and
P(YES | null) — so the gap between them can be scored against the author rather
than argued about.

Resolutions are adjudicated strictly against the written definitions.
Annotations are permitted; redefinitions are not. Disputes go to an adversarial
review, never to the pro-case.

The standing offer, printed with the slate wherever it appears, in the slate's
own words: **"score us."**
