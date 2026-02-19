from __future__ import annotations

import warnings
from collections.abc import Mapping
from typing import Any

import requests
from requests import Response

__version__ = "0.5.0"

UserAttributes = Mapping[str, Any]
AccountAttributes = Mapping[str, Any]
Attributes = Mapping[str, Any]

REGION_ENDPOINTS = {
    "US": "https://api.totango.com/pixel.gif/",
    "EU": "https://api-eu1.totango.com/pixel.gif/",
}


class Totango:
    """Client for Totango's tracking pixel endpoint."""

    def __init__(
        self,
        service_id: str,
        user_id: str | None = None,
        user_name: str | None = None,
        account_id: str | None = None,
        account_name: str | None = None,
        region: str | None = None,
        api_token: str | None = None,
    ) -> None:
        if region is None:
            self.url = "https://sdr.totango.com/pixel.gif/"
            self.region: str | None = None
        else:
            normalized_region = region.upper()
            if normalized_region not in REGION_ENDPOINTS:
                raise ValueError("region must be 'US' or 'EU'")
            if api_token is None:
                raise ValueError("api_token is required when region is set")
            self.region = normalized_region
            self.url = REGION_ENDPOINTS[normalized_region]

        self.service_id = service_id
        self.account_id = account_id
        self.account_name = account_name
        self.user_id = user_id
        self.user_name = user_name
        self.api_token = api_token

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

    def _get_headers(self) -> dict[str, str]:
        headers = {"User-Agent": f"python-totango/{__version__}"}
        if self.api_token:
            headers["Authorization"] = f"app-token {self.api_token}"
            headers["X-API-Token"] = self.api_token
        return headers

    def _post(self, payload: Mapping[str, Any]) -> Response:
        response = requests.post(
            self.url,
            data=payload,
            headers=self._get_headers(),
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
        warnings.warn(
            "track() will be deprecated in a future release, use track_activity() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.track_activity(
            module=module,
            action=action,
            user_id=user_id,
            user_name=user_name,
            account_id=account_id,
            account_name=account_name,
            user_opts=user_opts,
            account_opts=account_opts,
        )

    def track_activity(
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

    def set_user_attributes(
        self,
        user_id: str,
        user_name: str,
        attributes: UserAttributes,
    ) -> Response:
        return self.send(
            user_id=user_id,
            user_name=user_name,
            user_opts=attributes,
        )

    def set_account_attributes(
        self,
        account_id: str,
        account_name: str,
        attributes: AccountAttributes,
    ) -> Response:
        user_id = self.user_id or account_id
        user_name = self.user_name or user_id
        return self.send(
            user_id=user_id,
            user_name=user_name,
            account_id=account_id,
            account_name=account_name,
            account_opts=attributes,
        )

    def set_attributes(
        self,
        account_id: str,
        account_name: str,
        user_id: str,
        user_name: str,
        attributes: Attributes,
    ) -> Response:
        user_opts: dict[str, Any] = {}
        account_opts: dict[str, Any] = {}

        for key, value in attributes.items():
            if key.startswith("a."):
                account_opts[key[2:]] = value
            elif key.startswith("u."):
                user_opts[key[2:]] = value
            else:
                user_opts[key] = value

        return self.send(
            user_id=user_id,
            user_name=user_name,
            account_id=account_id,
            account_name=account_name,
            user_opts=user_opts,
            account_opts=account_opts,
        )
