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
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lumen Insights · KPIs</title>
<style>
  :root {{ --bg: #f5f6f8; --card: #fff; --ink: #1d2433; --muted: #667085; --line: #e4e7ec; --brand: #3b5bdb; --brand-ink: #fff; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
  header {{ background: var(--ink); color: #fff; padding: 14px 28px; display: flex; align-items: center; gap: 10px; }}
  header .logo {{ width: 26px; height: 26px; border-radius: 7px; background: linear-gradient(135deg, #5c7cfa, #22b8cf); }}
  header h1 {{ font-size: 17px; font-weight: 600; margin: 0; letter-spacing: .01em; }}
  header span {{ color: #aab3c5; font-size: 13px; margin-left: auto; }}
  main {{ max-width: 960px; margin: 0 auto; padding: 28px; display: flex; flex-direction: column; gap: 22px; }}
  h2 {{ font-size: 22px; margin: 0; }}
  form {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; display: flex; flex-wrap: wrap; align-items: end; gap: 14px; }}
  form label {{ display: flex; flex-direction: column; gap: 4px; font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }}
  input[type=date] {{ font: inherit; color: var(--ink); padding: 8px 10px; border: 1px solid var(--line); border-radius: 8px; }}
  button, .button {{ font: inherit; font-weight: 600; border: 0; border-radius: 8px; padding: 9px 16px; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; }}
  button {{ background: var(--brand); color: var(--brand-ink); }}
  .button {{ background: var(--card); color: var(--brand); border: 1px solid var(--brand); }}
  #kpis {{ width: 100%; border-collapse: separate; }}
  #kpis tbody {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; }}
  #kpis tr {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; display: flex; flex-direction: column-reverse; gap: 4px; }}
  #kpis th {{ text-align: left; font-size: 13px; font-weight: 500; color: var(--muted); }}
  #kpis td {{ font-size: 28px; font-weight: 700; font-variant-numeric: tabular-nums; }}
  .bar {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }}
  .period {{ color: var(--muted); }}
  .empty {{ background: var(--card); border: 1px dashed var(--line); border-radius: 12px; padding: 28px; color: var(--muted); text-align: center; }}
  footer {{ color: var(--muted); font-size: 12px; text-align: center; padding: 8px 0 24px; }}
</style></head>
<body>
<header><div class="logo" aria-hidden="true"></div><h1>Lumen Insights</h1><span>Retail dashboard</span></header>
<main>
<h2>Key figures</h2>
<form method="get" action="/">
  <label for="start">Start<input type="date" id="start" name="start" value="{start}" required></label>
  <label for="end">End<input type="date" id="end" name="end" value="{end}" required></label>
  <button type="submit">Show</button>
</form>
{body}
</main>
<footer>Lumen Retail · fictional data for training</footer>
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
    period = f"{start.isoformat()} to {end.isoformat()}"
    return (f'<div class="bar"><span class="period">Period: {period}</span>'
            f'<a class="button" id="export" href="{link}">Export CSV</a></div>\n'
            f'<table id="kpis"><tbody>{cells}</tbody></table>')


EMPTY = '<p class="empty">Pick a period to see its key figures.</p>'


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
                body = kpi_table(sales, date.fromisoformat(start), date.fromisoformat(end)) if start and end else EMPTY
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
    print(f"Dashboard on http://127.0.0.1:{args.port}/ (Ctrl-c to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
