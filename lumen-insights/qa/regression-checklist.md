# Manual regression checklist

Run before every release on `develop`, with `data/sales_sample.csv`. Updated after each release.

| # | Check | Last result |
|---|---|---|
| R1 | Revenue for a full month equals the sum of non-refunded lines | OK · 1.3.0 |
| R2 | Orders count ignores duplicate lines of the same order | OK · 1.3.0 |
| R3 | Average basket for a month with no sale shows 0.00 | OK · 1.3.0 |
| R4 | Top 5 products are ordered by revenue, ties by name | OK · 1.3.0 |
| R5 | Customers count for September 2026 | OK · 1.3.0 |
