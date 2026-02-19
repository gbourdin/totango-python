from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import requests
from requests import Response

__version__ = "0.4.1"

UserAttributes = Mapping[str, Any]
AccountAttributes = Mapping[str, Any]


class Totango:
    """Client for Totango's tracking pixel endpoint."""

    def __init__(
        self,
        service_id: str,
        user_id: str | None = None,
        user_name: str | None = None,
        account_id: str | None = None,
        account_name: str | None = None,
    ) -> None:
        self.url = "https://sdr.totango.com/pixel.gif/"
        self.service_id = service_id
        self.account_id = account_id
        self.account_name = account_name
        self.user_id = user_id
        self.user_name = user_name

    def _get_base_payload(
        self,
        user_id: str | None = None,
        user_name: str | None = None,
        account_id: str | None = None,
        account_name: str | None = None,
        user_opts: UserAttributes | None = None,
        account_opts: AccountAttributes | None = None,
    ) -> dict[str, Any]:
        user_id = user_id or self.user_id
        if user_id is None:
            raise NameError("user_id is required")

        payload: dict[str, Any] = {
            "sdr_s": self.service_id,
            "sdr_u": user_id,
        }

        user_name = user_name or self.user_name
        if user_name is not None:
            payload["sdr_u.name"] = user_name

        account_id = account_id or self.account_id
        if account_id is not None:
            payload["sdr_o"] = account_id

        account_name = account_name or self.account_name
        if account_name is not None:
            payload["sdr_odn"] = account_name

        for key, value in (user_opts or {}).items():
            payload[f"sdr_u.{key}"] = value

        for key, value in (account_opts or {}).items():
            payload[f"sdr_o.{key}"] = value

        return payload

    def _post(self, payload: Mapping[str, Any]) -> Response:
        response = requests.post(
            self.url,
            data=payload,
            headers={"User-Agent": f"python-totango/{__version__}"},
        )
        response.raise_for_status()
        return response

    def track(
        self,
        module: str,
        action: str,
        user_id: str | None = None,
        user_name: str | None = None,
        account_id: str | None = None,
        account_name: str | None = None,
        user_opts: UserAttributes | None = None,
        account_opts: AccountAttributes | None = None,
    ) -> Response:
        payload = self._get_base_payload(
            user_id=user_id,
            user_name=user_name,
            account_id=account_id,
            account_name=account_name,
            user_opts=user_opts,
            account_opts=account_opts,
        )
        payload["sdr_m"] = module
        payload["sdr_a"] = action

        return self._post(payload)

    def send(
        self,
        user_id: str | None = None,
        user_name: str | None = None,
        account_id: str | None = None,
        account_name: str | None = None,
        user_opts: UserAttributes | None = None,
        account_opts: AccountAttributes | None = None,
    ) -> Response:
        payload = self._get_base_payload(
            user_id=user_id,
            user_name=user_name,
            account_id=account_id,
            account_name=account_name,
            user_opts=user_opts,
            account_opts=account_opts,
        )

        return self._post(payload)
