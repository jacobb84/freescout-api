"""Tests for the Mailboxes resource."""

import responses

from freescout import FreeScoutClient


class TestMailboxesList:
    """Tests for listing mailboxes."""

    @responses.activate
    def test_list_mailboxes(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing mailboxes."""
        responses.add(
            responses.GET,
            f"{base_url}/api/mailboxes",
            json={
                "_embedded": {
                    "mailboxes": [
                        {
                            "id": 1,
                            "name": "Support",
                            "email": "support@example.org",
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

        result = client.mailboxes.list()

        assert len(result.mailboxes) == 1
        assert result.mailboxes[0].id == 1
        assert result.mailboxes[0].name == "Support"

    @responses.activate
    def test_list_mailboxes_for_user(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test listing mailboxes for a specific user."""
        responses.add(
            responses.GET,
            f"{base_url}/api/mailboxes",
            json={
                "_embedded": {"mailboxes": []},
                "page": {
                    "size": 50,
                    "totalElements": 0,
                    "totalPages": 0,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.mailboxes.list(user_id=7)

        assert len(result.mailboxes) == 0


class TestMailboxesCustomFields:
    """Tests for listing mailbox custom fields."""

    @responses.activate
    def test_list_custom_fields(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test listing custom fields for a mailbox."""
        responses.add(
            responses.GET,
            f"{base_url}/api/mailboxes/1/custom_fields",
            json={
                "_embedded": {
                    "custom_fields": [
                        {
                            "id": 18,
                            "name": "Priority",
                            "type": "dropdown",
                            "options": {"1": "Low", "2": "Medium", "3": "High"},
                            "required": False,
                            "sortOrder": 1,
                        },
                        {
                            "id": 19,
                            "name": "Purchase Date",
                            "type": "date",
                            "options": None,
                            "required": False,
                            "sortOrder": 3,
                        },
                    ]
                },
                "page": {
                    "size": 50,
                    "totalElements": 2,
                    "totalPages": 1,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.mailboxes.list_custom_fields(1)

        assert len(result.custom_fields) == 2
        assert result.custom_fields[0].name == "Priority"
        assert result.custom_fields[0].type == "dropdown"


class TestMailboxesFolders:
    """Tests for listing mailbox folders."""

    @responses.activate
    def test_list_folders(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing folders for a mailbox."""
        responses.add(
            responses.GET,
            f"{base_url}/api/mailboxes/1/folders",
            json={
                "_embedded": {
                    "folders": [
                        {
                            "id": 1,
                            "name": "Unassigned",
                            "type": "unassigned",
                            "totalCount": 10,
                            "activeCount": 5,
                        },
                        {
                            "id": 2,
                            "name": "Mine",
                            "type": "mine",
                            "userId": 1,
                            "totalCount": 20,
                            "activeCount": 15,
                        },
                    ]
                },
                "page": {
                    "size": 50,
                    "totalElements": 2,
                    "totalPages": 1,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.mailboxes.list_folders(1)

        assert len(result.folders) == 2
        assert result.folders[0].type == "unassigned"
        assert result.folders[1].user_id == 1
