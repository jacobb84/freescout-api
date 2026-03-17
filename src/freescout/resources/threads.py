"""Threads resource for FreeScout API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from freescout.enums import ConversationStatus, ThreadState, ThreadType
from freescout.resources.base import BaseResource


class ThreadsResource(BaseResource):
    """Resource for managing conversation threads."""

    def create(
        self,
        conversation_id: int,
        *,
        type: ThreadType | str,
        text: str,
        customer: dict[str, Any] | None = None,
        user: int | None = None,
        imported: bool = False,
        status: ConversationStatus | str | None = None,
        state: ThreadState | str | None = None,
        to: list[str] | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        created_at: datetime | str | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> int:
        """Create a new thread in a conversation.

        This method adds a new customer reply, user reply, or user note
        to a conversation.

        Args:
            conversation_id: The conversation ID.
            type: Thread type (customer, message, note).
            text: Thread body/content.
            customer: Customer data (for customer type threads).
            user: User ID (for message/note type threads).
            imported: Whether this is an imported thread.
            status: Set conversation status after adding thread.
            state: Thread state (draft, published).
            to: List of recipient email addresses.
            cc: List of CC email addresses.
            bcc: List of BCC email addresses.
            created_at: Custom creation timestamp.
            attachments: List of attachment dicts with fileName, mimeType,
                        and either "data" (base64) or "fileUrl".

        Returns:
            ID of the created thread.
        """
        data: dict[str, Any] = {
            "type": str(type),
            "text": text,
            "imported": imported,
        }

        if customer is not None:
            data["customer"] = customer
        if user is not None:
            data["user"] = user
        if status is not None:
            data["status"] = str(status)
        if state is not None:
            data["state"] = str(state)
        if to is not None:
            data["to"] = to
        if cc is not None:
            data["cc"] = cc
        if bcc is not None:
            data["bcc"] = bcc
        if created_at is not None:
            data["createdAt"] = (
                created_at.isoformat() if isinstance(created_at, datetime) else created_at
            )
        if attachments is not None:
            data["attachments"] = attachments

        result = self._transport.post(f"conversations/{conversation_id}/threads", data=data)
        return result["id"] if result else 0
