"""CSV export of the dashboard KPIs for a period (issue #1)."""
import csv
from datetime import date
from pathlib import Path

from . import kpis
from .data import Sale

HEADER = ["start", "end", "revenue_eur", "orders", "average_basket_eur", "customers"]


def export_kpis_csv(sales: list[Sale], start: date, end: date, folder) -> Path:
    path = Path(folder) / f"kpis_{start.isoformat()}_{end.isoformat()}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        if kpis.orders_count(sales, start, end):
            writer.writerow([
                start.isoformat(),
                end.isoformat(),
                f"{kpis.revenue(sales, start, end):.2f}",
                kpis.orders_count(sales, start, end),
                f"{kpis.average_basket(sales, start, end):.2f}",
                kpis.customers_count(sales, start, end),
            ])
    return path
