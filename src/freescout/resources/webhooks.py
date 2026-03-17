"""Webhooks resource for FreeScout API."""

from __future__ import annotations

from typing import Any

from freescout.enums import WebhookEvent
from freescout.models import WebhookList
from freescout.resources.base import BaseResource


class WebhooksResource(BaseResource):
    """Resource for managing webhooks."""

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> WebhookList:
        """List webhooks.

        Args:
            page: Page number.
            page_size: Number of items per page.

        Returns:
            WebhookList containing webhooks and pagination info.
        """
        params: dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }

        result = self._transport.get("webhooks", params=params)
        return WebhookList.from_response(result or {})

    def create(
        self,
        *,
        url: str,
        events: list[WebhookEvent | str],
        mailboxes: list[int] | None = None,
    ) -> int:
        """Create a new webhook.

        Args:
            url: URL to send webhook events to.
            events: List of event types to subscribe to.
            mailboxes: List of mailbox IDs to limit events to.

        Returns:
            ID of the created webhook.
        """
        data: dict[str, Any] = {
            "url": url,
            "events": [str(e) for e in events],
        }

        if mailboxes is not None:
            data["mailboxes"] = mailboxes

        result = self._transport.post("webhooks", data=data)
        return result["id"] if result else 0

    def delete(self, webhook_id: int) -> None:
        """Delete a webhook.

        Args:
            webhook_id: The webhook ID.
        """
        self._transport.delete(f"webhooks/{webhook_id}")
