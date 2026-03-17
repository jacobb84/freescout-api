"""Base resource class for FreeScout API resources."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from freescout._transport import Transport


class BaseResource:
    """Base class for all API resource wrappers."""

    def __init__(self, transport: "Transport") -> None:
        """Initialize the resource.

        Args:
            transport: Transport instance for making API requests.
        """
        self._transport = transport
