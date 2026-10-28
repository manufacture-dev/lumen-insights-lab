# Lumen Insights

KPIs behind the Lumen Retail analytics dashboard: revenue, orders, average basket, top products, and their CSV export. Lumen Retail is a fictional company; this repository is a training lab.

## Run

Python 3.11 or later, no dependency at runtime.

```bash
pip install pytest
pytest -q
```

## Layout

| Path | What |
|---|---|
| `src/lumen_insights/` | The KPI code |
| `tests/` | Unit tests, run by CI on every push and pull request |
| `data/sales_sample.csv` | A synthetic extract of sales lines |
| `docs/` | Release process and specs |
| `qa/` | Test plans and the manual regression checklist |

## How we work

Issues carry a `status:` label (refinement, ready-for-dev, in-progress, in-review, ready-for-qa, done). Branches start from `develop`; releases are cut from `develop` to `main` every two weeks, see [docs/release.md](docs/release.md).
