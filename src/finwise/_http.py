"""HTTP transport layer."""

from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING, Any, Optional

import httpx

from finwise._config import ClientConfig
from finwise.exceptions import (
    FinWiseConnectionError,
    FinWiseTimeoutError,
    RateLimitError,
    raise_for_status,
)

if TYPE_CHECKING:
    from httpx import Client as HttpxClient


class HTTPTransport:
    """
    HTTP transport layer with retry logic and error handling.

    Handles:
    - Request/response serialization
    - Automatic retries with exponential backoff
    - Rate limit handling (HTTP 429)
    - Connection and timeout errors
    - Request ID tracking for debugging
    """

    def __init__(
        self,
        config: ClientConfig,
        http_client: Optional[HttpxClient] = None,
    ) -> None:
        """
        Initialize the HTTP transport.

        Args:
            config: Client configuration.
            http_client: Optional custom httpx.Client instance.
        """
        self._config = config
        self._client = http_client or self._create_client()

    def _create_client(self) -> httpx.Client:
        """Create a configured httpx client."""
        return httpx.Client(
            base_url=self._config.base_url,
            timeout=httpx.Timeout(self._config.timeout),
            headers={
                "Authorization": self._config.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"finwise-python/{self._config.version}",
            },
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE).
            path: API endpoint path (e.g., "/accounts").
            json: Request body for POST/PATCH requests.
            params: Query parameters.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            FinWiseAPIError: On API error responses.
            FinWiseConnectionError: On connection failures.
            FinWiseTimeoutError: On request timeout.
        """
        request_id = str(uuid.uuid4())
        headers = {"Request-Id": request_id}

        last_exception: Optional[Exception] = None

        for attempt in range(self._config.max_retries + 1):
            try:
                response = self._client.request(
                    method=method,
                    url=path,
                    json=json,
                    params=params,
                    headers=headers,
                )

                # Handle rate limiting with retry
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "1"))
                    wait_time = min(retry_after, 2**attempt)

                    if attempt < self._config.max_retries:
                        time.sleep(wait_time)
                        continue

                    # Max retries exceeded
                    response_body = response.json() if response.content else {}
                    raise RateLimitError(
                        "Rate limit exceeded",
                        status_code=429,
                        request_id=request_id,
                        response_body=response_body,
                        retry_after=retry_after,
                    )

                # Handle server errors with retry
                if response.status_code >= 500 and attempt < self._config.max_retries:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue

                # Parse response body
                response_body = response.json() if response.content else {}

                # Raise exception for error status codes
                if not response.is_success:
                    raise_for_status(
                        response.status_code,
                        response_body,
                        request_id=request_id,
                    )

                return response_body

            except httpx.ConnectError as e:
                last_exception = e
                if attempt < self._config.max_retries:
                    time.sleep(2**attempt)
                    continue
                raise FinWiseConnectionError(
                    f"Failed to connect to {self._config.base_url}: {e}",
                    request_id=request_id,
                ) from e

            except httpx.TimeoutException as e:
                last_exception = e
                if attempt < self._config.max_retries:
                    time.sleep(2**attempt)
                    continue
                raise FinWiseTimeoutError(
                    f"Request timed out after {self._config.timeout}s",
                    request_id=request_id,
                ) from e

        # Should not reach here, but handle edge case
        if last_exception:
            raise last_exception
        raise RuntimeError("Unexpected state in request retry loop")

    def get(
        self, path: str, *, params: Optional[dict[str, Any]] = None
    ) -> Any:
        """Make a GET request."""
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """Make a POST request."""
        return self.request("POST", path, json=json, params=params)

    def patch(
        self,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """Make a PATCH request."""
        return self.request("PATCH", path, json=json, params=params)

    def delete(
        self, path: str, *, params: Optional[dict[str, Any]] = None
    ) -> Any:
        """Make a DELETE request."""
        return self.request("DELETE", path, params=params)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()
