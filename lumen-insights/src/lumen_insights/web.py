"""Dashboard page: the KPIs of a period, with a link to their CSV export (issue #1).

Run: python3 -m lumen_insights.web [--port 8000] [--data data/sales_sample.csv]
"""
import argparse
import html
import tempfile
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

from . import kpis
from .data import load_sales
from .export import export_kpis_csv

DEFAULT_DATA = Path(__file__).resolve().parents[2] / "data" / "sales_sample.csv"

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Lumen Insights · KPIs</title></head>
<body>
<h1>Lumen Insights · KPIs</h1>
<form method="get" action="/">
  <label for="start">Start</label> <input type="date" id="start" name="start" value="{start}" required>
  <label for="end">End</label> <input type="date" id="end" name="end" value="{end}" required>
  <button type="submit">Show</button>
</form>
{body}
</body></html>
"""


def kpi_table(sales, start: date, end: date) -> str:
    rows = [
        ("Revenue (EUR)", f"{kpis.revenue(sales, start, end):.2f}"),
        ("Orders", kpis.orders_count(sales, start, end)),
        ("Average basket (EUR)", f"{kpis.average_basket(sales, start, end):.2f}"),
        ("Customers", kpis.customers_count(sales, start, end)),
    ]
    cells = "".join(f"<tr><th>{name}</th><td>{value}</td></tr>" for name, value in rows)
    link = "/export?" + urlencode({"start": start.isoformat(), "end": end.isoformat()})
    return f'<table id="kpis">{cells}</table>\n<p><a id="export" href="{link}">Export CSV</a></p>'


def make_handler(sales):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlparse(self.path)
            query = {k: v[0] for k, v in parse_qs(url.query).items()}
            start, end = query.get("start", ""), query.get("end", "")
            if url.path == "/export" and start and end:
                with tempfile.TemporaryDirectory() as folder:
                    path = export_kpis_csv(sales, date.fromisoformat(start), date.fromisoformat(end), folder)
                    self.send(path.read_bytes(), "text/csv; charset=utf-8", path.name)
            elif url.path == "/":
                body = kpi_table(sales, date.fromisoformat(start), date.fromisoformat(end)) if start and end else ""
                page = PAGE.format(start=html.escape(start), end=html.escape(end), body=body)
                self.send(page.encode("utf-8"), "text/html; charset=utf-8")
            else:
                self.send_error(404)

        def send(self, content: bytes, content_type: str, filename: str | None = None):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            if filename:
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    return Handler


def main():
    parser = argparse.ArgumentParser(description="Serve the KPI dashboard.")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(load_sales(args.data)))
    print(f"Dashboard on http://127.0.0.1:{args.port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
