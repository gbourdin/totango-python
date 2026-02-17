from __future__ import annotations

import threading
import unittest
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, cast
from urllib.parse import parse_qs

import requests
import totango


class _RecordingHTTPServer(HTTPServer):
    requests_log: list[dict[str, Any]]
    response_statuses: list[int]


class _RecordingHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802 (stdlib handler signature)
        server = cast(_RecordingHTTPServer, self.server)
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        parsed = {key: values[0] for key, values in parse_qs(body, keep_blank_values=True).items()}

        server.requests_log.append(
            {
                "path": self.path,
                "headers": {key: value for key, value in self.headers.items()},
                "form": parsed,
            }
        )

        status_code = server.response_statuses.pop(0) if server.response_statuses else 200
        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return


@contextmanager
def _running_server(*, response_statuses: list[int] | None = None):
    server = _RecordingHTTPServer(("127.0.0.1", 0), _RecordingHandler)
    server.requests_log = []
    server.response_statuses = list(response_statuses or [])

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        url = f"http://127.0.0.1:{server.server_port}/pixel.gif/"
        yield server, url
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


class TotangoBehaviorTests(unittest.TestCase):
    def test_track_posts_expected_payload(self) -> None:
        with _running_server() as (server, url):
            client = totango.Totango(
                "SP-123",
                user_id="user-1",
                user_name="User One",
                account_id="account-1",
                account_name="Acme",
            )
            client.url = url

            response = client.track(
                "module-a",
                "action-b",
                user_opts={"plan": "gold"},
                account_opts={"tier": "enterprise"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(server.requests_log), 1)

        request = server.requests_log[0]
        self.assertEqual(request["path"], "/pixel.gif/")
        self.assertEqual(request["headers"]["User-Agent"], f"python-totango/{totango.__version__}")

        payload = request["form"]
        self.assertEqual(payload["sdr_s"], "SP-123")
        self.assertEqual(payload["sdr_u"], "user-1")
        self.assertEqual(payload["sdr_u.name"], "User One")
        self.assertEqual(payload["sdr_o"], "account-1")
        self.assertEqual(payload["sdr_odn"], "Acme")
        self.assertEqual(payload["sdr_m"], "module-a")
        self.assertEqual(payload["sdr_a"], "action-b")
        self.assertEqual(payload["sdr_u.plan"], "gold")
        self.assertEqual(payload["sdr_o.tier"], "enterprise")

    def test_track_user_id_argument_overrides_default_user(self) -> None:
        with _running_server() as (server, url):
            client = totango.Totango("SP-123", user_id="default-user")
            client.url = url

            response = client.track("module-a", "action-b", user_id="override-user")

        self.assertEqual(response.status_code, 200)
        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_u"], "override-user")

    def test_send_requires_user_id(self) -> None:
        client = totango.Totango("SP-123")

        with self.assertRaises(NameError):
            client.send()

    def test_http_errors_are_raised(self) -> None:
        with _running_server(response_statuses=[500]) as (_server, url):
            client = totango.Totango("SP-123", user_id="user-1")
            client.url = url

            with self.assertRaises(requests.HTTPError):
                client.send()


class TotangoTrackerParityTests(unittest.TestCase):
    def test_eu_region_uses_eu_endpoint(self) -> None:
        tracker = totango.TotangoTracker("SP-123", "EU")
        self.assertEqual(tracker.url, "https://api-eu1.totango.com/pixel.gif/")

    def test_invalid_region_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            totango.TotangoTracker("SP-123", "APAC")

    def test_track_activity_maps_to_event_payload(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            response = tracker.trackActivity("billing", "opened", "user@example.com", "Acme")

        self.assertEqual(response.status_code, 200)
        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_m"], "billing")
        self.assertEqual(payload["sdr_a"], "opened")
        self.assertEqual(payload["sdr_u"], "user@example.com")
        self.assertEqual(payload["sdr_u.name"], "user@example.com")
        self.assertEqual(payload["sdr_odn"], "Acme")

    def test_api_token_sets_auth_headers(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123", "US", "token-123")
            tracker.url = url
            tracker.trackActivity("billing", "opened", "user@example.com")

        headers = server.requests_log[0]["headers"]
        self.assertEqual(headers["Authorization"], "app-token token-123")
        self.assertEqual(headers["X-API-Token"], "token-123")

    def test_set_user_attributes(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.setUserAttributes(
                "user-1",
                "Jane User",
                {"plan": "enterprise", "role": "admin"},
            )

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_u"], "user-1")
        self.assertEqual(payload["sdr_u.name"], "Jane User")
        self.assertEqual(payload["sdr_u.plan"], "enterprise")
        self.assertEqual(payload["sdr_u.role"], "admin")

    def test_set_attributes_splits_user_and_account_prefixes(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.setAttributes(
                "account-1",
                "Acme",
                "user-1",
                "Jane User",
                {
                    "a.tier": "enterprise",
                    "a.segment": "financial-services",
                    "u.plan": "gold",
                    "u.mrr": "1200",
                },
            )

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_o"], "account-1")
        self.assertEqual(payload["sdr_odn"], "Acme")
        self.assertEqual(payload["sdr_u"], "user-1")
        self.assertEqual(payload["sdr_u.name"], "Jane User")
        self.assertEqual(payload["sdr_o.tier"], "enterprise")
        self.assertEqual(payload["sdr_o.segment"], "financial-services")
        self.assertEqual(payload["sdr_u.plan"], "gold")
        self.assertEqual(payload["sdr_u.mrr"], "1200")

    def test_set_account_attributes_uses_account_as_fallback_user(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.setAccountAttributes("account-1", "Acme", {"tier": "enterprise"})

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_u"], "account-1")
        self.assertEqual(payload["sdr_u.name"], "account-1")
        self.assertEqual(payload["sdr_o"], "account-1")
        self.assertEqual(payload["sdr_odn"], "Acme")
        self.assertEqual(payload["sdr_o.tier"], "enterprise")

    def test_set_account_attributes_prefers_existing_tracker_user(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url
            tracker.user_id = "user-1"
            tracker.user_name = "Jane User"

            tracker.setAccountAttributes("account-1", "Acme", {"tier": "enterprise"})

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_u"], "user-1")
        self.assertEqual(payload["sdr_u.name"], "Jane User")
        self.assertEqual(payload["sdr_o"], "account-1")
        self.assertEqual(payload["sdr_odn"], "Acme")
        self.assertEqual(payload["sdr_o.tier"], "enterprise")

    def test_set_attributes_without_prefix_defaults_to_user(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.setAttributes(
                "account-1",
                "Acme",
                "user-1",
                "Jane User",
                {"plan": "gold", "a.segment": "saas"},
            )

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_u.plan"], "gold")
        self.assertEqual(payload["sdr_o.segment"], "saas")

    def test_track_activity_snake_case_alias(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.track_activity("billing", "opened", "user@example.com", "Acme")

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_m"], "billing")
        self.assertEqual(payload["sdr_a"], "opened")
        self.assertEqual(payload["sdr_u"], "user@example.com")
        self.assertEqual(payload["sdr_odn"], "Acme")

    def test_set_user_attributes_snake_case_alias(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.set_user_attributes("user-1", "Jane User", {"plan": "enterprise"})

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_u"], "user-1")
        self.assertEqual(payload["sdr_u.name"], "Jane User")
        self.assertEqual(payload["sdr_u.plan"], "enterprise")

    def test_set_account_attributes_snake_case_alias(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.set_account_attributes("account-1", "Acme", {"tier": "enterprise"})

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_u"], "account-1")
        self.assertEqual(payload["sdr_u.name"], "account-1")
        self.assertEqual(payload["sdr_o"], "account-1")
        self.assertEqual(payload["sdr_odn"], "Acme")
        self.assertEqual(payload["sdr_o.tier"], "enterprise")

    def test_set_attributes_snake_case_alias(self) -> None:
        with _running_server() as (server, url):
            tracker = totango.TotangoTracker("SP-123")
            tracker.url = url

            tracker.set_attributes(
                "account-1",
                "Acme",
                "user-1",
                "Jane User",
                {"a.tier": "enterprise", "u.plan": "gold"},
            )

        payload = server.requests_log[0]["form"]
        self.assertEqual(payload["sdr_o.tier"], "enterprise")
        self.assertEqual(payload["sdr_u.plan"], "gold")


if __name__ == "__main__":
    unittest.main()
