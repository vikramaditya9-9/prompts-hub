import json
import unittest

from prompts_hub.health import Check, create_app


def request(app, path="/health/ready", method="GET"):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    body = b"".join(
        app({"REQUEST_METHOD": method, "PATH_INFO": path}, start_response)
    )
    return captured, json.loads(body)


class HealthApiTests(unittest.TestCase):
    def test_liveness_does_not_call_dependencies(self):
        called = False

        def dependency():
            nonlocal called
            called = True

        response, payload = request(create_app([Check("database", dependency)]), "/health/live")

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(payload, {"status": "ok", "checks": {}})
        self.assertFalse(called)

    def test_readiness_is_unavailable_when_required_check_fails(self):
        response, payload = request(create_app([Check("database", lambda: False)]))

        self.assertEqual(response["status"], "503 Service Unavailable")
        self.assertEqual(payload["status"], "not_ready")
        self.assertEqual(payload["checks"]["database"]["status"], "failed")

    def test_optional_failure_does_not_make_application_unready(self):
        response, payload = request(
            create_app([Check("analytics", lambda: False, required=False)])
        )

        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["checks"]["analytics"]["status"], "failed")

    def test_unknown_route_and_method_are_rejected(self):
        not_found, _ = request(create_app(), "/health/details")
        method_not_allowed, _ = request(create_app(), method="POST")

        self.assertEqual(not_found["status"], "404 Not Found")
        self.assertEqual(method_not_allowed["status"], "405 Method Not Allowed")


if __name__ == "__main__":
    unittest.main()