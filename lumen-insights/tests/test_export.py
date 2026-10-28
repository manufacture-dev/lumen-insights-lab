import csv
import tempfile
import unittest
from datetime import date

from tests.helpers import sample_sales
from lumen_insights.export import HEADER, export_kpis_csv


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


class ExportTest(unittest.TestCase):
    def setUp(self):
        self.sales = sample_sales()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_export_writes_one_row(self):
        path = export_kpis_csv(self.sales, date(2026, 9, 1), date(2026, 9, 30), self.tmp.name)
        self.assertEqual(path.name, "kpis_2026-09-01_2026-09-30.csv")
        self.assertEqual(read(path), [HEADER, ["2026-09-01", "2026-09-30", "200.00", "3", "66.67", "2"]])

    def test_export_empty_period_has_header_only(self):
        path = export_kpis_csv(self.sales, date(2026, 1, 1), date(2026, 1, 31), self.tmp.name)
        self.assertEqual(read(path), [HEADER])
