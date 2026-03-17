"""Mailboxes resource for FreeScout API."""

from __future__ import annotations

from typing import Any

from freescout.models import (
    FolderList,
    MailboxCustomFieldList,
    MailboxList,
)
from freescout.resources.base import BaseResource


class MailboxesResource(BaseResource):
    """Resource for managing mailboxes."""

    def list(
        self,
        *,
        user_id: int | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> MailboxList:
        """List mailboxes.

        Args:
            user_id: Filter by user ID (mailboxes the user has access to).
            page: Page number.
            page_size: Number of items per page.

        Returns:
            MailboxList containing mailboxes and pagination info.
        """
        params: dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }

        if user_id is not None:
            params["userId"] = user_id

        result = self._transport.get("mailboxes", params=params)
        return MailboxList.from_response(result or {})

    def list_custom_fields(
        self,
        mailbox_id: int,
    ) -> MailboxCustomFieldList:
        """List custom fields for a mailbox.

        Args:
            mailbox_id: The mailbox ID.

        Returns:
            MailboxCustomFieldList containing custom field definitions.
        """
        result = self._transport.get(f"mailboxes/{mailbox_id}/custom_fields")
        return MailboxCustomFieldList.from_response(result or {})

    def list_folders(
        self,
        mailbox_id: int,
    ) -> FolderList:
        """List folders for a mailbox.

        Args:
            mailbox_id: The mailbox ID.

        Returns:
            FolderList containing folders and pagination info.
        """
        result = self._transport.get(f"mailboxes/{mailbox_id}/folders")
        return FolderList.from_response(result or {})
