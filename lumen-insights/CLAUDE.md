# Lumen Insights

Python 3.11, stdlib only. Run the tests with `scripts/ci.sh`. Start the dashboard with `PYTHONPATH=src python3 -m lumen_insights.web`.

- Work from a ticket in `work/`. Branch `feature/<n>-<slug>` or `fix/<n>-<slug>` from `develop`.
- Before coding a story, write its spec with the spec-from-ticket skill.
- Amounts are in euros with two decimals; use `Decimal`, never `float`.
