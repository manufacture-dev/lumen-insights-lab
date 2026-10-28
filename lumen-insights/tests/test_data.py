import unittest
from pathlib import Path

from tests.helpers import sale  # noqa: F401  (puts src on the path)
from lumen_insights.data import load_sales

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sales_sample.csv"


class DataTest(unittest.TestCase):
    def test_sample_loads(self):
        sales = load_sales(SAMPLE)
        self.assertGreater(len(sales), 100)
        self.assertTrue(any(s.refunded for s in sales))
