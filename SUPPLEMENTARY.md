# Supplementary material

**Everything in this file is supplementary, added after the freeze, descriptive
only, and excluded from Study 2 scoring.**

Nothing here touches the frozen core. It does not change the pre-specified eight
domains, the ratchet criterion, or anything in
[`prereg/`](prereg/). The registration of 2026-08-01 does not cover any of it,
and none of it can support a verdict.

The reason for keeping this separate is simple. The core was fixed before the
data was seen; this was not. Mixing them would make the whole thing
unfalsifiable in the way the project exists to avoid.

| Status label | Meaning |
|---|---|
| **Supplementary** | Not part of the pre-registration |
| **Post-freeze** | Added after 2026-08-01, with the data gate open |
| **Descriptive only** | Charted and described; never scored |
| **Excluded from Study 2** | Cannot enter episode detection or rebuild scoring |

---

## A. Descriptive buffer companions

Charted alongside Study 1, **visually and textually separated from the core
eight**. Different panel styling, a section of their own, and a label on every
chart.

### A1 · NCES student–teacher ratios (education)

Federal, public, long coverage. A staffing-capacity measure for schools, in the
same spirit as the nurses companion in A2.

- **Source:** NCES Digest of Education Statistics
- **Access:** reachable — `nces.ed.gov` responds
- **Orientation:** lower ratio = more capacity, so the series is **inverted**
  before charting
- **Confound to state on the chart:** ratio changes reflect enrolment shifts and
  policy on class size, not only staffing capacity. A falling ratio can mean
  more teachers or fewer students, and those are different stories.

### A2 · BLS OES registered nurses per capita (domain-6 staffing companion)

Carried per [`docs/domain-6-decision.md`](docs/domain-6-decision.md). **OECD
hospital beds per 1,000 remains the domain-6 primary** and is the only one of
the two that enters Study 2.

- **Source:** BLS Occupational Employment and Wage Statistics
- **Access:** **BLOCKED.** `bls.gov` and `download.bls.gov` return 403 from this
  machine, sandboxed and unsandboxed. See the access notes below.
- **Confound to state on the chart:** nurse employment tracks **demand** as well
  as capacity. Hiring rises when admissions rise, so the series can move up
  exactly when a buffer measure should show strain. This confound points the
  opposite way to the beds series, which is why both are carried.

### A3 · NERC regional reserve margins (grid)

- **Source:** NERC Long-Term Reliability Assessment
- **Access:** reachable — `nerc.com` responds
- **Per-region series only. No national splice.** Spec v0.2 §3.2 rejected a
  national grid series precisely because the regional-entity map was
  reorganised repeatedly across the window. Constructing one anyway here would
  reintroduce the error the frozen spec declined to make.
- **Methodology breaks annotated on-chart:** ERO standup 2006, RFC formation,
  SPP RE dissolution 2018, FRCC dissolution into SERC 2019, and the shift
  between anticipated and prospective margin definitions.
- **NERC LTRA risk categories** carried as a qualitative overlay, not a numeric
  series.

---

## B. Slate evidence logs

Dated logs of **events, not arguments**, in [`results/watch/`](results/watch/).

Each prediction resolves against its frozen definition in
[`prereg/slate-v1.1.md`](prereg/slate-v1.1.md). These logs are the record that
feeds that resolution. They are not a running tally, and accumulating suggestive
entries does not resolve anything early.

| Log | Prediction | Resolution |
|---|---|---|
| [`results/watch/p1.md`](results/watch/p1.md) | SPR exchange-return performance | 2027-12-31 |
| [`results/watch/p2.md`](results/watch/p2.md) | Systemic private-credit event | 2029-12-31 |
| [`results/watch/p3.md`](results/watch/p3.md) | Term premium | 2028-01-31 |
| [`results/watch/p4.md`](results/watch/p4.md) | Overdose decline | ~2027-06-30 |
| [`results/watch/p5.md`](results/watch/p5.md) | Buffer-binding de-escalation | 2026-12-31 |
| [`results/watch/p6.md`](results/watch/p6.md) | Index out-of-sample trajectory | 2029-03-31 |

**Logging rules.** Every entry carries a date and a source. Events are recorded
whichever way they cut. An entry that looks bad for the thesis is logged in the
same words as one that looks good. No entry may reinterpret a frozen definition.

---

## C. Case-tracing candidates

Mechanism narratives with documentable physical coupling. **Not statistics**, and
they carry no evidential weight for any prediction or hypothesis.

**Listed as candidates only. The essays are authored outside this pipeline.**

### C1 · Munitions — one interceptor inventory serving two theaters

The physical coupling is concrete: a finite stock of interceptors, drawn on by
two simultaneous demands. Sourced from CSIS public reporting. Appears as the
qualitative section of Study 1, outside the quantitative set, as Index Spec v0.2
§4 already specifies. Munitions stock levels are classified; this is narrative
tracing, and no series will be constructed.

### C2 · Grid — datacenter and electrification load growth

Documented demand growth against reserve margins, using the A3 regional series
as context. The coupling is physical and traceable: specific facilities, specific
interconnection queues, specific margins.

---

## Access notes, 2026-08-02

Recorded because reproducibility depends on it, and because a reader trying to
rebuild this should know which sources were obtainable.

| Source | Status from this machine |
|---|---|
| NCES | Reachable |
| NERC | Reachable |
| EIA (bulk CSV) | Reachable |
| OECD SDMX | Reachable |
| Treasury FiscalData | Reachable |
| USDA FAS | Reachable with a browser user-agent |
| **BLS** (`www` and `download`) | **403 — blocked, sandboxed and unsandboxed** |
| **FRED** (all `stlouisfed.org`) | **Network timeout — blocked** |
| BEA | Reachable, requires a registration key |
| USDA NASS | Reachable, requires a registration key |

The BLS block affects **domain 7 (union density) in the frozen core** as well as
the A2 companion. Domain 7 is not supplementary and cannot be dropped; its
handling is an open item, tracked outside this file.
