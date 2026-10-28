from pathlib import Path

from lumen_insights.data import load_sales

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sales_sample.csv"


def test_sample_loads():
    sales = load_sales(SAMPLE)
    assert len(sales) > 100
    assert any(s.refunded for s in sales)
