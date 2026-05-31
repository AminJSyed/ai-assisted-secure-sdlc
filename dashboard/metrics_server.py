from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import subprocess

METRICS_PATH = Path("dashboard/secure-sdlc-metrics.prom")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ["/metrics", "/"]:
            self.send_response(404)
            self.end_headers()
            return

        if not METRICS_PATH.exists():
            subprocess.run(["make", "dashboard"], check=False)

        data = METRICS_PATH.read_text() if METRICS_PATH.exists() else ""
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9200), Handler)
    print("Secure SDLC metrics server running on http://localhost:9200/metrics")
    server.serve_forever()
