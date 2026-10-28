import csv
from datetime import date

from lumen_insights.export import HEADER, export_kpis_csv


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def test_export_writes_one_row(sales, tmp_path):
    path = export_kpis_csv(sales, date(2026, 9, 1), date(2026, 9, 30), tmp_path)
    assert path.name == "kpis_2026-09-01_2026-09-30.csv"
    assert read(path) == [HEADER, ["2026-09-01", "2026-09-30", "200.00", "3", "66.67", "2"]]


def test_export_empty_period_has_header_only(sales, tmp_path):
    path = export_kpis_csv(sales, date(2026, 1, 1), date(2026, 1, 31), tmp_path)
    assert read(path) == [HEADER]
