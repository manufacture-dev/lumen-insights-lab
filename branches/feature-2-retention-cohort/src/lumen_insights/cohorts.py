"""Monthly retention cohorts (issue #2)."""
from collections import defaultdict

from .data import Sale


def month(day) -> str:
    return f"{day.year:04d}-{day.month:02d}"


def retention_by_month(sales: list[Sale]) -> dict[str, dict[str, float]]:
    """For each first-purchase month, the share of its customers who bought again in each later month."""
    first: dict[str, str] = {}
    active: dict[str, set[str]] = defaultdict(set)
    for s in sorted(sales, key=lambda s: s.day):
        if s.refunded:
            continue
        m = month(s.day)
        first.setdefault(s.customer_id, m)
        active[m].add(s.customer_id)
    cohorts: dict[str, set[str]] = defaultdict(set)
    for customer, m in first.items():
        cohorts[m].add(customer)
    table = {}
    for cohort, members in sorted(cohorts.items()):
        table[cohort] = {
            m: round(len(members & customers) / len(members), 2)
            for m, customers in sorted(active.items())
            if m > cohort
        }
    return table
