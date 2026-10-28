import unittest
from datetime import date
from decimal import Decimal

from tests.helpers import sample_sales
from lumen_insights import kpis

SEPT = (date(2026, 9, 1), date(2026, 9, 30))


class KpisTest(unittest.TestCase):
    def setUp(self):
        self.sales = sample_sales()

    def test_revenue_for_september(self):
        self.assertEqual(kpis.revenue(self.sales, *SEPT), Decimal("200.00"))

    def test_orders_count(self):
        self.assertEqual(kpis.orders_count(self.sales, *SEPT), 3)

    def test_average_basket(self):
        self.assertEqual(kpis.average_basket(self.sales, *SEPT), Decimal("66.67"))

    def test_average_basket_empty_period(self):
        self.assertEqual(kpis.average_basket(self.sales, date(2026, 1, 1), date(2026, 1, 31)), Decimal("0.00"))

    def test_top_products(self):
        self.assertEqual(kpis.top_products(self.sales, *SEPT, n=2),
                         [("Chair", Decimal("110.00")), ("Lamp", Decimal("80.00"))])
