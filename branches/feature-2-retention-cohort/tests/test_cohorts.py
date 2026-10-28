from lumen_insights.cohorts import retention_by_month


def test_retention_by_month(sales):
    assert retention_by_month(sales) == {
        "2026-09": {"2026-10": 0.5},
        "2026-10": {},
    }
