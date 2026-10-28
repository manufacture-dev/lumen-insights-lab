# Test plan · Top products (1.3.0)

Story: top 5 products by revenue for a period. Data: `data/sales_sample.csv`.

| Case | Criterion | Steps | Expected | Result |
|---|---|---|---|---|
| T1 | Given a month with sales, when I open top products, then I see 5 products by revenue | Period 2026-09 | 5 rows, revenue descending | OK |
| T2 | Refunded lines are not counted | Period with a refund | Refunded product revenue lowered | OK |
| T3 | Ties are ordered by name | Two products with equal revenue | Alphabetical order | OK |
| T4 (edge) | Fewer than 5 products in the period | One-week period | As many rows as products | OK |
