"""Conversations resource for FreeScout API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from freescout.enums import (
    ConversationStatus,
    ConversationState,
    ConversationType,
    SortField,
    SortOrder,
)
from freescout.models import (
    Conversation,
    ConversationList,
    CustomField,
    TimelogList,
)
from freescout.resources.base import BaseResource


class ConversationsResource(BaseResource):
    """Resource for managing conversations."""

    def list(
        self,
        *,
        mailbox_id: int | None = None,
        folder_id: int | None = None,
        status: ConversationStatus | str | None = None,
        state: ConversationState | str | None = None,
        type: ConversationType | str | None = None,
        assigned_to: int | None = None,
        customer_email: str | None = None,
        customer_phone: str | None = None,
        customer_id: int | None = None,
        number: int | None = None,
        subject: str | None = None,
        tag: str | None = None,
        created_by_user_id: int | None = None,
        created_by_customer_id: int | None = None,
        created_since: datetime | str | None = None,
        updated_since: datetime | str | None = None,
        sort_field: SortField | str = SortField.CREATED_AT,
        sort_order: SortOrder | str = SortOrder.DESC,
        embed: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> ConversationList:
        """List conversations with optional filters.

        Args:
            mailbox_id: Filter by mailbox ID.
            folder_id: Filter by folder ID.
            status: Filter by conversation status.
            state: Filter by conversation state.
            type: Filter by conversation type.
            assigned_to: Filter by assigned user ID.
            customer_email: Filter by customer email.
            customer_phone: Filter by customer phone.
            customer_id: Filter by customer ID.
            number: Filter by conversation number.
            subject: Filter by subject (partial match).
            tag: Filter by tag name.
            created_by_user_id: Filter by user who created.
            created_by_customer_id: Filter by customer who created.
            created_since: Filter conversations created after this date.
            updated_since: Filter conversations updated after this date.
            sort_field: Field to sort by.
            sort_order: Sort order (asc or desc).
            embed: Embed related resources (e.g., "threads").
            page: Page number.
            page_size: Number of items per page.

        Returns:
            ConversationList containing conversations and pagination info.
        """
        params: dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "sortField": str(sort_field),
            "sortOrder": str(sort_order),
        }

        if mailbox_id is not None:
            params["mailboxId"] = mailbox_id
        if folder_id is not None:
            params["folderId"] = folder_id
        if status is not None:
            params["status"] = str(status)
        if state is not None:
            params["state"] = str(state)
        if type is not None:
            params["type"] = str(type)
        if assigned_to is not None:
            params["assignedTo"] = assigned_to
        if customer_email is not None:
            params["customerEmail"] = customer_email
        if customer_phone is not None:
            params["customerPhone"] = customer_phone
        if customer_id is not None:
            params["customerId"] = customer_id
        if number is not None:
            params["number"] = number
        if subject is not None:
            params["subject"] = subject
        if tag is not None:
            params["tag"] = tag
        if created_by_user_id is not None:
            params["createdByUserId"] = created_by_user_id
        if created_by_customer_id is not None:
            params["createdByCustomerId"] = created_by_customer_id
        if created_since is not None:
            params["createdSince"] = (
                created_since.isoformat() if isinstance(created_since, datetime) else created_since
            )
        if updated_since is not None:
            params["updatedSince"] = (
                updated_since.isoformat() if isinstance(updated_since, datetime) else updated_since
            )
        if embed is not None:
            params["embed"] = embed

        result = self._transport.get("conversations", params=params)
        return ConversationList.from_response(result or {})

    def get(
        self,
        conversation_id: int,
        *,
        embed: str | None = "threads",
    ) -> Conversation:
        """Get a single conversation by ID.

        Args:
            conversation_id: The conversation ID.
            embed: Embed related resources (e.g., "threads").

        Returns:
            Conversation object.
        """
        params: dict[str, Any] = {}
        if embed is not None:
            params["embed"] = embed

        result = self._transport.get(f"conversations/{conversation_id}", params=params)
        return Conversation.model_validate(result)

    def create(
        self,
        *,
        mailbox_id: int,
        subject: str,
        customer: dict[str, Any],
        threads: list[dict[str, Any]],
        type: ConversationType | str = ConversationType.EMAIL,
        status: ConversationStatus | str = ConversationStatus.ACTIVE,
        assign_to: int | None = None,
        imported: bool = False,
        custom_fields: list[dict[str, Any]] | None = None,
        created_at: datetime | str | None = None,
        closed_at: datetime | str | None = None,
    ) -> int:
        """Create a new conversation.

        Args:
            mailbox_id: ID of the mailbox.
            subject: Conversation subject.
            customer: Customer data (must include "email").
            threads: List of thread data.
            type: Conversation type.
            status: Conversation status.
            assign_to: User ID to assign the conversation to.
            imported: Whether this is an imported conversation.
            custom_fields: List of custom field values.
            created_at: Custom creation timestamp.
            closed_at: Custom closed timestamp.

        Returns:
            ID of the created conversation.
        """
        data: dict[str, Any] = {
            "mailboxId": mailbox_id,
            "subject": subject,
            "customer": customer,
            "threads": threads,
            "type": str(type),
            "status": str(status),
            "imported": imported,
        }

        if assign_to is not None:
            data["assignTo"] = assign_to
        if custom_fields is not None:
            data["customFields"] = custom_fields
        if created_at is not None:
            data["createdAt"] = (
                created_at.isoformat() if isinstance(created_at, datetime) else created_at
            )
        if closed_at is not None:
            data["closedAt"] = (
                closed_at.isoformat() if isinstance(closed_at, datetime) else closed_at
            )

        result = self._transport.post("conversations", data=data)
        return result["id"] if result else 0

    def update(
        self,
        conversation_id: int,
        *,
        by_user: int | None = None,
        status: ConversationStatus | str | None = None,
        assign_to: int | None = None,
        mailbox_id: int | None = None,
        customer_id: int | None = None,
        subject: str | None = None,
    ) -> None:
        """Update a conversation.

        Args:
            conversation_id: The conversation ID.
            by_user: User ID making the change.
            status: New status.
            assign_to: User ID to assign to.
            mailbox_id: New mailbox ID.
            customer_id: New customer ID.
            subject: New subject.
        """
        data: dict[str, Any] = {}

        if by_user is not None:
            data["byUser"] = by_user
        if status is not None:
            data["status"] = str(status)
        if assign_to is not None:
            data["assignTo"] = assign_to
        if mailbox_id is not None:
            data["mailboxId"] = mailbox_id
        if customer_id is not None:
            data["customerId"] = customer_id
        if subject is not None:
            data["subject"] = subject

        self._transport.put(f"conversations/{conversation_id}", data=data)

    def delete(self, conversation_id: int) -> None:
        """Delete a conversation permanently.

        Args:
            conversation_id: The conversation ID.
        """
        self._transport.delete(f"conversations/{conversation_id}")

    def update_custom_fields(
        self,
        conversation_id: int,
        custom_fields: list[dict[str, Any]],
    ) -> None:
        """Update custom fields on a conversation.

        Args:
            conversation_id: The conversation ID.
            custom_fields: List of custom field updates, each with "id" and "value".
        """
        data = {"customFields": custom_fields}
        self._transport.put(f"conversations/{conversation_id}/custom_fields", data=data)

    def update_tags(
        self,
        conversation_id: int,
        tags: list[str],
    ) -> None:
        """Update tags on a conversation.

        Args:
            conversation_id: The conversation ID.
            tags: List of tag names.
        """
        data = {"tags": tags}
        self._transport.put(f"conversations/{conversation_id}/tags", data=data)

    def list_timelogs(
        self,
        conversation_id: int,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> TimelogList:
        """List timelogs for a conversation.

        Args:
            conversation_id: The conversation ID.
            page: Page number.
            page_size: Number of items per page.

        Returns:
            TimelogList containing timelogs and pagination info.
        """
        params = {"page": page, "pageSize": page_size}
        result = self._transport.get(f"conversations/{conversation_id}/timelogs", params=params)
        return TimelogList.from_response(result or {})
