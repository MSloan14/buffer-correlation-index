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
| **Study 2** | The ratchet question — have buffers that once rebuilt after stress episodes stopped doing so? | **Criterion frozen 2026-08-01**, validated before freezing, before any data contact |
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

## Study 2 — the ratchet question, frozen 2026-08-01

The ratchet question survived the index withdrawal because it does not depend on
cross-domain covariance. The criterion in
[`prereg/ratchet-spec-v1.0.md`](prereg/ratchet-spec-v1.0.md) was drafted and
then — before freezing — tested against synthetic worlds, on the principle that
the index test's failure was one of identification and the replacement should be
checked for the same disease before it was trusted.

**It discriminates.** A late-onset ratchet is separated from a pure accelerating
decline by **+78.0 points** (90.2% versus 12.2%), against a +20 requirement. It
is also specific: **99.6%** "against H-R" in both mean-reversion worlds. If
buffers genuinely rebuild, this criterion says so.

**The claim it tests was narrowed before freezing.** The draft worded the
hypothesis timelessly — every episode ratchets, in every era — while its own
machinery tested a *change* in rebuild behaviour. The single permitted amendment
re-scoped the claim to match the test: **buffers that formerly rebuilt have
stopped doing so.** That is a strictly narrower hypothesis and a harder one to
support; a domain that has ratcheted steadily since 1950 is now invisible to the
test. The amendment is recorded in §1 of the frozen spec with its direction of
effect.

Three limitations are frozen into the specification and bind any result: the
criterion is **blind to ratchets shallower than 10%** — so an "against" verdict
means "no ratchet ≥ 10%", not refutation — the episode detector fires on
episode-free trending series, and a violent smooth late collapse can fake the
signature.

The validation, including a correction notice for an earlier run that reached
the opposite conclusion and nearly ended the study:
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
| [`results/ratchet-identification/`](results/ratchet-identification/) | The validation that let Study 2's criterion be frozen, and a correction notice for an earlier run that reached the opposite conclusion. |
| [`results/power-simulation/`](results/power-simulation/) | What the withdrawn design could and could not detect. |
| [`results/design-comparison/`](results/design-comparison/) | Six candidate designs compared. None rescued it. |
| [`REVIEWER-NOTES.md`](REVIEWER-NOTES.md) | Known limitations, and an errata for a published finding that was wrong. Not part of the pre-registration. |
| [`SUPPLEMENTARY.md`](SUPPLEMENTARY.md) | Everything outside the frozen core: descriptive companions, slate evidence logs, case-tracing candidates. **Post-freeze, descriptive only, excluded from Study 2 scoring.** |
| [`results/watch/`](results/watch/) | Dated evidence logs for each slate prediction. Events, not arguments. |
| [`docs/domain-6-options.md`](docs/domain-6-options.md) · [`domain-6-decision.md`](docs/domain-6-decision.md) | The health-capacity series choice, and why beds is primary. |
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

**Registered 2026-08-01 18:53 UTC−5**, Open-Ended Registration, contributor
Mica N Sloan.

| | |
|---|---|
| **OSF registration** | https://osf.io/n6gep |
| **Registration DOI** | 10.17605/OSF.IO/N6GEP |
| **Parent project** (all seven documents, public, CC BY 4.0) | https://osf.io/xpz6m |
| **Internet Archive snapshot** | https://archive.org/details/osf-registrations-n6gep-v1 |

**The ratchet criterion was frozen and third-party timestamped before any real
series was fetched.** The registration went live on 2026-08-01; the data gate
opened afterwards. That ordering is the point, and it is checkable: the
criterion in [`prereg/ratchet-spec-v1.0.md`](prereg/ratchet-spec-v1.0.md) is in
the registration, and every file under `data/` postdates it.

**Known issue with the OSF archive folder.** The registration's own archive
folder is empty, due to a platform problem rather than anything about the
documents. The seven constituent documents are available in three other places:
the **parent project** linked above, this repository at tag
[`prereg-v1`](https://github.com/MSloan14/buffer-correlation-index/releases/tag/prereg-v1),
and the Internet Archive snapshot. Per-file SHA-256 hashes are in
[`CHECKSUMS.sha256`](CHECKSUMS.sha256), so copies from any source can be checked
against each other.

Three ways to check the timestamp, weakest first:

1. **Commit dates.** `git log --format='%H %ad %s' --date=iso`. Weakest form —
   commit dates come from the committer's machine and can be set to anything.
   **This proves nothing on its own.**
2. **The GitHub release.** Tag `prereg-v1`, timestamped by a third party.
3. **The OSF registration.** Immutable, which makes it the strongest link:
   unlike a git history, the author cannot rewrite it.

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
