import io
import json
import unittest

from prompts_hub.ecommerce import InMemoryEcommerceRepository, create_app


def request(app, path, method="GET", payload=None, query_string=""):
    body = json.dumps(payload).encode() if payload is not None else b""
    response = {}

    def start_response(status, headers):
        response["status"] = status
        response["headers"] = dict(headers)

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query_string,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": io.BytesIO(body),
    }
    response_body = b"".join(app(environ, start_response))
    return response, json.loads(response_body)


def request_raw(app, path, method="GET"):
    response = {}

    def start_response(status, headers):
        response["status"] = status
        response["headers"] = dict(headers)

    body = b"".join(app({"REQUEST_METHOD": method, "PATH_INFO": path}, start_response))
    return response, body


class EcommerceWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(InMemoryEcommerceRepository())

    def test_catalog_lists_available_products(self):
        response, payload = request(self.app, "/api/products")
        self.assertEqual(response["status"], "200 OK")
        self.assertGreaterEqual(len(payload["products"]), 3)
        self.assertEqual(payload["products"][0]["inventory"], 12)

    def test_checkout_reduces_inventory_and_updates_customer_profile(self):
        payload = {
            "customer_id": "cust-001",
            "email": "customer@example.com",
            "items": [
                {"product_id": "prod-001", "quantity": 2},
                {"product_id": "prod-003", "quantity": 1},
            ],
        }
        response, data = request(self.app, "/api/orders/checkout", "POST", payload)
        self.assertEqual(response["status"], "201 Created")
        self.assertEqual(data["order"]["status"], "confirmed")
        self.assertEqual(data["profile"]["customer_id"], "cust-001")
        self.assertIn("prod-001", data["profile"]["products"])
        self.assertEqual(data["order"]["email_alert"]["status"], "queued")
        self.assertEqual(data["order"]["items"][0]["quantity"], 2)

    def test_checkout_rejects_insufficient_inventory(self):
        payload = {
            "customer_id": "cust-001",
            "email": "customer@example.com",
            "items": [{"product_id": "prod-002", "quantity": 99}],
        }
        response, data = request(self.app, "/api/orders/checkout", "POST", payload)
        self.assertEqual(response["status"], "409 Conflict")
        self.assertEqual(data["error"]["code"], "insufficient_inventory")

    def test_static_ui_assets_are_served(self):
        response, body = request_raw(self.app, "/ui/ecommerce.html")
        self.assertEqual(response["status"], "200 OK")
        self.assertIn(b"Velora Market", body)


if __name__ == "__main__":
    unittest.main()
