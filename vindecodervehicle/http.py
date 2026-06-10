"""HTTP transport using the Python standard library."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from .exceptions import NetworkError


class HttpClient:
    DEFAULT_TIMEOUT = 30

    def __init__(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.timeout = timeout

    def get(self, url: str, params: dict[str, Any]) -> tuple[int, str]:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        full_url = f"{url}?{query}" if query else url
        request = urllib.request.Request(
            full_url,
            headers={
                "Accept": "application/json",
                "User-Agent": "vindecodervehicle-python-sdk/1.0",
            },
            method="GET",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.status, response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return exc.code, body
        except urllib.error.URLError as exc:
            raise NetworkError(f"Network error while calling VIN Decoder API: {exc.reason}") from exc

    @staticmethod
    def decode_json(body: str) -> dict[str, Any]:
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise NetworkError("Invalid JSON response from VIN Decoder API.") from exc

        if not isinstance(payload, dict):
            raise NetworkError("Expected a JSON object from VIN Decoder API.")

        return payload