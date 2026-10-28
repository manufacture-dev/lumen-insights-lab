# Lumen Insights

KPIs behind the Lumen Retail analytics dashboard: revenue, orders, average basket, top products, and their CSV export. Lumen Retail is a fictional company; this repository is a training lab.

## Run

Python 3.11 or later, nothing to install.

```bash
scripts/ci.sh                 # tests of the current checkout
scripts/ci.sh <branch>        # tests of another branch
```

## Layout

| Path | What |
|---|---|
| `src/lumen_insights/` | The KPI code |
| `tests/` | Unit tests (`unittest`) |
| `data/sales_sample.csv` | A synthetic extract of sales lines |
| `work/` | The ticket board: one file per ticket, see [work/README.md](work/README.md) |
| `docs/` | Release process, review checklist and specs |
| `qa/` | Test plans and the manual regression checklist |
| `scripts/ci.sh` | The checks run before a merge |

## How we work

Tickets live in `work/` with a status (refinement, ready-for-dev, in-progress, in-review, ready-for-qa, done). Branches start from `develop` and wait for review before being merged; releases are cut from `develop` to `main` every two weeks, see [docs/release.md](docs/release.md).
