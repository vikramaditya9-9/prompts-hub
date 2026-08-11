import io
import json
import unittest

from prompts_hub.claims import InMemoryClaimRepository, create_app


def request(app, path, method="GET", payload=None):
    body = json.dumps(payload).encode() if payload is not None else b""
    response = {}

    def start_response(status, headers):
        response["status"] = status
        response["headers"] = dict(headers)

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
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


class ClaimApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(InMemoryClaimRepository())
        self.claim = {
            "insurance_type": "motor",
            "insurer": "Example Mutual",
            "policy_number": "POLICY-123",
            "incident_date": "2026-08-10",
            "location": "Example City",
            "description": "A factual incident description.",
            "losses": [{"description": "Repair", "amount": 1250, "currency": "USD"}],
        }

    def test_create_get_update_and_submit_claim(self):
        created_response, created_payload = request(self.app, "/api/claims", "POST", self.claim)
        claim_id = created_payload["claim"]["id"]

        self.assertEqual(created_response["status"], "201 Created")
        self.assertEqual(created_payload["claim"]["status"], "draft")

        get_response, get_payload = request(self.app, f"/api/claims/{claim_id}")
        self.assertEqual(get_response["status"], "200 OK")
        self.assertEqual(get_payload["claim"]["policy_number"], "POLICY-123")

        update_response, update_payload = request(
            self.app, f"/api/claims/{claim_id}", "PATCH", {"location": "Updated City"}
        )
        self.assertEqual(update_response["status"], "200 OK")
        self.assertEqual(update_payload["claim"]["location"], "Updated City")

        submit_response, submit_payload = request(self.app, f"/api/claims/{claim_id}/submit", "POST")
        self.assertEqual(submit_response["status"], "200 OK")
        self.assertEqual(submit_payload["claim"]["status"], "submitted")

    def test_submit_rejects_missing_required_fields(self):
        response, payload = request(self.app, "/api/claims", "POST", {"insurance_type": "home"})

        self.assertEqual(response["status"], "201 Created")
        claim_id = payload["claim"]["id"]
        submit_response, submit_payload = request(self.app, f"/api/claims/{claim_id}/submit", "POST")

        self.assertEqual(submit_response["status"], "422 Unprocessable Entity")
        self.assertIn("policy_number", submit_payload["error"]["fields"])

    def test_validation_rejects_unknown_type_and_bad_date(self):
        response, payload = request(
            self.app,
            "/api/claims",
            "POST",
            {"insurance_type": "unknown", "incident_date": "tomorrow"},
        )

        self.assertEqual(response["status"], "422 Unprocessable Entity")
        self.assertEqual(payload["error"]["code"], "validation_error")

    def test_default_app_exposes_labeled_mock_data(self):
        response, payload = request(create_app(), "/api/claims/claim-demo-1")

        self.assertEqual(response["status"], "200 OK")
        self.assertTrue(payload["claim"]["is_mock"])

    def test_supported_insurance_types_are_available(self):
        response, payload = request(self.app, "/api/insurance-types")

        self.assertEqual(response["status"], "200 OK")
        self.assertIn("motor", payload["insurance_types"])

    def test_claim_ui_and_assets_are_served(self):
        page_response, page = request_raw(self.app, "/")
        script_response, script = request_raw(self.app, "/ui/app.js")

        self.assertEqual(page_response["status"], "200 OK")
        self.assertIn(b"Claimdesk", page)
        self.assertEqual(script_response["status"], "200 OK")
        self.assertIn(b"/api/claims", script)


if __name__ == "__main__":
    unittest.main()