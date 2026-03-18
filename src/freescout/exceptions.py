"""Exception classes for the FreeScout API client."""

from typing import Any


class FreeScoutError(Exception):
    """Base exception for all FreeScout API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        request_url: str | None = None,
        request_method: str | None = None,
        response_text: str | None = None,
        response_headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize FreeScoutError.

        Args:
            message: Human-readable error message.
            status_code: HTTP status code from the API response.
            response_data: Raw response data from the API.
            request_url: The URL that was requested.
            request_method: The HTTP method used.
            response_text: Raw response body text.
            response_headers: Response headers.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        self.request_url = request_url
        self.request_method = request_method
        self.response_text = response_text
        self.response_headers = response_headers or {}

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(FreeScoutError):
    """Raised when authentication fails (401 Unauthorized)."""

    pass


class ForbiddenError(FreeScoutError):
    """Raised when access is forbidden (403 Forbidden)."""

    pass


class NotFoundError(FreeScoutError):
    """Raised when a resource is not found (404 Not Found)."""

    pass


class ValidationError(FreeScoutError):
    """Raised when request validation fails (400 Bad Request)."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        """Initialize ValidationError.

        Args:
            message: Human-readable error message.
            status_code: HTTP status code from the API response.
            response_data: Raw response data from the API.
            errors: List of validation error details.
        """
        super().__init__(message, status_code, response_data)
        self.errors = errors or []


class ConflictError(FreeScoutError):
    """Raised when there's a conflict (409 Conflict)."""

    pass


class RateLimitError(FreeScoutError):
    """Raised when rate limit is exceeded (429 Too Many Requests)."""

    pass


class ServerError(FreeScoutError):
    """Raised when a server error occurs (5xx errors)."""

    pass
