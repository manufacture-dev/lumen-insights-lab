"""Dashboard KPIs: revenue, orders, average basket, top products."""
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal

from .data import Sale

CENT = Decimal("0.01")


def in_period(sales: list[Sale], start: date, end: date) -> list[Sale]:
    return [s for s in sales if start <= s.day <= end]


def revenue(sales: list[Sale], start: date, end: date) -> Decimal:
    """Net revenue: refunded lines are excluded."""
    total = sum((s.amount for s in in_period(sales, start, end) if not s.refunded), Decimal("0"))
    return total.quantize(CENT)


def orders_count(sales: list[Sale], start: date, end: date) -> int:
    return len({s.order_id for s in in_period(sales, start, end)})


def average_basket(sales: list[Sale], start: date, end: date) -> Decimal:
    # Fully refunded orders must not lower the average basket (issue #3).
    refunded = {s.order_id for s in in_period(sales, start, end) if s.refunded}
    orders = len({s.order_id for s in in_period(sales, start, end)} - refunded)
    if orders == 0:
        return Decimal("0.00")
    return (revenue(sales, start, end) / orders).quantize(CENT)


def top_products(sales: list[Sale], start: date, end: date, n: int = 5) -> list[tuple[str, Decimal]]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for s in in_period(sales, start, end):
        if not s.refunded:
            totals[s.product] += s.amount
    ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    return [(p, v.quantize(CENT)) for p, v in ranked[:n]]


def customers_count(sales: list[Sale], start: date, end: date) -> int:
    return len(Counter(s.customer_id for s in in_period(sales, start, end)))
