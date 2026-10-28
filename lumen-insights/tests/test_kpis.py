from datetime import date
from decimal import Decimal

from lumen_insights import kpis

SEPT = (date(2026, 9, 1), date(2026, 9, 30))


def test_revenue_for_september(sales):
    assert kpis.revenue(sales, *SEPT) == Decimal("200.00")


def test_orders_count(sales):
    assert kpis.orders_count(sales, *SEPT) == 3


def test_average_basket(sales):
    assert kpis.average_basket(sales, *SEPT) == Decimal("66.67")


def test_average_basket_empty_period(sales):
    assert kpis.average_basket(sales, date(2026, 1, 1), date(2026, 1, 31)) == Decimal("0.00")


def test_top_products(sales):
    assert kpis.top_products(sales, *SEPT, n=2) == [("Chair", Decimal("110.00")), ("Lamp", Decimal("80.00"))]
