"""FreeScout API Client."""

import os
from typing import Any

import requests

from freescout._transport import Transport
from freescout.exceptions import FreeScoutError
from freescout.resources.conversations import ConversationsResource
from freescout.resources.customers import CustomersResource
from freescout.resources.mailboxes import MailboxesResource
from freescout.resources.tags import TagsResource
from freescout.resources.threads import ThreadsResource
from freescout.resources.users import UsersResource
from freescout.resources.webhooks import WebhooksResource


class FreeScoutClient:
    """Client for interacting with the FreeScout API.

    This client provides access to all FreeScout API resources through
    resource-specific attributes.

    Example:
        ```python
        from freescout import FreeScoutClient

        # Using environment variables
        client = FreeScoutClient()

        # Or with explicit credentials
        client = FreeScoutClient(
            base_url="https://support.example.com",
            api_key="your-api-key"
        )

        # List conversations
        conversations = client.conversations.list(mailbox_id=1)
        for conv in conversations.conversations:
            print(conv.subject)

        # Get a specific customer
        customer = client.customers.get(123)
        print(customer.first_name)
        ```

    Attributes:
        conversations: Resource for managing conversations.
        customers: Resource for managing customers.
        mailboxes: Resource for managing mailboxes.
        tags: Resource for managing tags.
        threads: Resource for managing conversation threads.
        users: Resource for managing users.
        webhooks: Resource for managing webhooks.
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize the FreeScout API client.

        Args:
            base_url: Base URL for the FreeScout instance. If not provided,
                uses the FREESCOUT_URL environment variable.
            api_key: API key for authentication. If not provided, uses the
                FREESCOUT_API_KEY environment variable.
            timeout: Request timeout in seconds. Defaults to 30.
            max_retries: Maximum number of retries for failed requests.
                Defaults to 3.
            session: Optional pre-configured requests Session.

        Raises:
            FreeScoutError: If base_url or api_key is not provided and
                corresponding environment variable is not set.
        """
        self._base_url = base_url or os.environ.get("FREESCOUT_URL")
        self._api_key = api_key or os.environ.get("FREESCOUT_API_KEY")

        if not self._base_url:
            raise FreeScoutError(
                "base_url is required. Provide it directly or set FREESCOUT_URL "
                "environment variable."
            )

        if not self._api_key:
            raise FreeScoutError(
                "api_key is required. Provide it directly or set FREESCOUT_API_KEY "
                "environment variable."
            )

        self._transport = Transport(
            base_url=self._base_url,
            api_key=self._api_key,
            timeout=timeout,
            max_retries=max_retries,
            session=session,
        )

        self._conversations: ConversationsResource | None = None
        self._customers: CustomersResource | None = None
        self._mailboxes: MailboxesResource | None = None
        self._tags: TagsResource | None = None
        self._threads: ThreadsResource | None = None
        self._users: UsersResource | None = None
        self._webhooks: WebhooksResource | None = None

    @property
    def conversations(self) -> ConversationsResource:
        """Access the conversations resource."""
        if self._conversations is None:
            self._conversations = ConversationsResource(self._transport)
        return self._conversations

    @property
    def customers(self) -> CustomersResource:
        """Access the customers resource."""
        if self._customers is None:
            self._customers = CustomersResource(self._transport)
        return self._customers

    @property
    def mailboxes(self) -> MailboxesResource:
        """Access the mailboxes resource."""
        if self._mailboxes is None:
            self._mailboxes = MailboxesResource(self._transport)
        return self._mailboxes

    @property
    def tags(self) -> TagsResource:
        """Access the tags resource."""
        if self._tags is None:
            self._tags = TagsResource(self._transport)
        return self._tags

    @property
    def threads(self) -> ThreadsResource:
        """Access the threads resource."""
        if self._threads is None:
            self._threads = ThreadsResource(self._transport)
        return self._threads

    @property
    def users(self) -> UsersResource:
        """Access the users resource."""
        if self._users is None:
            self._users = UsersResource(self._transport)
        return self._users

    @property
    def webhooks(self) -> WebhooksResource:
        """Access the webhooks resource."""
        if self._webhooks is None:
            self._webhooks = WebhooksResource(self._transport)
        return self._webhooks

    @property
    def base_url(self) -> str:
        """Get the base URL for the FreeScout instance."""
        return self._base_url

    def __repr__(self) -> str:
        return f"FreeScoutClient(base_url='{self._base_url}')"
