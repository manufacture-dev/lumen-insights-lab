"""Load sales lines from the CSV extract."""
import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Sale:
    order_id: str
    day: date
    customer_id: str
    product: str
    category: str
    quantity: int
    unit_price: Decimal
    refunded: bool

    @property
    def amount(self) -> Decimal:
        return self.unit_price * self.quantity


def load_sales(path) -> list[Sale]:
    with open(path, newline="", encoding="utf-8") as f:
        return [
            Sale(
                order_id=row["order_id"],
                day=date.fromisoformat(row["date"]),
                customer_id=row["customer_id"],
                product=row["product"],
                category=row["category"],
                quantity=int(row["quantity"]),
                unit_price=Decimal(row["unit_price"]),
                refunded=row["refunded"] == "true",
            )
            for row in csv.DictReader(f)
        ]
