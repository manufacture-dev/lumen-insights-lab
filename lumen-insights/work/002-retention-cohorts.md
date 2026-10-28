---
id: 2
title: Monthly retention cohorts
type: story
status: in-review
area: cohorts
owner: developer
branch: feature/2-retention-cohort
review: waiting since 2026-10-22
created: 2026-10-09
updated: 2026-10-22
---
**As a** marketing manager, **I want** to see, for each month of first purchase, the share of customers who bought again in the following months, **so that** I can measure loyalty.

## Acceptance criteria

- Given customers grouped by the month of their first purchase, when I open the cohort table, then each row shows, for each later month, the share of the cohort who bought that month, rounded to two decimals.
- Refunded lines do not count as a purchase.
- A cohort with no later month shows an empty row.

## Log

- 2026-10-09 · product owner: Asked by marketing for the loyalty review.
- 2026-10-15 · dev lead: Approach agreed in the sprint planning. Ready for dev.
- 2026-10-22 · developer: Done on feature/2-retention-cohort, CI passes. Waiting for a reviewer.
