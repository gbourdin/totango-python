from __future__ import annotations

import threading
import unittest
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.parse import parse_qs

import requests

import totango


class _RecordingHTTPServer(HTTPServer):
    requests_log: list[dict[str, Any]]
    response_statuses: list[int]


class _RecordingHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802 (stdlib handler signature)
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        parsed = {key: values[0] for key, values in parse_qs(body, keep_blank_values=True).items()}

        self.server.requests_log.append(
            {
                "path": self.path,
                "headers": {key: value for key, value in self.headers.items()},
                "form": parsed,
            }
        )

        status_code = self.server.response_statuses.pop(0) if self.server.response_statuses else 200
        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, _format: str, *_args: Any) -> None:  # noqa: A003
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


if __name__ == "__main__":
    unittest.main()
