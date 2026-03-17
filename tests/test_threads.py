"""Tests for the Threads resource."""

import responses

from freescout import FreeScoutClient
from freescout.enums import ConversationStatus, ThreadType


class TestThreadsCreate:
    """Tests for creating threads."""

    @responses.activate
    def test_create_customer_thread(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test creating a customer reply thread."""
        responses.add(
            responses.POST,
            f"{base_url}/api/conversations/1/threads",
            headers={"Resource-ID": "42"},
            status=201,
        )

        thread_id = client.threads.create(
            conversation_id=1,
            type=ThreadType.CUSTOMER,
            text="Thank you for your help!",
            customer={"email": "customer@example.com"},
        )

        assert thread_id == 42

    @responses.activate
    def test_create_message_thread(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test creating a user message thread."""
        responses.add(
            responses.POST,
            f"{base_url}/api/conversations/1/threads",
            headers={"Resource-ID": "43"},
            status=201,
        )

        thread_id = client.threads.create(
            conversation_id=1,
            type=ThreadType.MESSAGE,
            text="Let us know if you need anything else.",
            user=33,
            status=ConversationStatus.CLOSED,
        )

        assert thread_id == 43

    @responses.activate
    def test_create_note_thread(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test creating a note thread."""
        responses.add(
            responses.POST,
            f"{base_url}/api/conversations/1/threads",
            headers={"Resource-ID": "44"},
            status=201,
        )

        thread_id = client.threads.create(
            conversation_id=1,
            type=ThreadType.NOTE,
            text="Internal note: Customer is a VIP.",
            user=33,
        )

        assert thread_id == 44

    @responses.activate
    def test_create_thread_with_attachments(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test creating a thread with attachments."""
        responses.add(
            responses.POST,
            f"{base_url}/api/conversations/1/threads",
            headers={"Resource-ID": "45"},
            status=201,
        )

        thread_id = client.threads.create(
            conversation_id=1,
            type=ThreadType.MESSAGE,
            text="Please see the attached file.",
            user=33,
            attachments=[
                {
                    "fileName": "document.pdf",
                    "mimeType": "application/pdf",
                    "data": "base64encodeddata",
                }
            ],
        )

        assert thread_id == 45

    @responses.activate
    def test_create_thread_with_recipients(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test creating a thread with CC and BCC recipients."""
        responses.add(
            responses.POST,
            f"{base_url}/api/conversations/1/threads",
            headers={"Resource-ID": "46"},
            status=201,
        )

        thread_id = client.threads.create(
            conversation_id=1,
            type=ThreadType.MESSAGE,
            text="Reply with multiple recipients.",
            user=33,
            to=["primary@example.com"],
            cc=["cc1@example.com", "cc2@example.com"],
            bcc=["bcc@example.com"],
        )

        assert thread_id == 46
