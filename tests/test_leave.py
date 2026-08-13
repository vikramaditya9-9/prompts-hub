import io
import json
import unittest

from prompts_hub.leave import InMemoryLeaveRepository, create_app


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


class LeaveWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(InMemoryLeaveRepository())
        self.payload = {
            "employee_id": "emp-001",
            "manager_id": "mgr-001",
            "leave_type": "annual",
            "start_date": "2026-09-10",
            "end_date": "2026-09-12",
            "reason": "Family visit",
        }

    def test_employee_can_create_submit_and_cancel_own_leave(self):
        created_response, created_payload = request(self.app, "/api/leave-requests", "POST", self.payload)
        self.assertEqual(created_response["status"], "201 Created")
        self.assertEqual(created_payload["leave_request"]["status"], "draft")

        leave_id = created_payload["leave_request"]["id"]
        submit_response, submit_payload = request(self.app, f"/api/leave-requests/{leave_id}/submit", "POST")
        self.assertEqual(submit_response["status"], "200 OK")
        self.assertEqual(submit_payload["leave_request"]["status"], "submitted")

        cancel_response, cancel_payload = request(
            self.app,
            f"/api/leave-requests/{leave_id}/cancel",
            "POST",
            {"employee_id": "emp-001", "reason": "Plans changed"},
        )
        self.assertEqual(cancel_response["status"], "200 OK")
        self.assertEqual(cancel_payload["leave_request"]["status"], "cancelled")

    def test_manager_can_approve_submitted_request_with_reason(self):
        created_response, created_payload = request(self.app, "/api/leave-requests", "POST", self.payload)
        leave_id = created_payload["leave_request"]["id"]
        request(self.app, f"/api/leave-requests/{leave_id}/submit", "POST")

        response, payload = request(
            self.app,
            f"/api/leave-requests/{leave_id}/approve",
            "POST",
            {"manager_id": "mgr-001", "reason": "Approved for calendar coverage"},
        )
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(payload["leave_request"]["status"], "approved")

    def test_rejection_requires_reason(self):
        created_response, created_payload = request(self.app, "/api/leave-requests", "POST", self.payload)
        leave_id = created_payload["leave_request"]["id"]
        request(self.app, f"/api/leave-requests/{leave_id}/submit", "POST")

        response, payload = request(
            self.app,
            f"/api/leave-requests/{leave_id}/reject",
            "POST",
            {"manager_id": "mgr-001"},
        )
        self.assertEqual(response["status"], "422 Unprocessable Entity")
        self.assertIn("reason", payload["error"]["fields"])

    def test_status_transitions_are_restricted(self):
        created_response, created_payload = request(self.app, "/api/leave-requests", "POST", self.payload)
        leave_id = created_payload["leave_request"]["id"]

        response, payload = request(
            self.app,
            f"/api/leave-requests/{leave_id}/approve",
            "POST",
            {"manager_id": "mgr-001", "reason": "Invalid phase"},
        )
        self.assertEqual(response["status"], "409 Conflict")
        self.assertEqual(payload["error"]["code"], "invalid_status_transition")

    def test_employee_cannot_view_other_employee_requests(self):
        created_response, created_payload = request(self.app, "/api/leave-requests", "POST", self.payload)
        leave_id = created_payload["leave_request"]["id"]

        response, payload = request(self.app, f"/api/leave-requests/{leave_id}", "GET", None, "employee_id=emp-999")
        self.assertEqual(response["status"], "403 Forbidden")
        self.assertEqual(payload["error"]["code"], "forbidden")

    def test_administrator_can_view_all_records(self):
        request(self.app, "/api/leave-requests", "POST", self.payload)
        response, payload = request(self.app, "/api/leave-records", "GET", None, "role=administrator")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(len(payload["leave_requests"]), 1)

    def test_leave_ui_assets_are_served(self):
        response, body = request_raw(self.app, "/ui/leave.html")
        self.assertEqual(response["status"], "200 OK")
        self.assertIn(b"Leaveboard", body)


if __name__ == "__main__":
    unittest.main()
