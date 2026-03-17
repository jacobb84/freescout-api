"""Tests for the FreeScoutClient class."""

import os
from unittest.mock import patch

import pytest

from freescout import FreeScoutClient
from freescout.exceptions import FreeScoutError
from freescout.resources.conversations import ConversationsResource
from freescout.resources.customers import CustomersResource
from freescout.resources.mailboxes import MailboxesResource
from freescout.resources.tags import TagsResource
from freescout.resources.threads import ThreadsResource
from freescout.resources.users import UsersResource
from freescout.resources.webhooks import WebhooksResource


class TestClientInitialization:
    """Tests for client initialization."""

    def test_init_with_explicit_credentials(self) -> None:
        """Test client initialization with explicit credentials."""
        client = FreeScoutClient(
            base_url="https://support.example.com",
            api_key="test-key",
        )
        assert client.base_url == "https://support.example.com"

    def test_init_with_environment_variables(self) -> None:
        """Test client initialization with environment variables."""
        with patch.dict(
            os.environ,
            {
                "FREESCOUT_URL": "https://env.example.com",
                "FREESCOUT_API_KEY": "env-key",
            },
        ):
            client = FreeScoutClient()
            assert client.base_url == "https://env.example.com"

    def test_init_missing_base_url_raises_error(self) -> None:
        """Test that missing base_url raises FreeScoutError."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("FREESCOUT_URL", None)
            os.environ.pop("FREESCOUT_API_KEY", None)
            with pytest.raises(FreeScoutError) as exc_info:
                FreeScoutClient(api_key="test-key")
            assert "base_url is required" in str(exc_info.value)

    def test_init_missing_api_key_raises_error(self) -> None:
        """Test that missing api_key raises FreeScoutError."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("FREESCOUT_URL", None)
            os.environ.pop("FREESCOUT_API_KEY", None)
            with pytest.raises(FreeScoutError) as exc_info:
                FreeScoutClient(base_url="https://example.com")
            assert "api_key is required" in str(exc_info.value)

    def test_custom_timeout(self) -> None:
        """Test client initialization with custom timeout."""
        client = FreeScoutClient(
            base_url="https://example.com",
            api_key="test-key",
            timeout=60,
        )
        assert client._transport.timeout == 60


class TestClientResources:
    """Tests for client resource access."""

    def test_conversations_resource(self, client: FreeScoutClient) -> None:
        """Test accessing conversations resource."""
        assert isinstance(client.conversations, ConversationsResource)
        assert client.conversations is client.conversations

    def test_customers_resource(self, client: FreeScoutClient) -> None:
        """Test accessing customers resource."""
        assert isinstance(client.customers, CustomersResource)
        assert client.customers is client.customers

    def test_mailboxes_resource(self, client: FreeScoutClient) -> None:
        """Test accessing mailboxes resource."""
        assert isinstance(client.mailboxes, MailboxesResource)
        assert client.mailboxes is client.mailboxes

    def test_tags_resource(self, client: FreeScoutClient) -> None:
        """Test accessing tags resource."""
        assert isinstance(client.tags, TagsResource)
        assert client.tags is client.tags

    def test_threads_resource(self, client: FreeScoutClient) -> None:
        """Test accessing threads resource."""
        assert isinstance(client.threads, ThreadsResource)
        assert client.threads is client.threads

    def test_users_resource(self, client: FreeScoutClient) -> None:
        """Test accessing users resource."""
        assert isinstance(client.users, UsersResource)
        assert client.users is client.users

    def test_webhooks_resource(self, client: FreeScoutClient) -> None:
        """Test accessing webhooks resource."""
        assert isinstance(client.webhooks, WebhooksResource)
        assert client.webhooks is client.webhooks


class TestClientRepr:
    """Tests for client string representation."""

    def test_repr(self, client: FreeScoutClient) -> None:
        """Test client __repr__."""
        repr_str = repr(client)
        assert "FreeScoutClient" in repr_str
        assert "support.example.com" in repr_str
