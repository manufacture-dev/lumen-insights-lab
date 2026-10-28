# Spec · #1 Export the dashboard KPIs to CSV

## Intent

Finance wants the period KPIs in a file they can open in a spreadsheet, instead of copying them from the dashboard.

## Approach

`export_kpis_csv(sales, start, end, folder)` writes `kpis_<start>_<end>.csv` with one header row and one row of values, reusing the existing KPI functions. Amounts with two decimals and a dot.

## Impacts

None on existing KPIs. New module `export.py`.

## Open questions

- Should a period with no sale produce an empty file or a header only? Header only, as agreed with the PO in the issue.
- Validation of the dates is left to the caller for now.
