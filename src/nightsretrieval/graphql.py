"""HTTP client for talking to the RA GraphQL endpoint.

The original implementation called ``requests.post`` without a timeout, which
left the scraper able to hang forever on a slow upstream. We now use a session
with bounded timeouts and exponential backoff on retryable status codes.
"""

from __future__ import annotations

from typing import Any

import requests
import structlog
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = structlog.get_logger(__name__)

_DEFAULT_TIMEOUT = (5.0, 15.0)  # (connect, read) seconds


def _build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST"]),
        raise_on_status=False,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session


_SESSION = _build_session()


def send_graphql_request(api_url: str, payload: dict[str, Any]) -> Any:
    headers = {
        "content-type": "application/json",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        ),
    }

    try:
        response = _SESSION.post(api_url, json=payload, headers=headers, timeout=_DEFAULT_TIMEOUT)
    except requests.exceptions.RequestException:
        logger.exception("ra_graphql_request_failed", url=api_url)
        return None

    if not response.ok:
        logger.warning(
            "ra_graphql_non_ok_response",
            url=api_url,
            status=response.status_code,
            body=response.text[:500],
        )
        return None

    try:
        return response.json()
    except ValueError:
        logger.exception("ra_graphql_invalid_json", url=api_url)
        return None
