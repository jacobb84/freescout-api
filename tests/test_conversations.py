"""Tests for the Conversations resource."""

import responses
from responses import matchers

from freescout import FreeScoutClient
from freescout.enums import ConversationStatus, ConversationType


class TestConversationsList:
    """Tests for listing conversations."""

    @responses.activate
    def test_list_conversations(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing conversations."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations",
            json={
                "_embedded": {
                    "conversations": [
                        {
                            "id": 1,
                            "number": 3,
                            "type": "email",
                            "status": "active",
                            "subject": "Test Subject",
                            "mailboxId": 1,
                            "customFields": [],
                        }
                    ]
                },
                "page": {
                    "size": 50,
                    "totalElements": 1,
                    "totalPages": 1,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.conversations.list()

        assert len(result.conversations) == 1
        assert result.conversations[0].id == 1
        assert result.conversations[0].subject == "Test Subject"
        assert result.page.total_elements == 1

    @responses.activate
    def test_list_conversations_with_filters(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test listing conversations with filters."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations",
            json={
                "_embedded": {"conversations": []},
                "page": {
                    "size": 50,
                    "totalElements": 0,
                    "totalPages": 0,
                    "number": 1,
                },
            },
            status=200,
            match=[
                matchers.query_param_matcher(
                    {
                        "mailboxId": "1",
                        "status": "active",
                        "page": "1",
                        "pageSize": "50",
                        "sortField": "createdAt",
                        "sortOrder": "desc",
                    },
                    strict_match=False,
                )
            ],
        )

        result = client.conversations.list(
            mailbox_id=1,
            status=ConversationStatus.ACTIVE,
        )

        assert len(result.conversations) == 0


class TestConversationsGet:
    """Tests for getting a single conversation."""

    @responses.activate
    def test_get_conversation(self, client: FreeScoutClient, base_url: str) -> None:
        """Test getting a single conversation."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations/1",
            json={
                "id": 1,
                "number": 3,
                "type": "email",
                "status": "closed",
                "subject": "Refund Request",
                "mailboxId": 1,
                "customFields": [],
                "_embedded": {
                    "threads": [
                        {
                            "id": 17,
                            "type": "customer",
                            "body": "Please help me.",
                        }
                    ],
                    "timelogs": [],
                    "tags": [],
                },
            },
            status=200,
        )

        conv = client.conversations.get(1)

        assert conv.id == 1
        assert conv.subject == "Refund Request"
        assert conv.status == "closed"
        assert conv.embedded is not None
        assert len(conv.embedded.threads) == 1


class TestConversationsCreate:
    """Tests for creating conversations."""

    @responses.activate
    def test_create_conversation(self, client: FreeScoutClient, base_url: str) -> None:
        """Test creating a conversation."""
        responses.add(
            responses.POST,
            f"{base_url}/api/conversations",
            headers={"Resource-ID": "35"},
            status=201,
        )

        conv_id = client.conversations.create(
            mailbox_id=1,
            subject="New Issue",
            customer={"email": "customer@example.com"},
            threads=[
                {
                    "type": "customer",
                    "text": "I need help with my order.",
                }
            ],
            type=ConversationType.EMAIL,
            status=ConversationStatus.ACTIVE,
        )

        assert conv_id == 35


class TestConversationsUpdate:
    """Tests for updating conversations."""

    @responses.activate
    def test_update_conversation(self, client: FreeScoutClient, base_url: str) -> None:
        """Test updating a conversation."""
        responses.add(
            responses.PUT,
            f"{base_url}/api/conversations/1",
            status=204,
        )

        client.conversations.update(
            1,
            status=ConversationStatus.CLOSED,
            assign_to=5,
        )

        assert len(responses.calls) == 1


class TestConversationsDelete:
    """Tests for deleting conversations."""

    @responses.activate
    def test_delete_conversation(self, client: FreeScoutClient, base_url: str) -> None:
        """Test deleting a conversation."""
        responses.add(
            responses.DELETE,
            f"{base_url}/api/conversations/1",
            status=204,
        )

        client.conversations.delete(1)

        assert len(responses.calls) == 1


class TestConversationsCustomFields:
    """Tests for updating conversation custom fields."""

    @responses.activate
    def test_update_custom_fields(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test updating custom fields."""
        responses.add(
            responses.PUT,
            f"{base_url}/api/conversations/1/custom_fields",
            status=204,
        )

        client.conversations.update_custom_fields(
            1,
            custom_fields=[{"id": 37, "value": "Test value"}],
        )

        assert len(responses.calls) == 1


class TestConversationsTags:
    """Tests for updating conversation tags."""

    @responses.activate
    def test_update_tags(self, client: FreeScoutClient, base_url: str) -> None:
        """Test updating tags."""
        responses.add(
            responses.PUT,
            f"{base_url}/api/conversations/1/tags",
            status=204,
        )

        client.conversations.update_tags(1, tags=["urgent", "billing"])

        assert len(responses.calls) == 1


class TestConversationsTimelogs:
    """Tests for listing conversation timelogs."""

    @responses.activate
    def test_list_timelogs(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing timelogs."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations/1/timelogs",
            json={
                "_embedded": {
                    "timelogs": [
                        {
                            "id": 498,
                            "conversationStatus": "pending",
                            "userId": 1,
                            "timeSpent": 219,
                            "paused": False,
                            "finished": True,
                        }
                    ]
                },
                "page": {
                    "size": 50,
                    "totalElements": 1,
                    "totalPages": 1,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.conversations.list_timelogs(1)

        assert len(result.timelogs) == 1
        assert result.timelogs[0].id == 498
        assert result.timelogs[0].time_spent == 219
