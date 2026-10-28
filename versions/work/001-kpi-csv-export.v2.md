---
id: 1
title: Export the dashboard KPIs to CSV
type: story
status: ready-for-dev
area: export
owner: developer
created: 2026-10-08
updated: 2026-10-13
---
**As a** finance analyst, **I want** to export the KPIs of a period to a CSV file, **so that** I can work on them in a spreadsheet without copying them from the dashboard.

## Acceptance criteria

- Given a period with sales, when I export, then I get `kpis_<start>_<end>.csv` with a header row and one row: start, end, revenue, orders, average basket, customers.
- Given a period with no sale, when I export, then the file has the header row only.
- Given an end date before the start date, when I export, then I get a clear error and no file is written.
- Amounts have two decimals and a dot as decimal separator.
- Refunded lines are excluded from the revenue and the average basket.
- Customers is the number of distinct customers who ordered in the period.

## Out of scope

Excel format, scheduling the export.

## Log

- 2026-10-08 · product owner: Finance asked for it after the September close. Header only for an empty period: agreed with QA.
- 2026-10-13 · dev lead: Estimated 3 points. Ready for dev.
