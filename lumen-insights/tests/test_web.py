import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from tests.helpers import sample_sales
from lumen_insights.web import make_handler


class WebTest(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(sample_sales()))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def test_page_shows_the_kpis_of_a_period(self):
        with urlopen(self.base + "/?start=2026-09-01&end=2026-09-30") as r:
            page = r.read().decode("utf-8")
        self.assertIn('<td>200.00</td>', page)
        self.assertIn('href="/export?start=2026-09-01&end=2026-09-30"', page)

    def test_export_returns_the_csv(self):
        with urlopen(self.base + "/export?start=2026-09-01&end=2026-09-30") as r:
            self.assertEqual(r.headers["Content-Disposition"], 'attachment; filename="kpis_2026-09-01_2026-09-30.csv"')
            lines = r.read().decode("utf-8").splitlines()
        self.assertEqual(lines[1], "2026-09-01,2026-09-30,200.00,3,66.67,2")
