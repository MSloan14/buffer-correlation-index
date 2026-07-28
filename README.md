# buffer-correlation-index

A **pre-registered** test of a cross-domain buffer-correlation hypothesis.

> **Status: specification frozen before data contact.**
> The analysis plan in [`prereg/`](prereg/) is committed *before* any data in
> [`data/raw/`](data/raw/) is fetched or inspected. The git history is the evidence of that
> ordering: the commit that freezes the specification precedes the commit that introduces the data.

---

## Purpose

This repository exists so that the hypothesis, the analysis plan, and the stopping rules are all on
the public record **before** the data that will test them has been seen. That ordering is the entire
point. A result is only as credible as the commitment that preceded it, and a commitment is only
credible if it is timestamped by something the author cannot quietly revise.

<!-- TODO: state the hypothesis in one paragraph, in plain language, once the spec is drafted. -->

## Provenance

<!-- TODO: Fill in before publication.
     - Who ran this, and in what capacity.
     - Where each data series came from, and why that source was chosen.
     - What was known about the data at the moment the specification was frozen
       (ideally: nothing beyond its existence, schema, and date coverage).
     - Any prior exposure to the data or to related results, disclosed honestly.
     - Funding, affiliations, or conflicts of interest, if any.
-->

_Not yet written._

## Contents

| Path | What lives here |
|---|---|
| [`prereg/`](prereg/) | Frozen specifications and slates. Written before data contact; never edited after freezing, only superseded by a new dated file. |
| [`data/raw/`](data/raw/) | Untouched fetch output, exactly as retrieved. Never hand-edited. |
| [`data/processed/`](data/processed/) | Analysis-ready CSVs, produced only by scripts in [`scripts/`](scripts/). |
| [`data/SOURCES.md`](data/SOURCES.md) | One row per series: name, source URL, retrieval date, notes. |
| [`scripts/fetch/`](scripts/fetch/) | Retrieval code. What produced `data/raw/`. |
| [`scripts/analysis/`](scripts/analysis/) | Analysis code implementing the frozen specification. |
| [`results/`](results/) | Outputs. Everything here is generated after the freeze. |

Data and scripts are **committed deliberately**, not ignored. An audit trail that omits the inputs
or the code is not an audit trail.

## How to verify the timestamp

<!-- TODO: Expand once the repository is published and the freeze commit exists. -->

The claim to verify is: *the specification was committed before the data was fetched.* Three
independent ways to check, in increasing order of strength:

1. **Commit order and dates.** `git log --format='%H %ad %s' --date=iso` lists every commit with its
   author date. The `prereg/` freeze commit should precede any commit touching `data/raw/`.
   Caveat: author dates are supplied by the committer's machine and can be set to anything. This is
   the weakest form of evidence and is listed only for completeness.

2. **The published record.** Once pushed, the commit's appearance in the public repository is
   timestamped by a third party rather than by the author.

_Not yet written: the specific verification steps depend on which mechanism is used. This section
must be completed before the repository is presented as a pre-registration._

## Pre-registration integrity

- Files in `prereg/` are **append-only**. A frozen specification is never edited. If the plan
  changes, a new dated file is added and the change is disclosed, with the original left intact.
- Deviations from the frozen plan get documented in `results/`, alongside the result they affected.
- If the analysis is run more than once, every run is reported, not just the informative one.
