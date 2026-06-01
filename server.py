#!/usr/bin/env python3
"""Lab chemical ordering tracker — run with: python3 server.py"""

import json
import os
import uuid
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

DATA_FILE = os.path.join(os.path.dirname(__file__), "orders.json")


def load_orders():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_orders(orders):
    with open(DATA_FILE, "w") as f:
        json.dump(orders, f, indent=2)


def read_body(handler):
    length = int(handler.headers.get("Content-Length", 0))
    return handler.rfile.read(length).decode()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress default access log noise

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            html_path = os.path.join(os.path.dirname(__file__), "index.html")
            with open(html_path, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/orders":
            orders = load_orders()
            # sort: pending first, then ordered, then received; within each by date desc
            priority = {"Pending": 0, "Ordered": 1, "Received": 2}
            orders.sort(key=lambda o: (priority.get(o.get("status", "Pending"), 3), o.get("date", "")))
            self.send_json(orders)

        elif path == "/api/export":
            import csv, io
            orders = load_orders()
            buf = io.StringIO()
            fields = ["id", "chemical", "cas", "supplier", "catalog", "quantity",
                      "urgency", "requested_by", "notes", "status", "date", "status_updated"]
            w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(orders)
            body = buf.getvalue().encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Disposition", "attachment; filename=lab_orders.csv")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/orders":
            data = json.loads(read_body(self))
            orders = load_orders()
            order = {
                "id": str(uuid.uuid4())[:8],
                "chemical": data.get("chemical", "").strip(),
                "cas": data.get("cas", "").strip(),
                "supplier": data.get("supplier", "").strip(),
                "catalog": data.get("catalog", "").strip(),
                "quantity": data.get("quantity", "").strip(),
                "urgency": data.get("urgency", "Normal"),
                "requested_by": data.get("requested_by", "").strip(),
                "notes": data.get("notes", "").strip(),
                "status": "Pending",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status_updated": "",
            }
            orders.append(order)
            save_orders(orders)
            self.send_json(order, 201)

        elif path == "/api/status":
            data = json.loads(read_body(self))
            orders = load_orders()
            for o in orders:
                if o["id"] == data.get("id"):
                    o["status"] = data.get("status", o["status"])
                    o["status_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    break
            save_orders(orders)
            self.send_json({"ok": True})

        elif path == "/api/delete":
            data = json.loads(read_body(self))
            orders = load_orders()
            orders = [o for o in orders if o["id"] != data.get("id")]
            save_orders(orders)
            self.send_json({"ok": True})

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    port = 8765
    print(f"Lab Orders running at http://localhost:{port}")
    print("Press Ctrl+C to stop.")
    HTTPServer(("", port), Handler).serve_forever()
