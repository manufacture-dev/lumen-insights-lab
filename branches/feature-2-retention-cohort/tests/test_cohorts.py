import unittest

from tests.helpers import sample_sales
from lumen_insights.cohorts import retention_by_month


class CohortsTest(unittest.TestCase):
    def test_retention_by_month(self):
        self.assertEqual(retention_by_month(sample_sales()), {
            "2026-09": {"2026-10": 0.5},
            "2026-10": {},
        })
