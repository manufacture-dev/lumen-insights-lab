---
id: 3
title: Average basket too low when an order is fully refunded
type: bug
status: in-review
area: kpi
owner: dev lead
branch: fix/3-refund-basket
review: waiting since 2026-10-23
blocks: 6
created: 2026-10-21
updated: 2026-10-23
---
Found while testing #1 on September data.

**Steps**: take a month with one fully refunded order; compare the average basket with revenue divided by the orders that were not refunded.

**Expected**: a fully refunded order does not count in the average basket. A partially refunded order still counts, with its net amount.

**Actual**: the fully refunded order is counted, so the average basket is too low.

Blocking for the 1.4 release: the export of #1 shows the wrong value.

## Log

- 2026-10-21 · qa: Found while testing #1. Blocking for 1.4.
- 2026-10-23 · dev lead: Fix on fix/3-refund-basket: orders with a refunded line are no longer counted in the average basket. CI is red, I'll look at it after the cohorts review.
