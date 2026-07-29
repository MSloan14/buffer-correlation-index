# Prediction Slate v1.1 (FROZEN)
### Dated, scoreable predictions dividing the rent-and-fragility thesis from the adaptive-resilience null · Phase 2 deliverable (b) · Supersedes v1.0 under the single authorized pre-timestamp revision cycle

**Status:** frozen, awaiting external timestamp (public GitHub commit or OSF registration) alongside Buffer-Correlation Index Spec v0.2. v1.0 was frozen but never externally timestamped; a bounded review pass identified defects, and this document is the single permitted revision before the timestamp binds. v1.0's freeze sentence was not violated: it bars edits after the external timestamp, which does not yet exist.
**Provenance chain:** Master Dossier v1 → Red-Team Rebuttal → Arbitration Report → Execution Handoff → Phase 1 Handoff → Phase 2 Kickoff → Slate v1.0 → bounded review pass → **this document.**
**Revision conditions:** no data contact in this revision. The single authorized ACM term-premium pull was exercised by the v1.0 session and is not repeated; its values stand recorded in §3. Every v1.1 change is tagged in the change log (§9) with its direction of effect.

---

## 0. Purpose and scoring protocol

Predictions shared between the thesis and the null carry no information; **the gap between the two conditional probabilities is the point**, and any prediction on which the two accounts converge is dropped as non-diagnostic (convergence check in §8 — one drop executed in v1.1). Each prediction below carries: an exactly-defined YES event, a resolution date, a resolution feed, P(YES | thesis), and P(YES | null).

**Scoring.** At each resolution: (i) Brier score for each account's conditional forecast; (ii) the cumulative log-likelihood ratio **Σ ln[P(outcome | thesis) / P(outcome | null)]** across resolved predictions — positive favors the thesis, negative the null. No official prior odds are declared; the likelihood ratio is reported and the reader applies their own prior. Results post to the standing scoreboard carried in every handoff.

**Adjudication rules.** Outcomes are judged strictly against the written definitions below; annotations are permitted, redefinitions are prohibited. If a named data feed is discontinued, the nearest official successor series is used and the substitution logged. Disputes are resolved by an adversarial thread on the Phase 5 model (fresh instance, hostile brief), never by a pro-case thread. The pro-case does not score its own ambiguous calls.

---

## 1. P1 — SPR rebuild

**P1 (scored) — exchange-return performance.** Formerly sub-resolution P1a; promoted to the scored SPR prediction in v1.1 (change log, entries 2–4).

- **YES event:** at least 50% of the exchange-agreement crude due for physical return to the SPR on or before 2027-12-31 **under the initial DOE-published return schedule for each 2026 exchange agreement** (the first schedule DOE published for that agreement, whenever published) has been physically delivered to the SPR by 2027-12-31. Subsequent renegotiations, deferrals, or amended schedules do not alter the denominator: deferral of initially-due crude counts as non-delivery. Zero-denominator guard: if no exchange crude was due on or before 2027-12-31 under initial schedules, P1 resolves UNSCORED with annotation.
- **Rationale (carried from v1.0):** the two worlds genuinely diverge on whether even *contracted* returns materialize — thesis-world predicts deferral and renegotiation, null-world predicts contractual performance. Distinguishing "refill via exchange returns" from "no refill" was mandated at Phase 1 and is implemented here. The initial-schedule anchor exists because deferral is the thesis's own predicted behavior; a denominator that shrank with each deferral would convert the thesis's predicted world into a YES for the null.
- **Resolution:** 2027-12-31, adjudicated on DOE Office of Petroleum Reserves publications and the EIA WPSR record.
- **P(YES):** thesis **0.30**, null **0.70** (gap 40; carried from v1.0's P1a assignment, which conditioned on exactly this performance-vs-deferral divergence). Annotation permitted at adjudication if physical injection capacity, rather than contractual behavior, is documented as the binding constraint on delivery.

**P1-t (watch line, unscored as of v1.1) — the ≥400M threshold.**

- **Event (text unchanged from v1.0's headline):** the Strategic Petroleum Reserve stands at ≥400.0 million barrels in the final EIA weekly print of calendar 2027. Barrels count regardless of mechanism: crude physically returned under the 2026 exchange agreements counts toward the threshold — the buffer either physically exists or it does not.
- **Recalibration (v1.1, review item 4; full arithmetic in §9 entry 2):** the event requires ~88.6M barrels of net build in ≤17.2 months from the frozen record's last print, ≈5.2M bbl/month sustained from day one with zero further draw — at or above the program's historical maximum sustained fill rate per the review-pass documentation — against in-record salt-cavern constraints, no executing refill program, and a reserve still drawing at the record's close. Recalibrated reference probabilities: thesis **0.05**, null **0.20**. Gap 15 points.
- **Disposition:** dropped from Brier/LLR scoring per §0's convergence rule (the slate's own v1.0 practice held every scored gap at ≥30 points). Retained inline, unscored, because the feed remains live context for P1 and for the standing scoreboard's descriptive watch list.
- **Feed (watch only):** EIA WPSR, final weekly print of 2027.

## 2. P2 — Systemic private-credit event

- **YES event:** on or before 2029-12-31, at least one of the following occurs: **(i)** an official-sector emergency action directed at the private-credit / BDC / interval-fund complex (a Federal Reserve facility, Treasury or FSOC emergency measure, or an explicit regulatory forbearance program responding to private-credit distress); **(ii)** within any rolling 90-day window, suspension or gating of redemptions, or payment default on fund-level obligations, at ≥3 unaffiliated private-credit vehicles with combined AUM ≥ $50B; **(iii)** failure or forced rescue (assisted acquisition, official or consortium bailout) of a top-10-by-private-credit-AUM manager.
- **Explicitly NOT sufficient:** a single fund failing, NAV markdowns however deep, spread widening, or concentrated losses at LPs without contagion — that is the "concentrated losses" world, and it scores for the null.
- **Resolution:** 2029-12-31. Feeds: Federal Reserve / Treasury / FSOC announcements; SEC filings; first-tier financial press for the gating count.
- **P(YES):** thesis **0.60**, null **0.20** (gap 40).

## 3. P3 — Term premium (threshold set under the authorized ACM pull)

- **Reference values retrieved 2026-07-27 (the single authorized data contact, exercised at v1.0; not repeated):** ACM 10-year term premium, monthly: Mar 2025 = 0.391%, Apr 2025 = 0.615% (CEIC, sourcing NY Fed), with the NY Fed dashboard showing ≈+35bp across April 2025; the series positive throughout 2025 (six-month moving average positive through year-end); Apr 2026 monthly = 0.73%; daily 2026-05-15 = 0.83%; daily 2026-06-29 = 0.47% (MacroMicro, sourcing NY Fed); frozen-record FRED prints 0.7322% (2026-07-02) and 0.7788% (2026-07-10). Kim–Wright companion for context only: >0.8% on 2025-01-13 (highest since 2011), ≈0.5% on 2025-05-02.
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
- **Failure event ("resumed exchange"), v1.1 definition (repaired after backtest; change log, entry 1):** within any rolling 7-calendar-day window (days defined by Arabian Standard Time, UTC+3), **(a)** one side conducts kinetic strikes (launched munitions targeting the adversary, regardless of interception outcome) against the qualifying target set on **three or more distinct calendar days**, AND **(b)** the other side conducts **at least one** qualifying kinetic strike within the same window. Sides and qualifying target sets: Western side — US and/or Israeli forces, striking Iranian territory or Iranian military assets; Iranian side — Iranian forces, or strikes attributed to Iranian direction by two first-tier outlets or an official US/Israeli statement, striking US, Israeli, or Gulf-partner territory, forces, or flagged shipping. Either side may be the ≥3-day striker; the definition is symmetric and imposes no causal ordering between (a) and (b). Exclusions unchanged from v1.0: proxy actions without attributed Iranian direction (e.g., Houthi strikes alone), covert sabotage, and cyber operations do not qualify; single strikes and sub-threshold patterns (fewer than three strike days by one side, or no strike by the other side within the window) do not trigger. Israel is included on the Western side because the depleted interceptor complex — the buffer whose binding is under test — is shared.
- **Backtest disclosed:** the v1.0 definition (≥2 consecutive days with BOTH sides striking on each day) fails against the July 2026 campaign as documented in the Phase 1 record — thirteen consecutive US strike nights with episodic Iranian retaliation on Gulf bases produces no two consecutive days of same-day reciprocal strikes, so the paradigm resumed exchange would not have triggered its own definition. The v1.1 definition triggers on that campaign (≥3 US strike days in any 7-day window; ≥1 attributed Iranian strike within such windows).
- **YES event (pause holds):** no resumed exchange, as defined, occurs from 2026-07-28 through 2026-12-31.
- **Resolution:** 2026-12-31, adjudicated by 2027-01-07 to absorb reporting lag. Feed: first-tier wire and press reporting (Reuters/AP class), official statements.
- **P(YES):** thesis **0.40**, null **0.75** (gap 35; unchanged — the v1.0 probabilities were assigned to the phenomenon "does fighting resume," which the v1.0 text mis-operationalized and the v1.1 text realigns; see §9 entry 1). This is the nearest-term, most diagnostic entry: thesis-world's metastable exhaustion with no shock-absorbing channel breaks; null-world's negative-feedback dominance holds.

## 6. P6 — The index's own out-of-sample trajectory

- **Instrument:** the quarterly companion of Index Spec v0.2 (§7, S8; substantively identical to the v0.1 companion — the v0.2 food domain is annual-native and does not enter it): mean pairwise Pearson correlation of first-differenced normalized series over the trailing 40-quarter window, on the quarterly-native subset (strategic reserve, financial, fiscal debt/GDP, household).
- **Outcome variable:** the companion statistic at 2028Q4 minus its value at 2026Q4 (computable ~2029-03-31 when 2028Q4 data are complete). Trailing windows at both endpoints contain crisis quarters; the headline P6 comparison includes them (this is out-of-sample tracking, not the between-crisis trend test), with the ex-crisis variant reported as an annotation per the spec.
- **Resolution bands:** RISE if the change exceeds +0.05; FLAT within ±0.05; DECLINE below −0.05.
- **P(outcome):** thesis — RISE **0.55**, FLAT **0.30**, DECLINE **0.15**. Null — RISE **0.25**, FLAT **0.40**, DECLINE **0.35**. (Multi-outcome Brier at resolution.)
- **Contingency:** P6 exists only because the spec is frozen; if the Phase 3 result disconfirms over 2000–2026, the correlated-drain *claim* is withdrawn per the spec's binding commitment, and P6 remains the sole forward-looking channel through which the hypothesis may earn its way back — prospectively, never retrospectively.
- **Resolution:** 2029-03-31. Feed: the Phase 3 data pipeline, extended per the frozen methodology; scripts and CSVs auditable by Phase 5.

---

## 7. What is deliberately absent

No prediction is included for munitions-stock levels (classified; unresolvable) or for any outcome on which thesis and null agree (e.g., "AI capex slows eventually," "the DoL rule finalizes" — both worlds expect these at similar probability, so they carry no diagnostic weight and appear only on the descriptive watch list, not here). As of v1.1, the SPR ≥400M threshold event joins the watch-list category: retained inline as P1-t for the record, excluded from scoring after recalibration collapsed its diagnostic gap.

## 8. Convergence check (mandated: drop any prediction whose probabilities converge)

| P | P(YES\|thesis) | P(YES\|null) | Gap (pts) | Scored? |
|---|---|---|---|---|
| P1 (exchange-return performance) | 0.30 | 0.70 | 40 | Yes |
| P1-t (≥400M threshold) | 0.05 | 0.20 | 15 | **No — dropped per §0 convergence rule (v1.1)** |
| P2 | 0.60 | 0.20 | 40 | Yes |
| P3 | 0.65 | 0.30 | 35 | Yes |
| P4 | 0.35 | 0.70 | 35 | Yes |
| P5 | 0.40 | 0.75 | 35 | Yes |
| P6 (RISE) | 0.55 | 0.25 | 30 | Yes |

All scored gaps ≥30 points. One drop executed in v1.1 under the slate's own rule. The standing offer prints with the slate wherever it appears: **score us.**

---

## 9. Change log v1.0 → v1.1 (each entry tagged: thesis-helping / null-helping / neutral-precision; governing rule: every change must increase discriminating power, never merely change which outcome is likelier)

**Preamble.** Predecessor: Prediction Slate v1.0, frozen 2026-07-27, never externally timestamped. This is the single authorized pre-timestamp revision, executed against a written review brief; slate-side items are 3 (P5) and 4 (P1). The scoring protocol (§0) is unweakened and is *applied* in entry 3.

1. **P5 failure definition repaired (review item 3).** Backtest: the v1.0 definition required ≥2 consecutive calendar days with BOTH sides striking on each day; the July 2026 campaign — thirteen consecutive US strike nights, episodic Iranian retaliation on Gulf bases, per the Phase 1 handoff — contains no such pair of days unless retaliation happened to land on back-to-back strike days, so the paradigm resumed exchange would not have triggered the definition. A failure definition that does not trigger on its own motivating case discriminates nothing between the two worlds; the repair (either side strikes on ≥3 days within any rolling 7-day window, plus ≥1 qualifying strike by the other side within the same window, all v1.0 qualifying clauses and exclusions carried, calendar convention fixed at AST) is the minimal change that realigns the written event with the phenomenon the probabilities were assigned to. **Direction: thesis-helping, tagged honestly and against the review brief's parenthetical.** The brief states "a tighter failure definition is null-helping"; the direction analysis runs the other way and is recorded rather than adopted: the repair makes the failure trigger *more* sensitive, lowering P(YES) under both accounts and exposing the null's high-confidence YES (0.75) to more downside — equivalently, the v1.0 text was inadvertently null-helping (a real resumed campaign could have resolved YES, scoring for the null against reality), and removing that bias helps the thesis relative to v1.0. Probabilities unchanged (0.40 / 0.75): they were assigned to the phenomenon, not to the defective text. Power ground: restores the prediction's ability to see the event it exists to score.
2. **P1-t (the ≥400M threshold, v1.0's scored headline) recalibrated (review item 4).** Arithmetic, from the frozen record: last recorded print 311.4M (w/e 2026-07-17), still drawing at −5.1M bbl/wk, no executing refill program, salt-cavern constraints in the record. Required build: 400.0 − 311.4 = **88.6M bbl**. Available time from the record date (2026-07-27) to resolution (2027-12-31): ≈17.2 months. Required sustained rate assuming the draw stops immediately and fill starts immediately: 88.6 / 17.2 ≈ **5.2M bbl/month for 17 consecutive months** — characterized by the review-pass documentation as at or above the program's historical maximum sustained fill rate. Each additional month of continued draw at the last recorded rate (≈22M bbl/month) raises the required sustained rate by roughly 1.5–2M bbl/month. The null's world is orderly rebuilding and contractual performance; it is not record-exceeding fill from a standing start, so P(YES|null) = 0.65 assigned a supermajority probability to a near-infeasible engineering outcome and is unjustifiable. Recalibrated: **null 0.65 → 0.20** (residual mass for front-loaded schedules, supplementary commercial purchases, and the possibility that the historical-maximum characterization, which is documentary rather than engineering-verified, is loose); **thesis 0.20 → 0.05** (the same physics binds both worlds; the thesis's v1.0 value was also too high). **Direction: null-helping.** At v1.0 values, a physically-determined NO would have banked ln(0.80/0.35) ≈ **+0.83** of log-likelihood for the thesis on an outcome carrying no information about which world is real; the recalibration (and entry 3) removes that free thesis gain. Power ground: a prediction whose outcome is fixed by arithmetic in both worlds discriminates nothing.
3. **Convergence drop executed (consequence of entry 2).** Recalibrated gap = 15 points, below the ≥30-point floor v1.0's own §8 practice applied; §0 mandates dropping converged predictions, and refusing to apply the slate's own rule would weaken the frozen protocol. P1-t exits Brier/LLR scoring and is retained inline as an unscored watch line. **Direction: null-helping** (same removal as entry 2). Power ground: scoring mass now sits entirely on genuinely diagnostic events.
4. **P1a promoted to the scored P1 (consequence of entries 2–3).** The Phase-1-mandated sub-resolution — exchange-return performance — becomes the scored SPR prediction; probabilities 0.30 / 0.70 carried from v1.0, whose assignment already conditioned on the performance-vs-deferral divergence. **Direction: neutral-to-null-helping** relative to v1.0's headline (replaces a thesis-favoring scoring artifact with a genuinely contested event). Power ground: this is the SPR question on which the two worlds actually disagree.
5. **P1 denominator anchored to initial DOE-published schedules; zero-denominator guard added (integrity of the promoted P1, within item 4).** Under v1.0's text ("schedules as they stand at resolution"), deferral — the thesis's own predicted behavior — would shrink the denominator and push P1 toward YES, scoring for the null precisely when the thesis's world obtains. The anchor makes deferral count as non-delivery, which is what the 0.30/0.70 assignment assumed; the guard handles the empty-denominator case (resolves UNSCORED with annotation). **Direction: anchor thesis-helping** (restores the event's alignment with the assigned probabilities; makes YES strictly harder); **guard neutral-precision.** Residual risk — a tiny nonzero initially-due denominator could still resolve YES trivially: **noted, deferred to post-timestamp versioning.**
6. **P6 instrument reference updated v0.1 → v0.2** (quarterly companion substantively unchanged; the new food domain is annual-native and outside it). **Direction: neutral.**
7. **Defects noticed, out of the review brief's scope — noted, deferred to post-timestamp versioning, flagged to Phase 5:** (i) P2(iii)'s "top-10-by-private-credit-AUM" lacks an as-of date for the ranking (manager rank at event time vs at slate time). (ii) P3's vintage-shift exposure — M₂₀₂₅ recomputed from the resolution-date vintage can drift a few basis points — stands as disclosed in v1.0; no change. (iii) P1's de-minimis-denominator residual from entry 5.

---

**Version: v1.1 · Date frozen: 2026-07-27 · Predecessor: v1.0 (2026-07-27, superseded pre-timestamp)**
No edits after external timestamp; amendments require a new versioned spec citing this one.
