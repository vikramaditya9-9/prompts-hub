"""E-commerce catalog and order APIs for the prompts-hub demo."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from threading import Lock
from typing import Any, Callable, Iterable
from uuid import uuid4
from wsgiref.simple_server import make_server
from pathlib import Path

UI_DIRECTORY = Path(__file__).with_name("ui")


class EcommerceError(Exception):
    """Client-safe e-commerce error."""

    def __init__(self, status_code: int, code: str, message: str, fields: dict[str, str] | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.fields = fields or {}


class InMemoryEcommerceRepository:
    """Thread-safe in-memory repository for inventory and customer profiles."""

    def __init__(self, products: Iterable[dict[str, Any]] | None = None, profiles: Iterable[dict[str, Any]] | None = None, orders: Iterable[dict[str, Any]] | None = None) -> None:
        self._products = {product["id"]: deepcopy(product) for product in (products or mock_products())}
        self._profiles = {profile["customer_id"]: deepcopy(profile) for profile in (profiles or [])}
        self._orders = {order["id"]: deepcopy(order) for order in (orders or [])}
        self._lock = Lock()

    def list_products(self) -> list[dict[str, Any]]:
        with self._lock:
            return [deepcopy(product) for product in self._products.values()]

    def get_product(self, product_id: str) -> dict[str, Any] | None:
        with self._lock:
            product = self._products.get(product_id)
            return deepcopy(product) if product else None

    def update_inventory(self, product_id: str, quantity_delta: int) -> dict[str, Any]:
        with self._lock:
            product = self._products[product_id]
            product["inventory"] = int(product.get("inventory", 0)) + quantity_delta
            return deepcopy(product)

    def get_profile(self, customer_id: str) -> dict[str, Any] | None:
        with self._lock:
            profile = self._profiles.get(customer_id)
            return deepcopy(profile) if profile else None

    def upsert_profile(self, customer_id: str, email: str) -> dict[str, Any]:
        with self._lock:
            profile = self._profiles.get(customer_id)
            if profile is None:
                profile = {
                    "customer_id": customer_id,
                    "email": email,
                    "products": [],
                    "orders": [],
                }
                self._profiles[customer_id] = deepcopy(profile)
            else:
                profile["email"] = email
                profile.setdefault("products", [])
                profile.setdefault("orders", [])
            return deepcopy(self._profiles[customer_id])

    def add_order_to_profile(self, customer_id: str, order_id: str, product_ids: list[str]) -> dict[str, Any]:
        with self._lock:
            profile = self._profiles.setdefault(customer_id, {"customer_id": customer_id, "email": "", "products": [], "orders": []})
            profile.setdefault("products", [])
            profile.setdefault("orders", [])
            if order_id not in profile["orders"]:
                profile["orders"].append(order_id)
            for product_id in product_ids:
                if product_id not in profile["products"]:
                    profile["products"].append(product_id)
            return deepcopy(profile)

    def create_order(self, order: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            stored = deepcopy(order)
            self._orders[stored["id"]] = stored
            return deepcopy(stored)


def mock_products() -> list[dict[str, Any]]:
    return [
        {"id": "prod-001", "name": "Aster Hoodie", "price": 89.99, "inventory": 12, "category": "Apparel"},
        {"id": "prod-002", "name": "Nimbus Bottle", "price": 24.50, "inventory": 8, "category": "Lifestyle"},
        {"id": "prod-003", "name": "Orbit Speaker", "price": 149.00, "inventory": 5, "category": "Electronics"},
        {"id": "prod-004", "name": "Drift Backpack", "price": 69.00, "inventory": 10, "category": "Travel"},
    ]


class EcommerceService:
    """Business logic for product browsing and single-checkout processing."""

    def __init__(self, repository: InMemoryEcommerceRepository) -> None:
        self.repository = repository

    def list_products(self) -> list[dict[str, Any]]:
        return self.repository.list_products()

    def get_profile(self, customer_id: str) -> dict[str, Any]:
        profile = self.repository.get_profile(customer_id)
        if profile is None:
            raise EcommerceError(404, "customer_not_found", "Customer profile was not found")
        return profile

    def checkout(self, data: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise EcommerceError(422, "invalid_payload", "Request body must be a JSON object")

        customer_id = str(data.get("customer_id") or "").strip()
        email = str(data.get("email") or "").strip()
        items = data.get("items")

        errors: dict[str, str] = {}
        if not customer_id:
            errors["customer_id"] = "This field is required"
        if not email:
            errors["email"] = "This field is required"
        if not isinstance(items, list) or not items:
            errors["items"] = "At least one item is required"

        if errors:
            raise EcommerceError(422, "validation_error", "Checkout data is invalid", errors)

        normalized_items: list[dict[str, Any]] = []
        inventory_updates: list[tuple[str, int]] = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise EcommerceError(422, "validation_error", f"Item {index + 1} is invalid", {"items": "Each cart item must be an object"})
            product_id = str(item.get("product_id") or "").strip()
            quantity = item.get("quantity")
            if not product_id:
                errors["items"] = "Product id is required"
                continue
            try:
                quantity_int = int(quantity)
            except (TypeError, ValueError):
                raise EcommerceError(422, "validation_error", "Quantities must be integers", {"items": "Each quantity must be an integer"})
            if quantity_int <= 0:
                raise EcommerceError(422, "validation_error", "Quantities must be positive", {"items": "Each quantity must be greater than zero"})

            product = self.repository.get_product(product_id)
            if product is None:
                raise EcommerceError(404, "product_not_found", f"Product '{product_id}' was not found")
            if product["inventory"] < quantity_int:
                raise EcommerceError(409, "insufficient_inventory", f"Not enough stock for {product['name']}", {"product_id": product_id})

            total = round(product["price"] * quantity_int, 2)
            normalized_items.append({
                "product_id": product_id,
                "name": product["name"],
                "quantity": quantity_int,
                "unit_price": product["price"],
                "line_total": total,
            })
            inventory_updates.append((product_id, -quantity_int))

        profile = self.repository.upsert_profile(customer_id, email)
        order_id = str(uuid4())
        order = {
            "id": order_id,
            "customer_id": customer_id,
            "email": email,
            "items": normalized_items,
            "status": "confirmed",
            "subtotal": round(sum(item["line_total"] for item in normalized_items), 2),
            "total": round(sum(item["line_total"] for item in normalized_items), 2),
            "created_at": _timestamp(),
            "updated_at": _timestamp(),
            "email_alert": {
                "status": "queued",
                "recipient": email,
                "message": "Order confirmed. Inventory has been updated.",
            },
        }

        for product_id, delta in inventory_updates:
            self.repository.update_inventory(product_id, delta)
        self.repository.create_order(order)
        self.repository.add_order_to_profile(customer_id, order_id, [item["product_id"] for item in normalized_items])

        return {"order": order, "profile": self.repository.get_profile(customer_id)}


class EcommerceApplication:
    """WSGI view for the e-commerce catalog and checkout workflow."""

    def __init__(self, service: EcommerceService) -> None:
        self.service = service

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        try:
            if method == "GET" and path in {"/", "/index.html", "/ui/", "/ui/ecommerce.html"}:
                return self._static_response(start_response, "ecommerce.html")
            if method == "GET" and path in {"/ui/ecommerce.js", "/ui/ecommerce.css"}:
                return self._static_response(start_response, path.rsplit("/", 1)[1])
            if method == "GET" and path == "/api/products":
                return self._respond(start_response, 200, {"products": self.service.list_products()})
            if method == "GET" and path.startswith("/api/customers/") and path.endswith("/profile"):
                customer_id = path.split("/")[3]
                return self._respond(start_response, 200, {"profile": self.service.get_profile(customer_id)})
            if method == "POST" and path == "/api/orders/checkout":
                payload = _read_json(environ)
                return self._respond(start_response, 201, self.service.checkout(payload))
            return self._respond(start_response, 404, {"error": {"code": "not_found", "message": "Route was not found"}})
        except EcommerceError as error:
            payload = {"error": {"code": error.code, "message": str(error)}}
            if error.fields:
                payload["error"]["fields"] = error.fields
            return self._respond(start_response, error.status_code, payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self._respond(start_response, 400, {"error": {"code": "invalid_json", "message": "Request body must contain valid JSON"}})

    @staticmethod
    def _respond(start_response: Callable, status_code: int, payload: dict[str, Any]) -> list[bytes]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        status_text = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            404: "Not Found",
            409: "Conflict",
            422: "Unprocessable Entity",
        }[status_code]
        start_response(f"{status_code} {status_text}", [("Content-Type", "application/json"), ("Content-Length", str(len(body)))])
        return [body]

    @staticmethod
    def _static_response(start_response: Callable, filename: str) -> list[bytes]:
        content_types = {
            "ecommerce.html": "text/html; charset=utf-8",
            "ecommerce.js": "text/javascript; charset=utf-8",
            "ecommerce.css": "text/css; charset=utf-8",
        }
        body = (UI_DIRECTORY / filename).read_bytes()
        start_response("200 OK", [("Content-Type", content_types[filename]), ("Content-Length", str(len(body)))])
        return [body]


def create_app(repository: InMemoryEcommerceRepository | None = None) -> EcommerceApplication:
    return EcommerceApplication(EcommerceService(repository or InMemoryEcommerceRepository()))


def _read_json(environ: dict[str, Any]) -> dict[str, Any]:
    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw = environ.get("wsgi.input", b"").read(length)
    return json.loads(raw.decode("utf-8") or "{}")


def _timestamp() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the prompts-hub e-commerce API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8200)
    args = parser.parse_args()
    with make_server(args.host, args.port, create_app()) as server:
        print(f"E-commerce API listening on http://{args.host}:{args.port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
