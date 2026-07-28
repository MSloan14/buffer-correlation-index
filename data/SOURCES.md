# Data sources

One row per series. Fill this in **at the moment of retrieval**, from the fetch script's own output.
Do not backfill from memory later — a provenance record reconstructed after the fact is not a
provenance record.

| Series | Source URL | Retrieval date (UTC) | Notes |
|---|---|---|---|
| _none yet_ | | | |

## Column meanings

- **Series** — the identifier used for this data everywhere else in the repo, including in
  `data/raw/` filenames and in the frozen specification. Keep it stable.
- **Source URL** — the exact URL fetched, including query parameters. If the data came from an API,
  record the full request. If it came from a download page rather than a direct link, record both.
- **Retrieval date (UTC)** — when the fetch actually ran, in UTC, `YYYY-MM-DD` or with a time if the
  series updates intraday. Not the date the data covers.
- **Notes** — anything a reader would need to reproduce or distrust this row: revision or vintage of
  the series, licence and redistribution terms, known gaps or discontinuities, units, and whether
  the source revises historical values after publication.

## Standing rules

1. Nothing enters `data/raw/` without a row here.
2. Files in `data/raw/` are never hand-edited. If a series is wrong, re-fetch it and add a new row.
3. If a source revises its history, that is a finding worth recording, not an inconvenience to
   smooth over. Add a row for the new vintage and keep the old one.
