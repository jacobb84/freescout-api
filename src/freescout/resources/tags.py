"""Tags resource for FreeScout API."""

from __future__ import annotations

from typing import Any

from freescout.models import TagList
from freescout.resources.base import BaseResource


class TagsResource(BaseResource):
    """Resource for managing tags."""

    def list(
        self,
        *,
        conversation_id: int | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> TagList:
        """List tags.

        Args:
            conversation_id: Filter by conversation ID (tags on that conversation).
            page: Page number.
            page_size: Number of items per page.

        Returns:
            TagList containing tags and pagination info.
        """
        params: dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }

        if conversation_id is not None:
            params["conversationId"] = conversation_id

        result = self._transport.get("tags", params=params)
        return TagList.from_response(result or {})
