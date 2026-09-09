"""
Customer Service API
Standard Python REST-style HTTP service using only the Python standard library.
No third-party packages are required.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import urlparse

HOST = "0.0.0.0"
PORT = 8080

customers = [
    {"id": 1, "name": "Rahul", "email": "rahul@example.com"},
    {"id": 2, "name": "Priya", "email": "priya@example.com"},
]


class CustomerHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self.send_json(200, {
                "application": "customer-service",
                "message": "Customer Service API is running"
            })
            return

        if path == "/health":
            self.send_json(200, {"status": "UP"})
            return

        if path == "/customers":
            self.send_json(200, customers)
            return

        if path.startswith("/customers/"):
            try:
                customer_id = int(path.split("/")[-1])
            except ValueError:
                self.send_json(400, {"message": "Invalid customer id"})
                return

            customer = next(
                (c for c in customers if c["id"] == customer_id),
                None
            )

            if customer is None:
                self.send_json(404, {"message": "Customer not found"})
            else:
                self.send_json(200, customer)
            return

        self.send_json(404, {"message": "Endpoint not found"})

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/customers":
            self.send_json(404, {"message": "Endpoint not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"message": "Invalid JSON"})
            return

        name = payload.get("name")
        email = payload.get("email")

        if not name or not email:
            self.send_json(
                400,
                {"message": "name and email are required"}
            )
            return

        new_customer = {
            "id": max((c["id"] for c in customers), default=0) + 1,
            "name": name,
            "email": email,
        }
        customers.append(new_customer)

        self.send_json(201, new_customer)

    def log_message(self, format, *args):
        print(f"[HTTP] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), CustomerHandler)
    print(f"customer-service is running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping customer-service...")
    finally:
        server.server_close()
