"""Internal HTTP transport helpers for FreeScout API client."""

import time
from collections.abc import Iterator
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from freescout._version import __version__
from freescout.exceptions import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    FreeScoutError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5


def create_session(
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
) -> requests.Session:
    """Create a requests Session with retry configuration.

    Args:
        max_retries: Maximum number of retries for failed requests.
        backoff_factor: Backoff factor for retries.

    Returns:
        Configured requests Session.
    """
    session = requests.Session()

    if max_retries > 0:
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

    return session


def handle_response(response: requests.Response) -> dict[str, Any] | None:
    """Handle API response and raise appropriate exceptions.

    Args:
        response: The requests Response object.

    Returns:
        Parsed JSON response data, or None for 204 responses.

    Raises:
        AuthenticationError: For 401 responses.
        ForbiddenError: For 403 responses.
        NotFoundError: For 404 responses.
        ValidationError: For 400 responses.
        ConflictError: For 409 responses.
        RateLimitError: For 429 responses.
        ServerError: For 5xx responses.
        FreeScoutError: For other error responses.
    """
    status_code = response.status_code

    if status_code == 204:
        return None

    if status_code in (200, 201):
        if response.headers.get("Resource-ID"):
            return {"id": int(response.headers["Resource-ID"])}
        try:
            return response.json()
        except ValueError:
            return None

    try:
        error_data = response.json()
    except ValueError:
        error_data = {"message": response.text or "Unknown error"}

    message = error_data.get("message", "API error")
    errors = error_data.get("_embedded", {}).get("errors", [])
    
    # Common kwargs for all exceptions
    common_kwargs = {
        "message": message,
        "status_code": status_code,
        "response_data": error_data,
        "request_url": response.request.url,
        "request_method": response.request.method,
        "response_text": response.text,
        "response_headers": dict(response.headers),
    }

    if status_code == 400:
        raise ValidationError(
            **common_kwargs,
            errors=errors,
        )
    elif status_code == 401:
        raise AuthenticationError(**common_kwargs)
    elif status_code == 403:
        raise ForbiddenError(**common_kwargs)
    elif status_code == 404:
        raise NotFoundError(**common_kwargs)
    elif status_code == 409:
        raise ConflictError(**common_kwargs)
    elif status_code == 429:
        raise RateLimitError(**common_kwargs)
    elif status_code >= 500:
        raise ServerError(**common_kwargs)
    else:
        raise FreeScoutError(**common_kwargs)


class Paginator:
    """Iterator for paginated API responses.

    Handles automatic pagination through list endpoints.
    """

    def __init__(
        self,
        transport: "Transport",
        endpoint: str,
        params: dict[str, Any] | None = None,
        page_size: int = 50,
        max_pages: int | None = None,
    ) -> None:
        """Initialize Paginator.

        Args:
            transport: Transport instance for making requests.
            endpoint: API endpoint path.
            params: Query parameters for the request.
            page_size: Number of items per page.
            max_pages: Maximum number of pages to fetch (None for all).
        """
        self.transport = transport
        self.endpoint = endpoint
        self.params = params or {}
        self.page_size = page_size
        self.max_pages = max_pages
        self.current_page = 0
        self.total_pages: int | None = None

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """Iterate through all pages."""
        return self

    def __next__(self) -> dict[str, Any]:
        """Get the next page of results."""
        if self.total_pages is not None and self.current_page >= self.total_pages:
            raise StopIteration

        if self.max_pages is not None and self.current_page >= self.max_pages:
            raise StopIteration

        self.current_page += 1
        params = {
            **self.params,
            "page": self.current_page,
            "pageSize": self.page_size,
        }

        result = self.transport.get(self.endpoint, params=params)
        if result is None:
            raise StopIteration

        page_info = result.get("page", {})
        self.total_pages = page_info.get("totalPages", 1)

        return result


class Transport:
    """HTTP transport layer for making API requests."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize Transport.

        Args:
            base_url: Base URL for the FreeScout API.
            api_key: API key for authentication.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            session: Optional pre-configured requests Session.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session = session or create_session(max_retries=max_retries)

    def _get_headers(self) -> dict[str, str]:
        """Get headers for API requests."""
        return {
            "X-FreeScout-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"freescout-api-python/{__version__}",
        }

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/api/{endpoint}"

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Make a GET request.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            Response data.
        """
        url = self._build_url(endpoint)
        response = self.session.get(
            url,
            headers=self._get_headers(),
            params=params,
            timeout=self.timeout,
        )
        return handle_response(response)

    def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Make a POST request.

        Args:
            endpoint: API endpoint path.
            data: Request body data.

        Returns:
            Response data.
        """
        url = self._build_url(endpoint)
        response = self.session.post(
            url,
            headers=self._get_headers(),
            json=data,
            timeout=self.timeout,
        )
        return handle_response(response)

    def put(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Make a PUT request.

        Args:
            endpoint: API endpoint path.
            data: Request body data.

        Returns:
            Response data.
        """
        url = self._build_url(endpoint)
        response = self.session.put(
            url,
            headers=self._get_headers(),
            json=data,
            timeout=self.timeout,
        )
        return handle_response(response)

    def delete(
        self,
        endpoint: str,
    ) -> dict[str, Any] | None:
        """Make a DELETE request.

        Args:
            endpoint: API endpoint path.

        Returns:
            Response data.
        """
        url = self._build_url(endpoint)
        response = self.session.delete(
            url,
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        return handle_response(response)

    def paginate(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        page_size: int = 50,
        max_pages: int | None = None,
    ) -> Paginator:
        """Create a paginator for the given endpoint.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.
            page_size: Number of items per page.
            max_pages: Maximum number of pages to fetch.

        Returns:
            Paginator instance.
        """
        return Paginator(
            transport=self,
            endpoint=endpoint,
            params=params,
            page_size=page_size,
            max_pages=max_pages,
        )
