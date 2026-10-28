import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lumen_insights.data import Sale  # noqa: E402


def sale(order, day, customer, product, qty, price, category="home", refunded=False):
    return Sale(order, date.fromisoformat(day), customer, product, category, qty, Decimal(price), refunded)


def sample_sales():
    return [
        sale("O1", "2026-09-02", "C1", "Lamp", 1, "40.00"),
        sale("O1", "2026-09-02", "C1", "Bulb", 4, "2.50"),
        sale("O2", "2026-09-10", "C2", "Chair", 2, "55.00", category="furniture"),
        sale("O3", "2026-09-21", "C1", "Lamp", 1, "40.00"),
        sale("O4", "2026-10-03", "C3", "Desk", 1, "180.00", category="furniture"),
        sale("O5", "2026-10-05", "C2", "Bulb", 10, "2.50"),
    ]
