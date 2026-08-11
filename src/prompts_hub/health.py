"""Dependency-free WSGI health endpoints for the application."""

from __future__ import annotations

import argparse
import json
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass
from time import monotonic
from typing import Callable, Iterable
from wsgiref.simple_server import make_server

logger = logging.getLogger(__name__)
HealthCheck = Callable[[], bool | None]


@dataclass(frozen=True)
class Check:
    """A named readiness dependency check."""

    name: str
    function: HealthCheck
    required: bool = True


class HealthApplication:
    """WSGI application exposing liveness, readiness, and aggregate health."""

    def __init__(
        self,
        checks: Iterable[Check] = (),
        timeout_seconds: float = 2.0,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        self.checks = tuple(checks)
        self.timeout_seconds = timeout_seconds

    def __call__(self, environ: dict, start_response: Callable) -> list[bytes]:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/health")

        if method != "GET":
            return self._respond(
                start_response,
                405,
                {"status": "error", "message": "method not allowed"},
                {"Allow": "GET"},
            )

        if path == "/health/live":
            return self._respond(start_response, 200, {"status": "ok", "checks": {}})
        if path in {"/health", "/health/ready"}:
            payload, status_code = self._readiness()
            return self._respond(start_response, status_code, payload)
        return self._respond(
            start_response,
            404,
            {"status": "error", "message": "not found"},
        )

    def _readiness(self) -> tuple[dict, int]:
        results: dict[str, dict[str, object]] = {}
        required_failure = False

        for check in self.checks:
            result = self._run_check(check)
            results[check.name] = result
            if check.required and result["status"] != "ok":
                required_failure = True

        status = "not_ready" if required_failure else "ok"
        return {"status": status, "checks": results}, 503 if required_failure else 200

    def _run_check(self, check: Check) -> dict[str, object]:
        started = monotonic()
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(check.function)
        try:
            result = future.result(timeout=self.timeout_seconds)
            check_status = "ok" if result is not False else "failed"
        except TimeoutError:
            future.cancel()
            check_status = "timeout"
            logger.warning("Health check timed out: %s", check.name)
        except Exception:
            check_status = "failed"
            logger.exception("Health check failed: %s", check.name)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

        return {
            "status": check_status,
            "latency_ms": round((monotonic() - started) * 1000, 2),
        }

    @staticmethod
    def _respond(
        start_response: Callable,
        status_code: int,
        payload: dict,
        extra_headers: dict[str, str] | None = None,
    ) -> list[bytes]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
        ]
        if extra_headers:
            headers.extend(extra_headers.items())
        status_text = {200: "OK", 404: "Not Found", 405: "Method Not Allowed", 503: "Service Unavailable"}[status_code]
        start_response(f"{status_code} {status_text}", headers)
        return [body]


def create_app(checks: Iterable[Check] = (), timeout_seconds: float = 2.0) -> HealthApplication:
    """Create an application that can be mounted in a WSGI server."""

    return HealthApplication(checks, timeout_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the prompts-hub health API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    with make_server(args.host, args.port, create_app()) as server:
        logger.info("Health API listening on http://%s:%s", args.host, args.port)
        server.serve_forever()