"""Tests for the Webhooks resource."""

import responses

from freescout import FreeScoutClient
from freescout.enums import WebhookEvent


class TestWebhooksList:
    """Tests for listing webhooks."""

    @responses.activate
    def test_list_webhooks(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing webhooks."""
        responses.add(
            responses.GET,
            f"{base_url}/api/webhooks",
            json={
                "_embedded": {
                    "webhooks": [
                        {
                            "id": 1,
                            "url": "https://example.org/webhook",
                            "events": ["convo.created", "convo.assigned"],
                            "mailboxes": [1, 3],
                            "lastRunTime": "2024-02-27T15:30:00Z",
                            "lastRunError": "",
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

        result = client.webhooks.list()

        assert len(result.webhooks) == 1
        assert result.webhooks[0].id == 1
        assert result.webhooks[0].url == "https://example.org/webhook"
        assert "convo.created" in result.webhooks[0].events


class TestWebhooksCreate:
    """Tests for creating webhooks."""

    @responses.activate
    def test_create_webhook(self, client: FreeScoutClient, base_url: str) -> None:
        """Test creating a webhook."""
        responses.add(
            responses.POST,
            f"{base_url}/api/webhooks",
            headers={"Resource-ID": "17"},
            status=201,
        )

        webhook_id = client.webhooks.create(
            url="https://example.org/new-webhook",
            events=[WebhookEvent.CONVO_CREATED, WebhookEvent.CONVO_ASSIGNED],
        )

        assert webhook_id == 17

    @responses.activate
    def test_create_webhook_with_mailboxes(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test creating a webhook with specific mailboxes."""
        responses.add(
            responses.POST,
            f"{base_url}/api/webhooks",
            headers={"Resource-ID": "18"},
            status=201,
        )

        webhook_id = client.webhooks.create(
            url="https://example.org/new-webhook",
            events=[WebhookEvent.CONVO_CREATED],
            mailboxes=[1, 2],
        )

        assert webhook_id == 18


class TestWebhooksDelete:
    """Tests for deleting webhooks."""

    @responses.activate
    def test_delete_webhook(self, client: FreeScoutClient, base_url: str) -> None:
        """Test deleting a webhook."""
        responses.add(
            responses.DELETE,
            f"{base_url}/api/webhooks/17",
            status=204,
        )

        client.webhooks.delete(17)

        assert len(responses.calls) == 1
