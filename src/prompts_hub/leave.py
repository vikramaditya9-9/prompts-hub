"""Leave request APIs with service and repository layers."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import date, datetime, timezone
from io import BytesIO
from pathlib import Path
from threading import Lock
from typing import Any, Callable
from urllib.parse import parse_qs
from uuid import uuid4
from wsgiref.simple_server import make_server

LEAVE_TYPES = ("annual", "sick", "personal", "maternity", "paternity", "unpaid")
LEAVE_STATUSES = ("draft", "submitted", "approved", "rejected", "cancelled")
REQUIRED_LEAVE_FIELDS = (
    "employee_id",
    "manager_id",
    "leave_type",
    "start_date",
    "end_date",
    "reason",
)
UI_DIRECTORY = Path(__file__).with_name("ui")
ALLOWED_TRANSITIONS = {
    "draft": {"submitted", "cancelled"},
    "submitted": {"approved", "rejected", "cancelled"},
    "approved": set(),
    "rejected": set(),
    "cancelled": set(),
}


class LeaveError(Exception):
    """An expected API error with a safe client-facing message."""

    def __init__(self, status_code: int, code: str, message: str, fields: dict[str, str] | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.fields = fields or {}


class InMemoryLeaveRepository:
    """Thread-safe repository for leave requests."""

    def __init__(self, leave_requests: list[dict[str, Any]] | None = None) -> None:
        self._leave_requests = {leave_request["id"]: deepcopy(leave_request) for leave_request in (leave_requests or [])}
        self._lock = Lock()

    def create(self, leave_request: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            stored = deepcopy(leave_request)
            self._leave_requests[stored["id"]] = stored
            return deepcopy(stored)

    def get(self, leave_id: str) -> dict[str, Any] | None:
        with self._lock:
            leave_request = self._leave_requests.get(leave_id)
            return deepcopy(leave_request) if leave_request else None

    def update(self, leave_id: str, changes: dict[str, Any]) -> dict[str, Any] | None:
        with self._lock:
            leave_request = self._leave_requests.get(leave_id)
            if leave_request is None:
                return None
            leave_request.update(deepcopy(changes))
            return deepcopy(leave_request)

    def list_all(self) -> list[dict[str, Any]]:
        with self._lock:
            return [deepcopy(item) for item in self._leave_requests.values()]

    def list_by_employee(self, employee_id: str) -> list[dict[str, Any]]:
        with self._lock:
            return [deepcopy(item) for item in self._leave_requests.values() if item.get("employee_id") == employee_id]

    def list_by_manager(self, manager_id: str) -> list[dict[str, Any]]:
        with self._lock:
            return [deepcopy(item) for item in self._leave_requests.values() if item.get("manager_id") == manager_id]


def mock_leave_requests() -> list[dict[str, Any]]:
    """Return deterministic mock leave records suitable for local development."""

    return [
        {
            "id": "leave-demo-1",
            "employee_id": "emp-001",
            "manager_id": "mgr-001",
            "leave_type": "annual",
            "start_date": "2026-08-20",
            "end_date": "2026-08-22",
            "reason": "Family trip",
            "status": "submitted",
            "decision_reason": None,
            "created_at": "2026-08-01T09:00:00+00:00",
            "updated_at": "2026-08-01T09:00:00+00:00",
            "is_mock": True,
        },
        {
            "id": "leave-demo-2",
            "employee_id": "emp-002",
            "manager_id": "mgr-002",
            "leave_type": "sick",
            "start_date": "2026-08-25",
            "end_date": "2026-08-26",
            "reason": "Medical appointment",
            "status": "approved",
            "decision_reason": "Approved and scheduled",
            "created_at": "2026-08-03T10:00:00+00:00",
            "updated_at": "2026-08-03T10:00:00+00:00",
            "is_mock": True,
        },
    ]


class LeaveService:
    """Business rules for leave creation, review, and lifecycle transitions."""

    def __init__(self, repository: InMemoryLeaveRepository) -> None:
        self.repository = repository

    def create_leave(self, data: dict[str, Any]) -> dict[str, Any]:
        normalized = self._validate_fields(data)
        now = _timestamp()
        leave_request = {
            "id": str(uuid4()),
            **normalized,
            "status": "draft",
            "decision_reason": None,
            "created_at": now,
            "updated_at": now,
            "is_mock": False,
        }
        return self.repository.create(leave_request)

    def get_leave(self, leave_id: str, employee_id: str | None = None, manager_id: str | None = None, role: str | None = None) -> dict[str, Any]:
        leave_request = self.repository.get(leave_id)
        if leave_request is None:
            raise LeaveError(404, "leave_not_found", "Leave request was not found")

        if role == "administrator":
            return leave_request
        if employee_id and leave_request["employee_id"] == employee_id:
            return leave_request
        if manager_id and leave_request["manager_id"] == manager_id:
            return leave_request
        raise LeaveError(403, "forbidden", "You are not allowed to access this leave request")

    def list_leave_requests(self, employee_id: str | None = None, manager_id: str | None = None, role: str | None = None) -> list[dict[str, Any]]:
        if role == "administrator":
            return self.repository.list_all()
        if employee_id:
            return self.repository.list_by_employee(employee_id)
        if manager_id:
            return self.repository.list_by_manager(manager_id)
        raise LeaveError(403, "forbidden", "You do not have permission to list leave requests")

    def submit_leave(self, leave_id: str, employee_id: str) -> dict[str, Any]:
        leave_request = self.get_leave(leave_id, employee_id=employee_id)
        if leave_request["status"] != "draft":
            raise LeaveError(409, "invalid_status_transition", "Only draft requests can be submitted")
        self._validate_fields(leave_request, require_all=True)
        result = self.repository.update(
            leave_id,
            {"status": "submitted", "updated_at": _timestamp()},
        )
        return result or self.get_leave(leave_id, employee_id=employee_id)

    def cancel_leave(self, leave_id: str, employee_id: str, reason: str | None = None) -> dict[str, Any]:
        leave_request = self.get_leave(leave_id, employee_id=employee_id)
        if leave_request["status"] not in {"draft", "submitted"}:
            raise LeaveError(409, "invalid_status_transition", "Only draft or submitted requests can be cancelled")
        if reason is not None:
            leave_request["decision_reason"] = reason
        result = self.repository.update(
            leave_id,
            {"status": "cancelled", "decision_reason": reason or leave_request.get("decision_reason"), "updated_at": _timestamp()},
        )
        return result or self.get_leave(leave_id, employee_id=employee_id)

    def approve_leave(self, leave_id: str, manager_id: str, reason: str | None = None) -> dict[str, Any]:
        leave_request = self.repository.get(leave_id)
        if leave_request is None:
            raise LeaveError(404, "leave_not_found", "Leave request was not found")
        if leave_request["manager_id"] != manager_id:
            raise LeaveError(403, "forbidden", "This manager is not assigned to the request")
        if leave_request["status"] != "submitted":
            raise LeaveError(409, "invalid_status_transition", "Only submitted requests can be approved")
        if not reason or not reason.strip():
            raise LeaveError(422, "validation_error", "Approval reason is required", {"reason": "This field is required"})
        result = self.repository.update(
            leave_id,
            {"status": "approved", "decision_reason": reason.strip(), "updated_at": _timestamp()},
        )
        return result or self.get_leave(leave_id, manager_id=manager_id)

    def reject_leave(self, leave_id: str, manager_id: str, reason: str | None = None) -> dict[str, Any]:
        leave_request = self.repository.get(leave_id)
        if leave_request is None:
            raise LeaveError(404, "leave_not_found", "Leave request was not found")
        if leave_request["manager_id"] != manager_id:
            raise LeaveError(403, "forbidden", "This manager is not assigned to the request")
        if leave_request["status"] != "submitted":
            raise LeaveError(409, "invalid_status_transition", "Only submitted requests can be rejected")
        if not reason or not reason.strip():
            raise LeaveError(422, "validation_error", "Rejection reason is required", {"reason": "This field is required"})
        result = self.repository.update(
            leave_id,
            {"status": "rejected", "decision_reason": reason.strip(), "updated_at": _timestamp()},
        )
        return result or self.get_leave(leave_id, manager_id=manager_id)

    @staticmethod
    def _validate_fields(data: dict[str, Any], require_all: bool = True) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise LeaveError(422, "invalid_payload", "Request body must be a JSON object")

        fields: dict[str, str] = {}
        for field in REQUIRED_LEAVE_FIELDS:
            if require_all and not data.get(field):
                fields[field] = "This field is required"

        leave_type = data.get("leave_type")
        if leave_type is not None and leave_type not in LEAVE_TYPES:
            fields["leave_type"] = "Unsupported leave type"

        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date is not None:
            try:
                date.fromisoformat(start_date)
            except (TypeError, ValueError):
                fields["start_date"] = "Use YYYY-MM-DD"
        if end_date is not None:
            try:
                date.fromisoformat(end_date)
            except (TypeError, ValueError):
                fields["end_date"] = "Use YYYY-MM-DD"
        if start_date and end_date:
            try:
                if date.fromisoformat(end_date) < date.fromisoformat(start_date):
                    fields["end_date"] = "End date must be on or after start date"
            except (TypeError, ValueError):
                pass

        if fields:
            raise LeaveError(422, "validation_error", "Leave request data is invalid", fields)

        allowed = {
            key: deepcopy(value)
            for key, value in data.items()
            if key not in {"id", "status", "created_at", "updated_at", "is_mock", "decision_reason"}
        }
        return allowed


class LeaveApplication:
    """WSGI application exposing the leave API."""

    def __init__(self, service: LeaveService) -> None:
        self.service = service

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        try:
            if method == "GET" and path in {"/", "/leave", "/ui/", "/ui/leave.html"}:
                return self._static_response(start_response, "leave.html")
            if method == "GET" and path in {"/ui/leave.js", "/ui/leave.css"}:
                return self._static_response(start_response, path.rsplit("/", 1)[1])
            if path == "/api/leave-requests" and method == "POST":
                payload = self.service.create_leave(_read_json(environ))
                return self._respond(start_response, 201, {"leave_request": payload})
            if path == "/api/leave-requests" and method == "GET":
                query = _query_params(environ)
                records = self.service.list_leave_requests(
                    employee_id=query.get("employee_id"),
                    manager_id=query.get("manager_id"),
                    role=query.get("role"),
                )
                return self._respond(start_response, 200, {"leave_requests": records})
            if path == "/api/leave-records" and method == "GET":
                query = _query_params(environ)
                if query.get("role") != "administrator":
                    raise LeaveError(403, "forbidden", "Administrator access is required")
                return self._respond(start_response, 200, {"leave_requests": self.service.repository.list_all()})

            leave_id, action = self._leave_route(path)
            if leave_id and method == "GET" and action is None:
                query = _query_params(environ)
                return self._respond(
                    start_response,
                    200,
                    {"leave_request": self.service.get_leave(leave_id, employee_id=query.get("employee_id"), manager_id=query.get("manager_id"), role=query.get("role"))},
                )
            if leave_id and action == "submit" and method == "POST":
                body = _read_json(environ)
                return self._respond(start_response, 200, {"leave_request": self.service.submit_leave(leave_id, body.get("employee_id") or body.get("actor_id") or "")})
            if leave_id and action == "cancel" and method == "POST":
                body = _read_json(environ)
                employee_id = body.get("employee_id") or body.get("actor_id")
                if not employee_id:
                    raise LeaveError(422, "validation_error", "Employee is required", {"employee_id": "This field is required"})
                return self._respond(start_response, 200, {"leave_request": self.service.cancel_leave(leave_id, employee_id, body.get("reason"))})
            if leave_id and action == "approve" and method == "POST":
                body = _read_json(environ)
                manager_id = body.get("manager_id")
                if not manager_id:
                    raise LeaveError(422, "validation_error", "Manager is required", {"manager_id": "This field is required"})
                return self._respond(start_response, 200, {"leave_request": self.service.approve_leave(leave_id, manager_id, body.get("reason"))})
            if leave_id and action == "reject" and method == "POST":
                body = _read_json(environ)
                manager_id = body.get("manager_id")
                if not manager_id:
                    raise LeaveError(422, "validation_error", "Manager is required", {"manager_id": "This field is required"})
                return self._respond(start_response, 200, {"leave_request": self.service.reject_leave(leave_id, manager_id, body.get("reason"))})
            return self._respond(start_response, 404, {"error": {"code": "not_found", "message": "Route was not found"}})
        except LeaveError as error:
            payload = {"error": {"code": error.code, "message": str(error)}}
            if error.fields:
                payload["error"]["fields"] = error.fields
            return self._respond(start_response, error.status_code, payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self._respond(start_response, 400, {"error": {"code": "invalid_json", "message": "Request body must contain valid JSON"}})

    @staticmethod
    def _leave_route(path: str) -> tuple[str | None, str | None]:
        parts = path.strip("/").split("/")
        if len(parts) == 3 and parts[0] == "api" and parts[1] == "leave-requests":
            return parts[2], None
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "leave-requests":
            return parts[2], parts[3]
        return None, None

    @staticmethod
    def _respond(start_response: Callable, status_code: int, payload: dict[str, Any]) -> list[bytes]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        status_text = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
            409: "Conflict",
            422: "Unprocessable Entity",
        }[status_code]
        start_response(f"{status_code} {status_text}", [("Content-Type", "application/json"), ("Content-Length", str(len(body)))])
        return [body]

    @staticmethod
    def _static_response(start_response: Callable, filename: str) -> list[bytes]:
        content_types = {
            "leave.html": "text/html; charset=utf-8",
            "leave.js": "text/javascript; charset=utf-8",
            "leave.css": "text/css; charset=utf-8",
        }
        body = (UI_DIRECTORY / filename).read_bytes()
        start_response("200 OK", [("Content-Type", content_types[filename]), ("Content-Length", str(len(body)))])
        return [body]


def create_app(repository: InMemoryLeaveRepository | None = None) -> LeaveApplication:
    """Create the leave API with local mock data unless a repository is supplied."""

    return LeaveApplication(LeaveService(repository or InMemoryLeaveRepository(mock_leave_requests())))


def _read_json(environ: dict[str, Any]) -> dict[str, Any]:
    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw = environ.get("wsgi.input", BytesIO()).read(length)
    return json.loads(raw.decode("utf-8") or "{}")


def _query_params(environ: dict[str, Any]) -> dict[str, str | None]:
    raw = environ.get("QUERY_STRING", "")
    params: dict[str, str | None] = {}
    for key, values in parse_qs(raw, keep_blank_values=True).items():
        params[key] = values[0] if values else None
    return params


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the prompts-hub leave API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8100)
    args = parser.parse_args()
    with make_server(args.host, args.port, create_app()) as server:
        print(f"Leave API listening on http://{args.host}:{args.port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
