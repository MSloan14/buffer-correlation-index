# Phase 4 Pre-Commitment — Results-Blind Branch Language for Dossier v3
### Written 2026-07-27, before external timestamp and before any Phase 3 data contact · Not part of the pre-registration · Binding on the Phase 4 writing session

**Why this exists.** Dossier v3's spine is the Phase 3 result, which does not exist yet. The passages that report that result are the ones most vulnerable to unconscious tuning: a withdrawal written after seeing a disconfirming number will hedge, and a confirmation written after seeing a confirming one will overclaim. Both are drafted here, blind, with equal care, before the result can influence either. Phase 4 selects the branch the result dictates and pastes it; it does not rewrite it.

**Status.** This document is *not* pre-registered and carries no evidential weight. It is a self-binding writing constraint. It should be committed to the repository alongside the frozen specs so that its date is on the record, clearly labeled as what it is.

**The one rule that makes it work.** Phase 4 may correct factual errors, update numbers to the Phase 4 snapshot, and adjust transitions for flow. It may **not** soften, qualify, or add caveats to the branch text selected. If Phase 4 believes a branch text is wrong, it says so explicitly in a note and states what it changed and why — visibly, not silently.

---

## 1. The three reporting states

Per Spec v0.2 §0, the verdict space is binary: any result short of full CONFIRM is disconfirmation, and there is no intermediate verdict. But the §6 precision diagnostic creates three *reporting* states, and the distinction is real even though the verdict is not:

| State | Verdict | Branch text |
|---|---|---|
| All four criteria (C1–C4) met | CONFIRM | **A** |
| Short of CONFIRM, precision adequate (MDE₈₀ well below plausible effect sizes) | DISCONFIRM | **B** |
| Short of CONFIRM, precision inadequate (CI wide, MDE₈₀ at or above plausible effect sizes) | DISCONFIRM | **C** |

States B and C withdraw the claim on identical terms. C differs only in what the record says about *why* the test came back empty. Phase 4 selects the state using the §6 diagnostic and, if tonight's power simulation is available, the pre-registered power curve — not by inspecting how close the result came to the threshold.

---

## 2. Branch A — CONFIRM

**Replaces Dossier v2 Part 1, Layer 2:**

> **Layer 2 — Mechanism (measured, at the strength the sensitivity battery supports).** The pre-registered test returned a rising cross-domain covariance of buffer changes over 2000–2026, robust to the frozen sensitivity battery. The correlated-drain precondition is therefore measurably present: the buffers this system runs on have been drawing down in increasingly synchronized fashion, which is the condition under which one shock propagates across domains rather than being absorbed locally.
>
> Four limits bind that sentence, and none of them is optional. First, the test measured a **precondition, not a cascade** — whether a bound buffer produces propagation or restraint is the province of the prediction slate, not this instrument, and the framework's one live case so far (July 2026) produced restraint. Second, the test was run on a **small sample**: endpoint blocks of seven and six annual observations, with the achieved confidence interval and minimum detectable effect published alongside the result. A confirmation at this power is a test survived, not a finding established; the honest reading is that the hypothesis cleared a bar it could have failed, and that a larger or independent replication would carry far more weight than this one does. Third, the two buffers most central to the thesis — munitions and social capital — are the least measurable, so the index leans on the domains that could be measured; the disclosed limitations in the accompanying reviewer notes are part of this result, not a footnote to it. Fourth, the spec was written by a party with an interest in the outcome, and the mitigation is the external timestamp and the scheduled adversarial audit, not our own assurance.
>
> What this licenses: the mechanism layer moves from [H] hypothesis to [V-limited] measured-with-stated-limits. What it does not license: any claim that cascade is demonstrated, that a threshold has been crossed, or that the timing of anything is known.

**Replaces Part 9, one-breath restatement, final two sentences:**

> The mechanism claim that makes this a single story — that the buffers drain together, so one shock cascades instead of being absorbed — was put to a test that was frozen and published before the data were touched, and it survived, on a small sample, with the limits stated in the open. That earns the story a hearing, not a verdict; the forward predictions are published with dates attached, and they are where it can still be killed.

**Appendix A pattern note becomes:**

> Through Phase 1, descriptive resolutions kept landing thesis-ward while mechanism-adjacent resolutions kept landing null-ward. The Phase 3 result is the first mechanism-layer datum to land the other way. One datum does not reverse a pattern; it does mean the pattern is no longer uniform, and the live question — when a buffer binds, does the system correct or cascade? — now has a measured precondition behind it and an unmeasured conditional in front of it.

**Part 6, objection 10, becomes:** answered as posed, within the stated power limits; the objection now transfers to the *conditional* claim (precondition → cascade), which the slate tests and the index cannot.

---

## 3. Branch B — DISCONFIRM, precision adequate

**Replaces Dossier v2 Part 1, Layer 2:**

> **Layer 2 — Mechanism: withdrawn.** The pre-registered test returned flat or domain-idiosyncratic cross-domain covariance over 2000–2026. Under the binding commitment frozen and externally timestamped before the data were touched, **the correlated-drain claim is withdrawn from this framework.** It is not deferred, not reframed as awaiting better instruments, and not retained in weaker language. The buffers described in Layer 1 are thin, and their thinness is documented; the claim that they have been thinning *together* in a way that makes the system cascade-prone is not supported by the test we designed to support it, and we are not entitled to it.
>
> What follows from that, stated plainly. The unified story is gone: what remains is a set of domain-specific depletions with domain-specific causes, which is a weaker and more ordinary claim than the one this framework was built to make. The adaptive-resilience account explains the same data without the additional structure, and on this question it is now the better-supported reading. Anyone who encountered an earlier version of this framework and took the correlated-drain claim seriously should discount it accordingly; the error was ours, it was in the direction our interests ran, and it was caught by a test we committed to in advance rather than by an outside party.
>
> One channel remains open, and it runs forward only: P6 tracks the same statistic out of sample through 2028. If cross-domain covariance rises prospectively, the claim can be re-made on that evidence. It cannot be re-made on this window, and no future version of this document may re-argue 2000–2026 by different methods and count that as recovery.

**Replaces Part 9, one-breath restatement:**

> We can show, with verified numbers, that the shared reserves this system runs on — oil, munitions, fiscal room, market liquidity — sit near multi-decade lows while the proceeds of the drawdown concentrate upward. That description held up under hostile review and it still stands. The claim that made it a single story — that the buffers drain together, so one shock cascades instead of being absorbed — we put to a frozen, published test, and the test came back empty. So we withdrew it. What is left is a well-evidenced description of thin buffers and upward transfer, six dated predictions that can still be scored against us, and one prospective channel through which the abandoned claim could earn its way back. That is less than we set out to show, and it is what we actually have.

**Appendix A pattern note becomes:**

> Every mechanism-adjacent resolution in this project has now landed null-ward: the July 2026 interceptor crunch produced de-escalation, Kharg showed mutual buffer preservation under maximum pressure, the munitions rebuild is contracted and executing, the overdose decline continued and is attributed to supply-side and public-health causes — and the index found no rising co-drain. The descriptive layer resolved thesis-ward with equal consistency. The most economical reading of that split is the one the arbitration reached before any of these resolutions: the facts are right and the story built on them outran them.

**Part 6, objection 1 (unfalsifiability) and objection 10 (correlation unquantified), both become:** answered — objection 10 by measurement, objection 1 by the framework having withdrawn a load-bearing claim on schedule when a pre-committed test failed. That withdrawal is the strongest evidence available that the framework is falsifiable, and it should be stated in exactly those terms, without triumphalism.

---

## 4. Branch C — DISCONFIRM, precision inadequate

**The discipline this branch exists to enforce:** C is where hedging would enter if it entered anywhere. The withdrawal in C is identical to B. The power note is a statement about what *this test* could have established; it is not a reservation attached to the withdrawal, and it may not be written as one.

**Replaces Dossier v2 Part 1, Layer 2:** use **Branch B's text verbatim**, then append exactly this and nothing more:

> **Power note, disclosed in advance.** The instrument was underpowered, and we said so before running it. The design's endpoint blocks hold seven and six annual observations; the achieved confidence interval on the contrast and the minimum detectable effect are published with the result, and the pre-registered limitations were committed to the public record alongside the frozen specification, before the data were touched. A reader is entitled to conclude that this test could not have detected a real effect of plausible size.
>
> That conclusion changes nothing about the withdrawal. We designed the test, we published its limits in advance, we ran it, and it failed to support the claim; a builder who declines to be bound by an instrument they chose and disclosed has pre-registered nothing. The correlated-drain claim is withdrawn on the same terms as if the test had been well-powered. What the power note buys is not a reservation — it is a more accurate account of the record for whoever tries this next, and a reason to prefer P6 and any future replication over this window.

**Part 9 and Appendix A:** use Branch B's text unchanged. The one-breath restatement does not mention power; a restatement that reaches for the excuse is the failure this branch is written to prevent.

---

## 5. Corrections v3 carries regardless of branch

1. **Appendix B scoreboard, rebuilt from Slate v1.1.** P1 is now *exchange-return performance* (≥50% of initially-scheduled exchange crude physically delivered by 2027-12-31; thesis 0.30 / null 0.70). The ≥400M threshold survives only as **P1-t, an unscored watch line** (0.05 / 0.20, dropped under the slate's own convergence rule). Every downstream document — v2's Appendix B, the Phase 1 handoff's Part 5, the execution handoff's Part 6 — still shows the superseded version and must not be copied forward.
2. **P5's definition is the v1.1 rolling-window form**, not the v1.0 consecutive-days form. If Phase 4 runs after 2026-12-31, P5 has resolved: report the outcome and the log-likelihood contribution rather than the prediction.
3. **Print the slate in full** with both conditional probabilities, resolution dates, feeds, and the standing offer — per the handoff's architecture item 3. Include the OSF DOI and repository URL inline; the timestamp is the claim's whole warrant.
4. **Pattern note promoted from Appendix A to the body** (v2 marked it "state it in v3"), in whichever branch form applies.
5. **Objection 1 updated** from "being answered structurally" to answered, citing the timestamp.
6. **Communication guide item 5** already replaced in v2; v3 adds that the slate is public, dated, and third-party timestamped.
7. **Reviewer notes and power simulation cited in the body**, not buried — the design's known limitations were published before data contact, and saying so is worth more than any argument v3 can make about its own rigor.
8. **Standing prior restated** per branch: unchanged for A ("directionally arguable at the descriptive layer; unproven at the mechanism layer"); for B and C it becomes *"supported at the descriptive layer; the mechanism claim was tested and withdrawn."*
9. **Fresh Snapshot Ritual at Phase 4 open** — every volatile value in v2 (Iran pause, SPR, Brent, DOL rule, overdose series, munitions) is date-stamped 2026-07-27 and will be stale.
10. **Phase 3 data-quality compromises** carried into v3 from the results memo, not summarized away.

---

## 6. v3 skeleton with insertion points

| Part | Source | Branch-dependent? |
|---|---|---|
| 0 — Use / tone / provenance | v2 Part 0, + timestamp and repo URL | No |
| 1 — Thesis restratified: Layer 1 descriptive | v2, refreshed to Phase 4 snapshot | No |
| 1 — Layer 2 mechanism | **§2, §3, or §4 above** | **Yes** |
| 1 — Steelman | v2, + the null's updated scoreboard record | Partly |
| 2 — Lenses | v2 unchanged ([M] enforcement intact) | No |
| 3 — Domain evidence | v2 + fresh snapshot + Phase 3 findings | No |
| 4 — Individual resilience | v2 unchanged | No |
| 5 — Source ledger | v2 + index sources | No |
| 6 — Attack surface | v2, objections 1 and 10 updated per branch | Partly |
| 7 — Reciprocity lens | v2 verbatim | No |
| 8 — Communication guide | v2 + slate public/timestamped | No |
| 9 — One-breath restatement | **§2, §3, or §4 above** | **Yes** |
| App. A — ACH matrix + pattern note | v2 + Phase 3 row | **Yes** |
| App. B — Scoreboard | Rebuilt from Slate v1.1 (§5.1) | No |
| App. C — Quarantined rhetoric | v2 verbatim | No |
| App. D — Index result summary | New: verdict, Δρ, CI, MDE, sensitivity battery, data compromises | Content yes |

**Done criterion, unchanged from the execution handoff:** v3 survives being handed to a hostile expert with the raw CSVs attached. Phase 5 is what tests that, and v3 unreviewed is a draft, not a result.
