# Prediction Slate v1.0 (FROZEN)
### Six dated, scoreable predictions dividing the rent-and-fragility thesis from the adaptive-resilience null · Phase 2 deliverable (b)

**Status:** frozen, awaiting external timestamp (public GitHub commit or OSF registration) alongside Buffer-Correlation Index Spec v0.1.
**Provenance chain:** Master Dossier v1 → Red-Team Rebuttal → Arbitration Report → Execution Handoff → Phase 1 Handoff → Phase 2 Kickoff → **this document.**

---

## 0. Purpose and scoring protocol

Predictions shared between the thesis and the null carry no information; **the gap between the two conditional probabilities is the point**, and any prediction on which the two accounts converge is dropped as non-diagnostic (convergence check in §8 — none required dropping). Each prediction below carries: an exactly-defined YES event, a resolution date, a resolution feed, P(YES | thesis), and P(YES | null).

**Scoring.** At each resolution: (i) Brier score for each account's conditional forecast; (ii) the cumulative log-likelihood ratio **Σ ln[P(outcome | thesis) / P(outcome | null)]** across resolved predictions — positive favors the thesis, negative the null. No official prior odds are declared; the likelihood ratio is reported and the reader applies their own prior. Results post to the standing scoreboard carried in every handoff.

**Adjudication rules.** Outcomes are judged strictly against the written definitions below; annotations are permitted, redefinitions are prohibited. If a named data feed is discontinued, the nearest official successor series is used and the substitution logged. Disputes are resolved by an adversarial thread on the Phase 5 model (fresh instance, hostile brief), never by a pro-case thread. The pro-case does not score its own ambiguous calls.

---

## 1. P1 — SPR rebuild

- **YES event:** the Strategic Petroleum Reserve stands at ≥400.0 million barrels in the final EIA weekly print of calendar 2027.
- **Resolution:** 2027-12-31 (adjudicated on the last Weekly Petroleum Status Report of 2027). Feed: EIA WPSR.
- **Barrels count regardless of mechanism.** Crude physically returned to the SPR under the 2026 IEA-coordinated release's exchange agreements counts toward the threshold: the buffer either physically exists or it does not, and the thesis claim is about reconstitution, not legal form.
- **P1a (sub-resolution, scored separately):** YES if ≥50% of exchange-agreement crude contractually due for return to the SPR on or before 2027-12-31 (per DOE published exchange schedules as they stand at resolution) has been physically delivered by that date. Rationale: the two worlds genuinely diverge on whether even *contracted* returns materialize — thesis-world predicts deferral and renegotiation, null-world predicts contractual performance. Distinguishing "refill via exchange returns" from "no refill" was mandated at Phase 1 and is implemented here.
- **P(YES):** P1 — thesis **0.20**, null **0.65** (gap 45). P1a — thesis **0.30**, null **0.70** (gap 40).

## 2. P2 — Systemic private-credit event

- **YES event:** on or before 2029-12-31, at least one of the following occurs: **(i)** an official-sector emergency action directed at the private-credit / BDC / interval-fund complex (a Federal Reserve facility, Treasury or FSOC emergency measure, or an explicit regulatory forbearance program responding to private-credit distress); **(ii)** within any rolling 90-day window, suspension or gating of redemptions, or payment default on fund-level obligations, at ≥3 unaffiliated private-credit vehicles with combined AUM ≥ $50B; **(iii)** failure or forced rescue (assisted acquisition, official or consortium bailout) of a top-10-by-private-credit-AUM manager.
- **Explicitly NOT sufficient:** a single fund failing, NAV markdowns however deep, spread widening, or concentrated losses at LPs without contagion — that is the "concentrated losses" world, and it scores for the null.
- **Resolution:** 2029-12-31. Feeds: Federal Reserve / Treasury / FSOC announcements; SEC filings; first-tier financial press for the gating count.
- **P(YES):** thesis **0.60**, null **0.20** (gap 40).

## 3. P3 — Term premium (threshold set under the authorized ACM pull)

- **Reference values retrieved 2026-07-27 (the single authorized data contact):** ACM 10-year term premium, monthly: Mar 2025 = 0.391%, Apr 2025 = 0.615% (CEIC, sourcing NY Fed), with the NY Fed dashboard showing ≈+35bp across April 2025; the series positive throughout 2025 (six-month moving average positive through year-end); Apr 2026 monthly = 0.73%; daily 2026-05-15 = 0.83%; daily 2026-06-29 = 0.47% (MacroMicro, sourcing NY Fed); frozen-record FRED prints 0.7322% (2026-07-02) and 0.7788% (2026-07-10). Kim–Wright companion for context only: >0.8% on 2025-01-13 (highest since 2011), ≈0.5% on 2025-05-02.
- **Reference estimate of the 2025 ACM calendar-year mean: ≈0.50%**, an estimate from the partial monthly anchors above, disclosed as such. It is a reference value, not the operative threshold, because the ACM model is retrospectively re-estimated and published history shifts by a few basis points across vintages.
- **Operative threshold (vintage-consistent, frozen as a formula with all parameters fixed):** T = M₂₀₂₅ + 0.25 percentage points, where M₂₀₂₅ = the mean of the twelve monthly ACM 10-year term-premium values for calendar 2025, computed from the NY Fed series vintage available on the resolution date. Reference T ≈ 0.75%.
- **YES event:** the mean of the twelve monthly ACM 10-year term-premium values for calendar 2027, from the same resolution-date vintage, exceeds T.
- **Why the +25bp margin:** bare exceedance of the 2025 mean is near-convergent — term premia are persistent, and both worlds would assign it high probability, which would force this prediction's deletion under the divergence rule. The margin makes P3 test the thesis's actual claim — a structural upward re-rating as fiscal space compresses — against the null's reversion-toward-2025 once the war shock passes. In effect: the thesis predicts the 2027 average holds at or above mid-2026's elevated level; the null predicts decay back toward the 2025 base.
- **Resolution:** 2028-01-31 (first NY Fed monthly publication covering full-year 2027). Feed: NY Fed ACM term premia page (FRED mirror acceptable). Descriptive, unscored companion line: the fraction of 2027 months above M₂₀₂₅.
- **P(YES):** thesis **0.65**, null **0.30** (gap 35).

## 4. P4 — Fourth consecutive annual overdose decline

- **YES event:** NCHS-reported total US drug-overdose deaths for calendar 2026 are lower than for calendar 2025, both figures as published in the same release — the first NCHS annual provisional release covering CY2026 (expected ~May–June 2027). Same-release comparison is required to neutralize the live provisional-revision channel. Backstop: if that release has not appeared by 2027-09-30, resolve on the CDC provisional 12-month-ending-December-2026 estimate as published at that date, against the 12-month-ending-December-2025 estimate in the same publication.
- **Policy-confound rule (frozen, verbatim in intent from Phase 1):** P4 tests the strong "bodies register the macro" claim only. If overdose declines reverse following documented cuts to Medicaid or prevention funding, the reversal scores for the null's supply-side/public-health account with an annotation — evidence about public-health-buffer withdrawal, not about macro-despair — and does not vindicate the strong thesis. A NO outcome is therefore adjudicated for attribution before scoring: only a reversal *not* attributable to documented policy withdrawal scores against the null.
- **The honest anti-thesis prediction:** this is the slate's credibility purchase. The thesis-as-written is embarrassed by continuation; it is included precisely because the framework must be scoreable where it is weakest.
- **Resolution:** ~2027-06-30 (backstop 2027-09-30). Feed: NCHS/CDC releases.
- **P(YES):** thesis **0.35**, null **0.70** (gap 35).

## 5. P5 — Does buffer-binding de-escalation hold?

- **Scored on behavior, not rhetoric (frozen, verbatim in intent from Phase 1):** Iran refusing the word "ceasefire" while holding fire is a hold. Diplomatic labels, threats, and posturing are non-events for this prediction.
- **Failure event ("resumed exchange"), defined numerically before events force the call:** two or more consecutive calendar days on each of which BOTH (a) US and/or Israeli forces conduct kinetic strikes (launched munitions targeting the adversary, regardless of interception outcome) against Iranian territory or Iranian military assets, AND (b) Iranian forces — or strikes attributed to Iranian direction by two first-tier outlets or an official US/Israeli statement — conduct kinetic strikes against US, Israeli, or Gulf-partner territory, forces, or flagged shipping. Proxy actions without attributed Iranian direction (e.g., Houthi strikes alone), one-sided strikes, single-day exchanges, covert sabotage, and cyber operations do not qualify. Israel is included on the Western side because the depleted interceptor complex — the buffer whose binding is under test — is shared.
- **YES event (pause holds):** no resumed exchange, as defined, occurs from 2026-07-28 through 2026-12-31.
- **Resolution:** 2026-12-31, adjudicated by 2027-01-07 to absorb reporting lag. Feed: first-tier wire and press reporting (Reuters/AP class), official statements.
- **P(YES):** thesis **0.40**, null **0.75** (gap 35). This is the nearest-term, most diagnostic entry: thesis-world's metastable exhaustion with no shock-absorbing channel breaks; null-world's negative-feedback dominance holds.

## 6. P6 — The index's own out-of-sample trajectory

- **Instrument:** the quarterly companion of Index Spec v0.1 (§7, S8): mean pairwise Pearson correlation of first-differenced normalized series over the trailing 40-quarter window, on the quarterly-native subset (strategic reserve, financial, fiscal debt/GDP, household).
- **Outcome variable:** the companion statistic at 2028Q4 minus its value at 2026Q4 (computable ~2029-03-31 when 2028Q4 data are complete). Trailing windows at both endpoints contain crisis quarters; the headline P6 comparison includes them (this is out-of-sample tracking, not the between-crisis trend test), with the ex-crisis variant reported as an annotation per the spec.
- **Resolution bands:** RISE if the change exceeds +0.05; FLAT within ±0.05; DECLINE below −0.05.
- **P(outcome):** thesis — RISE **0.55**, FLAT **0.30**, DECLINE **0.15**. Null — RISE **0.25**, FLAT **0.40**, DECLINE **0.35**. (Multi-outcome Brier at resolution.)
- **Contingency:** P6 exists only because Spec v0.1 is frozen; if the Phase 3 result disconfirms over 2000–2026, the correlated-drain *claim* is withdrawn per the spec's binding commitment, and P6 remains the sole forward-looking channel through which the hypothesis may earn its way back — prospectively, never retrospectively.
- **Resolution:** 2029-03-31. Feed: the Phase 3 data pipeline, extended per the frozen methodology; scripts and CSVs auditable by Phase 5.

---

## 7. What is deliberately absent

No prediction is included for munitions-stock levels (classified; unresolvable) or for any outcome on which thesis and null agree (e.g., "AI capex slows eventually," "the DoL rule finalizes" — both worlds expect these at similar probability, so they carry no diagnostic weight and appear only on the descriptive watch list, not here).

## 8. Convergence check (mandated: drop any prediction whose probabilities converge)

| P | P(YES\|thesis) | P(YES\|null) | Gap (pts) | Kept? |
|---|---|---|---|---|
| P1 | 0.20 | 0.65 | 45 | Yes |
| P1a | 0.30 | 0.70 | 40 | Yes |
| P2 | 0.60 | 0.20 | 40 | Yes |
| P3 | 0.65 | 0.30 | 35 | Yes |
| P4 | 0.35 | 0.70 | 35 | Yes |
| P5 | 0.40 | 0.75 | 35 | Yes |
| P6 (RISE) | 0.55 | 0.25 | 30 | Yes |

All gaps ≥30 points; nothing dropped. The standing offer prints with the slate wherever it appears: **score us.**

---

**Version: v1.0 · Date frozen: 2026-07-27**
No edits after external timestamp; amendments require a new versioned spec citing this one.
