"""Exception classes."""

from __future__ import annotations

from typing import Any, Optional


class FinWiseError(Exception):
    """
    Base exception for all FinWise SDK errors.

    Attributes:
        message: Human-readable error message.
        request_id: Request ID for debugging (if available).
    """

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
    ) -> None:
        self.message = message
        self.request_id = request_id
        super().__init__(message)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"request_id={self.request_id!r})"
        )


class FinWiseAPIError(FinWiseError):
    """
    API returned an error response.

    Attributes:
        status_code: HTTP status code.
        response_body: Raw response body (if available).
        error_code: API-specific error code (if available).
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        request_id: Optional[str] = None,
        response_body: Optional[dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        self.error_code = error_code
        super().__init__(message, request_id=request_id)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code}, "
            f"request_id={self.request_id!r})"
        )


class AuthenticationError(FinWiseAPIError):
    """
    Invalid or missing API key (HTTP 401).

    This error occurs when:
    - The API key is missing from the request
    - The API key is invalid or expired
    - The API key has been revoked
    """

    pass


class PermissionDeniedError(FinWiseAPIError):
    """
    Permission denied (HTTP 403).

    This error occurs when the API key doesn't have permission
    to perform the requested operation.
    """

    pass


class NotFoundError(FinWiseAPIError):
    """
    Resource not found (HTTP 404).

    This error occurs when the requested resource doesn't exist
    or has been deleted.
    """

    pass


class ValidationError(FinWiseAPIError):
    """
    Request validation failed (HTTP 400, 422).

    This error occurs when the request body contains invalid data.
    Check the response_body for detailed validation errors.
    """

    pass


class ConflictError(FinWiseAPIError):
    """
    Conflict error (HTTP 409).

    This error occurs when the request conflicts with the current
    state of the resource (e.g., duplicate entry).
    """

    pass


class RateLimitError(FinWiseAPIError):
    """
    Rate limit exceeded (HTTP 429).

    Attributes:
        retry_after: Seconds to wait before retrying (if provided by the API).
    """

    def __init__(
        self,
        message: str,
        *,
        retry_after: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, **kwargs)


class ServerError(FinWiseAPIError):
    """
    Server error (HTTP 5xx).

    This error indicates a problem on the FinWise server.
    These are typically transient and can be retried.
    """

    pass


class FinWiseConnectionError(FinWiseError):
    """
    Network connection error.

    This error occurs when the SDK cannot establish a connection
    to the FinWise API server.
    """

    pass


class FinWiseTimeoutError(FinWiseError):
    """
    Request timed out.

    This error occurs when the request takes longer than the
    configured timeout.
    """

    pass


def raise_for_status(
    status_code: int,
    response_body: dict[str, Any],
    request_id: Optional[str] = None,
) -> None:
    """
    Raise appropriate exception based on HTTP status code.

    Args:
        status_code: HTTP status code from the response.
        response_body: Parsed JSON response body.
        request_id: Request ID for debugging.

    Raises:
        FinWiseAPIError: Appropriate subclass based on status code.
    """
    message = response_body.get("message", "Unknown error")
    error_code = response_body.get("code")

    kwargs: dict[str, Any] = {
        "status_code": status_code,
        "request_id": request_id,
        "response_body": response_body,
        "error_code": error_code,
    }

    exception_map: dict[int, type[FinWiseAPIError]] = {
        400: ValidationError,
        401: AuthenticationError,
        403: PermissionDeniedError,
        404: NotFoundError,
        409: ConflictError,
        422: ValidationError,
        429: RateLimitError,
    }

    if status_code in exception_map:
        exc_class = exception_map[status_code]
        if exc_class == RateLimitError:
            kwargs["retry_after"] = response_body.get("retryAfter")
        raise exc_class(message, **kwargs)

    if 500 <= status_code < 600:
        raise ServerError(message, **kwargs)

    raise FinWiseAPIError(message, **kwargs)
