"""Insurance claim APIs with service and repository layers."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import date, datetime, timezone
from io import BytesIO
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Iterable
from uuid import uuid4
from wsgiref.simple_server import make_server

INSURANCE_TYPES = ("health", "motor", "home", "travel", "life", "business")
CLAIM_STATUSES = ("draft", "submitted")
REQUIRED_CLAIM_FIELDS = ("insurance_type", "insurer", "policy_number", "incident_date", "description")
UI_DIRECTORY = Path(__file__).with_name("ui")


class ClaimError(Exception):
    """An expected API error with a safe client-facing message."""

    def __init__(self, status_code: int, code: str, message: str, fields: dict[str, str] | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.fields = fields or {}


class InMemoryClaimRepository:
    """Thread-safe repository suitable for local development and tests."""

    def __init__(self, claims: Iterable[dict[str, Any]] = ()) -> None:
        self._claims = {claim["id"]: deepcopy(claim) for claim in claims}
        self._lock = Lock()

    def create(self, claim: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            stored = deepcopy(claim)
            self._claims[stored["id"]] = stored
            return deepcopy(stored)

    def get(self, claim_id: str) -> dict[str, Any] | None:
        with self._lock:
            claim = self._claims.get(claim_id)
            return deepcopy(claim) if claim else None

    def update(self, claim_id: str, changes: dict[str, Any]) -> dict[str, Any] | None:
        with self._lock:
            claim = self._claims.get(claim_id)
            if claim is None:
                return None
            claim.update(deepcopy(changes))
            return deepcopy(claim)


def mock_claims() -> list[dict[str, Any]]:
    """Return deterministic demo data for local development only."""

    return [
        {
            "id": "claim-demo-1",
            "insurance_type": "motor",
            "insurer": "Demo Mutual",
            "policy_number": "MOCK-POLICY-001",
            "claim_reference": "MOCK-CLAIM-001",
            "incident_date": "2026-08-01",
            "location": "Demo City",
            "description": "Demo claim for local UI development.",
            "status": "draft",
            "losses": [],
            "documents": [],
            "created_at": "2026-08-01T09:00:00+00:00",
            "updated_at": "2026-08-01T09:00:00+00:00",
            "is_mock": True,
        }
    ]


class ClaimService:
    """Business rules for creating, editing, and submitting claims."""

    def __init__(self, repository: InMemoryClaimRepository) -> None:
        self.repository = repository

    def create_claim(self, data: dict[str, Any]) -> dict[str, Any]:
        normalized = self._validate_fields(data, require_all=False)
        now = _timestamp()
        claim = {
            "id": str(uuid4()),
            **normalized,
            "status": "draft",
            "losses": normalized.get("losses", []),
            "documents": normalized.get("documents", []),
            "created_at": now,
            "updated_at": now,
            "is_mock": False,
        }
        return self.repository.create(claim)

    def get_claim(self, claim_id: str) -> dict[str, Any]:
        claim = self.repository.get(claim_id)
        if claim is None:
            raise ClaimError(404, "claim_not_found", "Claim was not found")
        return claim

    def update_claim(self, claim_id: str, data: dict[str, Any]) -> dict[str, Any]:
        claim = self.get_claim(claim_id)
        if claim["status"] != "draft":
            raise ClaimError(409, "claim_not_editable", "Only draft claims can be edited")
        changes = self._validate_fields(data, require_all=False)
        changes["updated_at"] = _timestamp()
        return self.repository.update(claim_id, changes) or self.get_claim(claim_id)

    def submit_claim(self, claim_id: str) -> dict[str, Any]:
        claim = self.get_claim(claim_id)
        if claim["status"] != "draft":
            raise ClaimError(409, "claim_already_submitted", "Claim has already been submitted")
        self._validate_fields(claim, require_all=True)
        updated = self.repository.update(
            claim_id,
            {"status": "submitted", "submitted_at": _timestamp(), "updated_at": _timestamp()},
        )
        return updated or self.get_claim(claim_id)

    @staticmethod
    def _validate_fields(data: dict[str, Any], require_all: bool) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise ClaimError(422, "invalid_payload", "Request body must be a JSON object")
        fields: dict[str, str] = {}
        if require_all:
            for field in REQUIRED_CLAIM_FIELDS:
                if not data.get(field):
                    fields[field] = "This field is required"
        insurance_type = data.get("insurance_type")
        if insurance_type is not None and insurance_type not in INSURANCE_TYPES:
            fields["insurance_type"] = "Unsupported insurance type"
        incident_date = data.get("incident_date")
        if incident_date is not None:
            try:
                date.fromisoformat(incident_date)
            except (TypeError, ValueError):
                fields["incident_date"] = "Use YYYY-MM-DD"
        for collection_name in ("losses", "documents"):
            collection = data.get(collection_name)
            if collection is not None and not isinstance(collection, list):
                fields[collection_name] = "This field must be a list"
        if fields:
            raise ClaimError(422, "validation_error", "Claim data is invalid", fields)
        allowed = {
            key: deepcopy(value)
            for key, value in data.items()
            if key not in {"id", "status", "created_at", "updated_at", "submitted_at", "is_mock"}
        }
        return allowed


class ClaimApplication:
    """WSGI application exposing the claim API."""

    def __init__(self, service: ClaimService) -> None:
        self.service = service

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        try:
            if method == "GET" and path in {"/", "/ui/", "/ui/index.html"}:
                return self._static_response(start_response, "index.html")
            if method == "GET" and path in {"/ui/app.js", "/ui/styles.css"}:
                return self._static_response(start_response, path.rsplit("/", 1)[1])
            if method == "GET" and path == "/api/insurance-types":
                return self._respond(start_response, 200, {"insurance_types": INSURANCE_TYPES})
            if path == "/api/claims" and method == "POST":
                return self._respond(start_response, 201, {"claim": self.service.create_claim(_read_json(environ))})
            claim_id, action = self._claim_route(path)
            if claim_id and method == "GET" and action is None:
                return self._respond(start_response, 200, {"claim": self.service.get_claim(claim_id)})
            if claim_id and method in {"PUT", "PATCH"} and action is None:
                return self._respond(start_response, 200, {"claim": self.service.update_claim(claim_id, _read_json(environ))})
            if claim_id and action == "submit" and method == "POST":
                return self._respond(start_response, 200, {"claim": self.service.submit_claim(claim_id)})
            return self._respond(start_response, 404, {"error": {"code": "not_found", "message": "Route was not found"}})
        except ClaimError as error:
            payload = {"error": {"code": error.code, "message": str(error)}}
            if error.fields:
                payload["error"]["fields"] = error.fields
            return self._respond(start_response, error.status_code, payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self._respond(start_response, 400, {"error": {"code": "invalid_json", "message": "Request body must contain valid JSON"}})

    @staticmethod
    def _claim_route(path: str) -> tuple[str | None, str | None]:
        parts = path.strip("/").split("/")
        if len(parts) == 3 and parts[:2] == ["api", "claims"]:
            return parts[2], None
        if len(parts) == 4 and parts[:2] == ["api", "claims"]:
            return parts[2], parts[3]
        return None, None

    @staticmethod
    def _respond(start_response: Callable, status_code: int, payload: dict[str, Any]) -> list[bytes]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        status_text = {200: "OK", 201: "Created", 400: "Bad Request", 404: "Not Found", 409: "Conflict", 422: "Unprocessable Entity"}[status_code]
        start_response(f"{status_code} {status_text}", [("Content-Type", "application/json"), ("Content-Length", str(len(body)))])
        return [body]

    @staticmethod
    def _static_response(start_response: Callable, filename: str) -> list[bytes]:
        content_types = {"index.html": "text/html; charset=utf-8", "app.js": "text/javascript; charset=utf-8", "styles.css": "text/css; charset=utf-8"}
        body = (UI_DIRECTORY / filename).read_bytes()
        start_response("200 OK", [("Content-Type", content_types[filename]), ("Content-Length", str(len(body)))])
        return [body]


def create_app(repository: InMemoryClaimRepository | None = None) -> ClaimApplication:
    """Create the claim API with local mock data unless a repository is supplied."""

    return ClaimApplication(ClaimService(repository or InMemoryClaimRepository(mock_claims())))


def _read_json(environ: dict[str, Any]) -> dict[str, Any]:
    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw = environ.get("wsgi.input", BytesIO()).read(length)
    return json.loads(raw.decode("utf-8") or "{}")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the prompts-hub insurance claim API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()
    with make_server(args.host, args.port, create_app()) as server:
        print(f"Insurance claim API listening on http://{args.host}:{args.port}")
        server.serve_forever()

if __name__ == "__main__":
    main()