# Buffer-Correlation Index — Specification v0.1 (FROZEN)
### Pre-registered test of the correlated-drain hypothesis · Written blind to joint data · Phase 2 deliverable (a)

**Status:** frozen, awaiting external timestamp (public GitHub commit or OSF registration) before any Phase 3 data contact.
**Provenance chain:** Master Dossier v1 → Red-Team Rebuttal → Arbitration Report → Execution Handoff → Phase 1 Handoff → Phase 2 Kickoff → **this document.**
**Authorship conditions:** produced in a session with no contact with any buffer-series data. One authorized exception was exercised: retrieval of current and 2025 NY Fed ACM term-premium values, used solely to set the Prediction Slate's P3 threshold. The term premium is not a component of this index.

---

## 0. The claim under test

The framework's mechanism layer asserts, as hypothesis [H]: *US collective buffers have been draining in increasingly correlated fashion over 2000–2026 — cross-domain co-movement of buffer drawdowns has risen over the window — which is the precondition under which a single shock propagates across buffers rather than being absorbed locally.*

This index tests the **precondition** (rising co-drain), not cascade itself. Whether a bound buffer produces cascade or restraint is the province of the Prediction Slate (P2, P5), not of this instrument. A confirming result here establishes only that the correlated-drain precondition is measurably present; a disconfirming result withdraws the correlated-drain claim entirely.

**The binding commitment (Execution Handoff Rule 3; Kickoff Constraint 3), verbatim:**

> *If the pre-specified analysis returns flat or domain-idiosyncratic cross-domain covariance over 2000–2026, the correlated-drain claim is withdrawn from the framework. No hedging into "not yet measurable."*

Operationally (§6): any result short of the full CONFIRM criteria constitutes disconfirmation for the purposes of this commitment. There is no intermediate verdict. The hypothesis may thereafter be tracked forward only through Prediction P6 (out-of-sample), never re-asserted retrospectively over 2000–2026 without a new, versioned, externally timestamped specification.

---

## 1. Scope

- **Geography:** United States only. Cross-country extension is future work.
- **Window:** 2000–2026 nominal. Observations for 2026 enter only when the full calendar year's underlying data are published (in practice: not before Phase 3 concludes for most annual-native series, and 2026 is a crisis-excluded year under §6 regardless, so the crisis-excluded headline statistic effectively spans 2000–2025).
- **Frequency:** **Annual** for the primary analysis. Justification: three of seven domains are annual-native (fiscal net-interest, health, social) and one is sparse-annual (corporate); computing the headline statistic at the lowest common native frequency avoids interpolation, and interpolation is banned in this spec because carrying annual values across quarters deflates within-year variance and manufactures spurious correlation structure. The cost — few observations — is acknowledged in §6 (power note) and partially offset by the quarterly companion analysis (§7, S8) on the quarterly-native subset.
- **Domains:** seven quantitative domains (§3), with munitions carried as a qualitative carve-out (§4). Seven sits inside the mandated 7–9 range.
- **Temporal aggregation:** sub-annual native series enter the annual index as calendar-year means of their native-frequency observations (weekly→monthly→annual means). Federal fiscal-year series are mapped to the calendar year containing the majority of the fiscal year (FY *t*, Oct *t−1*–Sep *t* → calendar year *t*). For the quarterly companion, monthly series enter as quarterly means.

---

## 2. Methodology — provenance and blindness disclosure (opens this section per Kickoff Constraint 6)

**(a)** The author of this specification knew, at spec time, the current (July 2026) levels of several candidate components — the SPR level, the direction of distillate stocks, the fiscal and private-market stress facts — because the project exists precisely because those levels are known to be low; the Phase 1 Handoff, a required input, contains them. Perfect blindness is unattainable here and is not claimed. **(b)** The author did not examine any historical joint series — no time series of any component over 2000–2026, individually or jointly — before freezing the component selection, orientations, normalization, test statistic, block boundaries, crisis windows, or confirm/disconfirm criteria in this document. The single authorized data pull (ACM term premium, for the Prediction Slate's P3) concerns a series that is not an index component. **(c)** The quantity under test — the *trend* in cross-domain covariance of buffer changes over 2000–2026 — is not recoverable from knowledge of current endpoint levels. Knowing that seven buffers are simultaneously low in 2026 says nothing about whether their drawdowns co-moved increasingly over the preceding quarter century; that is exactly what makes this freeze meaningful despite (a). A referee will note residual contamination: any macro-literate author "knows" roughly how 2008 and 2020 behaved. The mitigations are mechanical block boundaries (§5), date-defined crisis exclusions fixed before data contact (§6), and Phase 5's explicit mandate to audit this spec for hindsight bias.

---

## 3. Components and feeds (frozen selection)

| # | Domain | Sub-series | Feed | Native freq. | Orientation (higher = more buffer?) |
|---|---|---|---|---|---|
| 1 | Strategic reserve | (1a) SPR crude stocks, million bbl | EIA Weekly Petroleum Status Report / Monthly Energy Review | weekly | + |
| | | (1b) SPR coverage ratio = SPR stocks ÷ trailing-12-month mean daily crude inputs to refineries | EIA (both series) | weekly/monthly | + |
| 2 | Financial | (2) BIS credit-to-GDP gap, US, total private non-financial sector — **published values only, not re-derived** (Drehmann–Borio–Tsatsaronis one-sided HP, λ=400,000, per BIS WP 355) | BIS credit-gap statistics | quarterly | **−** (positive gap = froth, depleted absorption capacity) |
| 3 | Fiscal | (3a) Federal net interest outlays as % of federal revenues | OMB Historical Tables / CBO | annual (FY) | − |
| | | (3b) Federal debt held by the public as % of GDP | OMB/CBO (annual); FRED quarterly series for the companion | quarterly/annual | − |
| 4 | Corporate | (4a) Aggregate US nonfinancial net-debt/EBITDA | IMF GFSR chapters; S&P Global / rating-agency public summaries | sparse annual | − |
| | | (4b) Aggregate interest coverage ratio | same | sparse annual | + |
| 5 | Household | (5) Personal saving rate | BEA NIPA (Table 2.6 lineage) | monthly | + |
| 6 | Health capacity | (6) Hospital beds per 1,000 population | AHA Hospital Statistics / OECD Health Statistics | annual | + |
| 7 | Social / associational | (7) Union membership rate (% of employed wage and salary workers) | BLS Union Members annual release | annual | + |

**Frozen decisions and disclosed deviations:**

- **1b deviates from the Execution Handoff's letter** ("days-of-net-import-cover"). Reason, technical and disclosed now: the US became a net petroleum exporter mid-window (~2020), so days-of-*net-import* cover is undefined or sign-flipping over part of 2000–2026 and cannot enter a covariance statistic. The substitute — SPR stocks scaled by refinery crude throughput — is a well-defined intensity measure across the whole window and preserves the handoff's intent (a coverage ratio alongside the raw level). This is the only component-level deviation from the work order, and it is forced by arithmetic, not preference.
- **Fiscal proxy:** net-interest/revenue + debt/GDP is a pragmatic simplification. The conceptual anchor is the Ostry–Ghosh–Kim–Qureshi fiscal-fatigue / debt-limit framework (IMF SPN 2010; Ghosh et al., *Economic Journal* 2013): fiscal buffer as distance to a debt limit implied by a fiscal-reaction function. Estimating that reaction function is out of scope (Execution Handoff Limit 5); the proxy measures the same object crudely — how much of the state's absorption capacity is pre-committed — and the simplification is flagged as such wherever the index is reported.
- **Corporate gap rule and mechanical substitution:** GFSR/S&P summaries will yield an incomplete annual series. No interpolation. If, after Phase 3 collection, the corporate domain covers <60% of any analysis block's usable years, the domain switches **for the full window** to the BIS-published US nonfinancial-corporations credit-to-GDP series (orientation −). The switch is mechanical, not discretionary. If it triggers, the drop-corporate sensitivity run (S1) becomes mandatory reporting alongside every headline figure, because a BIS-credit corporate series shares construction with domain 2 and the induced pair correlation is partly artifactual.
- **Health substitution disclosed:** the conceptually preferred series (HHS hospital/ICU occupancy) begins ~2020 and cannot span the window. Beds per 1,000 is the long-window proxy. Known confound, stated now: its secular decline partly reflects the deliberate outpatient shift in care delivery, a technological/organizational trend, not extraction per se. The index measures buffer *level*, agnostic to cause; interpretation of this component must carry the confound.
- **Social-capital choice, pre-committed:** union membership rate, chosen on data-quality grounds — annual, complete, methodologically stable over the full window — over the GSS social-trust and neighbor-socializing items, which are biennial and carry a documented 2020–21 survey-mode comparability break. This is explicitly a data-quality-over-construct-validity trade: union density is an organized-associational-capacity proxy, not a measure of social connection at large. Mitigations, both frozen: the mandated drop-this-component run (S1) and a dedicated swap run substituting GSS social trust (S7).

---

## 4. Munitions: qualitative carve-out (frozen decision), and the convenience disclosure

**Decision: munitions are excluded from the quantitative index and carried qualitatively.** Three reasons, each sufficient. First, stock levels are classified; the public record consists of intermittent estimates (the CSIS "Last Rounds?" genre) that cannot support a 26-year series. Second, the available continuous proxy — procurement budgets — is a *flow into* the buffer that moves inversely to the stock (procurement surges follow depletion, as the 2026 THAAD/PAC-3 contracts demonstrate); injecting it as if it measured buffer level would put a mis-signed component into the covariance and corrupt the statistic in whichever direction the mis-signing happens to run. Third, a budget series measures political response, not physical reserve, and conflating the two is precisely the category error this framework is trying to stop making.

**The pre-emptive disclosure, in this spec's own voice:** the two buffers most central to the thesis — munitions and social capital — are the least measurable. Munitions are carved out entirely; social capital enters through a proxy chosen for data quality rather than construct fidelity. The index therefore leans on the domains that happen to be measurable, and a critic will say it measures what is convenient. The critic will be right about the composition, and we say it before they do. The consequence is a scope restriction accepted in advance: **a confirming result licenses the correlated-drain claim only over the seven measured domains and cannot be silently extended to munitions or to social capital broadly.** A disconfirming result, by contrast, withdraws the claim entirely — the asymmetry runs against the thesis, and that is the point of a pre-registration written by the side with the burden of proof.

---

## 5. Normalization, aggregation, and the test statistic (frozen)

**Normalization.** Each sub-series is oriented per the table in §3 (series where higher = less buffer are multiplied by −1) and z-scored against its own full-window (2000–2026, available observations) mean and standard deviation. Each domain's series is the unweighted mean of its sub-series z-scores (domains 1, 3, 4; single-sub-series domains pass through). Domain series are re-standardized to unit variance for the display composite only; the correlation statistic is scale-free and uses the domain series directly.

**Missing data.** No interpolation anywhere. First differences are computed only between adjacent available years. Pairwise correlations use pairwise-complete observations. A domain-pair is excluded from a block's average if it has fewer than 5 complete difference observations in that block; a domain is excluded from a block entirely if it covers <60% of that block's usable years. Every exclusion is logged in the Phase 3 results memo.

**The test statistic — choice made now.** The primary statistic is computed on **first differences** of the annual domain series (Δz), not levels. Justification: (i) normalized buffer levels are highly persistent, near-integrated series, and correlations of near-integrated series over short windows are dominated by incidental trend alignment — the spurious-regression problem (Granger–Newbold) in miniature; any two secularly declining series correlate strongly in levels regardless of whether their *drawdowns* have anything to do with each other. (ii) The mechanism claim is about synchronized drawdown — shocks and drains hitting multiple buffers in the same periods — and that is a statement about co-movement of *changes*. (iii) The descriptive layer already establishes that levels are jointly low; re-testing that in the guise of a mechanism test would be circular. **Levels are pre-named as the robustness alternate (S4)**, because a referee can fairly counter that differencing discards low-frequency co-drain; both are reported, the differences version is primary and verdict-bearing.

**Statistic S(t or block):** the unweighted mean of the pairwise Pearson correlations across all included domain pairs (21 pairs at full seven-domain strength) of the Δz series, computed over (a) the pre-defined blocks below (headline, verdict-bearing) and (b) trailing 10-year rolling windows (descriptive trajectory and consistency check only). The 10-year window is chosen over 8 to maximize observations per correlation estimate at annual frequency; the 8-year window is a named robustness run (S6). Spearman rank correlation is a named robustness run (S5), relevant because with 6–9 observations per block a single outlier year can dominate Pearson estimates.

**Blocks — mechanical construction.** The difference sample 2001–2026 (26 observations at most) is cut into near-equal thirds by date, with no reference to any data:
- **B1:** 2001–2009 (9 obs)
- **B2:** 2010–2017 (8 obs)
- **B3:** 2018–2026 (9 obs)

The headline contrast is **Δρ = ρ̄(B3, crisis-excluded) − ρ̄(B1, crisis-excluded)**, with B2 reported for shape (monotonicity is informative but not verdict-bearing).

**Inference.** Within each block, a moving-block bootstrap (block length 2 years, resampling year-vectors jointly across domains to preserve cross-sectional structure, 5,000 replications) yields the sampling distribution of ρ̄; the contrast's distribution is formed by independent resampling of the two blocks. The verdict-bearing interval is the one-sided 90% bootstrap confidence bound on Δρ.

---

## 6. Crisis windows, confirm/disconfirm criteria, and the power note (frozen)

**Crisis-window rule.** Common macro shocks mechanically spike difference-correlations across all domains at once; the claim under test is a rising trend **between** crises, not the trivial fact that crises are correlated events. Excluded years, defined by date now, with no discretion at Phase 3:

- **E = {2008, 2009, 2020, 2021, 2026}.**
- Justification: 2008–2009 = GFC acute phase (NBER recession Dec 2007–Jun 2009); 2020–2021 = COVID shock plus the extraordinary fiscal/monetary response that mechanically whipsawed the saving rate, credit gap, and fiscal series through 2021; 2026 = the Iran war — the event that motivated this project, whose inclusion would let the motivating crisis confirm the hypothesis by construction.
- Both variants are computed and reported: crisis-excluded (verdict-bearing) and crisis-included (S3, consistency).
- Effective crisis-excluded blocks: B1ex = 2001–2007 (7 obs); B2ex = 2010–2017 (8 obs); B3ex = {2018, 2019, 2022, 2023, 2024, 2025} (6 obs).

**CONFIRM requires all four of:**
- **C1.** Δρ > 0 (crisis-excluded point estimate).
- **C2.** The one-sided 90% bootstrap confidence bound on Δρ excludes zero.
- **C3.** Sign robustness: Δρ > 0 is preserved in every one of the seven drop-one-domain reruns (S1) and in ≥90% of 1,000 Dirichlet-weighted recomputations of the pair average (S2; symmetric Dirichlet, concentration 1, weights on domains, pair weight = product of its domains' weights renormalized).
- **C4.** Consistency: the crisis-included contrast is ≥ 0, and the Mann–Kendall trend statistic on the 10-year rolling series is non-negative.

**DISCONFIRM = anything short of all four.** Mapping to the verbatim commitment: failing C1/C2 is "flat"; failing C3 is "domain-idiosyncratic" (the appearance of co-drain produced by one or two domains, not a cross-domain property); failing C4 is inconsistency that a pre-registered test does not get to argue around. Per §0, disconfirmation withdraws the correlated-drain claim, full stop.

**Power note, stated against interest and in advance.** With 6–8 observations per crisis-excluded block, individual pairwise correlations carry standard errors near 0.4; averaging over 21 non-independent pairs narrows but does not tame this. The confirm bar is therefore demanding, and an indeterminate-but-suggestive result still withdraws the claim. This asymmetry is accepted deliberately: it is the price of a pre-commitment written by the compromised party, and it has a corollary a referee should also grant — a result that clears C1–C4 under this little power is correspondingly strong evidence, not a statistical accident to be waved off.

---

## 7. Sensitivity battery (enumerated, frozen)

- **S1.** Drop-one-domain: seven reruns of the full analysis, each excluding one domain. Feeds C3.
- **S2.** Weighting perturbation: 1,000 Dirichlet draws over domain weights, weighted mean pairwise correlation recomputed per draw. Feeds C3.
- **S3.** Crisis windows in/out: full analysis on both variants. Feeds C4.
- **S4.** Levels instead of first differences (the pre-named non-primary specification). Reported alongside the headline; not verdict-bearing, with one pre-commitment: if the levels version returns a *significantly opposite* sign (negative contrast, one-sided 90% bound excluding zero), that result must be reported in Dossier v3 immediately adjacent to the headline, not in an appendix.
- **S5.** Spearman in place of Pearson.
- **S6.** 8-year rolling window in place of 10-year (rolling series only; blocks unchanged).
- **S7.** Social-capital swap: union density → GSS social trust (biennial; pairwise-complete handling per §5; 2020–21 mode break noted and those obs already crisis-excluded).
- **S8.** Quarterly companion: domains 1 (SPR monthly), 2 (credit gap quarterly), 3b (debt/GDP quarterly), 5 (saving rate monthly) — the quarterly-native subset, 6 pairs, calendar-quarter frequency, 40-quarter trailing windows, same normalization and differencing logic. Descriptive and power-supporting only; it is also the measurement vehicle for Prediction P6. Its trailing windows unavoidably contain crisis quarters at both P6 endpoints; the ex-crisis variant is reported as an annotation, and no verdict over 2000–2026 rests on S8.

S1–S3 are gatekeeping (they feed C3/C4). S4–S8 are reported, not gatekeeping. Nothing outside S1–S8 is run against the frozen criteria; anything else computed in Phase 3 is labeled exploratory and carries no evidential status.

---

## 8. Display composite (non-verdict-bearing)

For visualization only, a **weakest-link composite** — the minimum oriented domain z-score at each date — is displayed alongside the cross-domain median. The min-function is the strong form of non-compensatory aggregation (Munda & Nardo 2009): a deep deficit in one buffer cannot be offset by surpluses elsewhere, which is precisely the thesis's own logic and, per the OECD/JRC *Handbook on Constructing Composite Indicators* (Nardo, Saisana, Saltelli et al. 2008), avoids the compensability objection that makes weighted-average composites "owe more to the craftsmanship of the modeller than to universally accepted scientific rules." The composite carries no inferential weight; the test statistic of §5 is the only verdict-bearing quantity.

---

## 9. Out of scope, listed as future work

Structural-break tests (Bai–Perron) on the correlation trajectory; cointegration / common-stochastic-trend analysis of buffer levels; DCC-GARCH dynamic conditional correlations; factor-model decomposition of common vs idiosyncratic drawdown variance; mixed-frequency (MIDAS-class) estimation that would use the quarterly-native series at full resolution. Each is acknowledged as what a full referee process would eventually demand of v0.2+; none is attempted in v0.1, and their absence is disclosed rather than papered over.

---

## 10. Novelty (bounded claim)

The contribution claimed is specific: **a rolling measure of cross-domain buffer covariance within one economy over time** (US, 2000–2026). Differentiation against the nearest prior art identified in Phase 1:

- **Gondauri Index (arXiv, 2026):** a diagnostics-first, *static, cross-country* macro-financial resilience composite — ranks countries at a point in time; measures no within-country, time-varying cross-domain covariance.
- **ECB sectoral systemic-risk-buffer composite indicators:** *financial-domain only* — sophisticated on bank-sector risk, no cross-domain reach into strategic reserves, fiscal, health, or associational capacity.
- **The static resilience/vulnerability lineage** (Cutter SoVI; Briguglio; FM Global Resilience Index; ND-GAIN): levels-composites ranking places, none measuring time-varying co-movement of buffer stocks.

Standing caveat, carried verbatim in intent from the Execution Handoff (Limit 9): this novelty finding was established within a bounded search. If prior art surfaces, the correct response is to cite and differentiate, not to defend priority.

---

## 11. Data-handling rules binding on Phase 3 (stated now)

Every series enters a CSV in the working directory with a source-URL-and-retrieval-date column per series. At least 10% of transcribed values are double-entered against source in a second pass; discrepancies trigger a full re-check of the affected series. Every data-quality compromise (gap, splice, vintage substitution, aggregation judgment) is logged in the results memo — the memo reports the outcome against §6's criteria *whichever way it goes*, and if disconfirm, drafts the withdrawal language for Dossier v3. If Phase 3 runs in an environment with direct API access (e.g., Claude Code on the human's machine pulling EIA/FRED/BIS directly), fetch scripts replace hand transcription and MUST be committed alongside the CSVs; that is strictly better, and Phase 5 audits the scripts. The CSVs, scripts, and memo ship together so the Phase 5 red team can attack the raw material, not a summary of it.

---

**Version: v0.1 · Date frozen: 2026-07-27**
No edits after external timestamp; amendments require a new versioned spec citing this one.
