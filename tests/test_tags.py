"""Tests for the Tags resource."""

import responses

from freescout import FreeScoutClient


class TestTagsList:
    """Tests for listing tags."""

    @responses.activate
    def test_list_tags(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing all tags."""
        responses.add(
            responses.GET,
            f"{base_url}/api/tags",
            json={
                "_embedded": {
                    "tags": [
                        {
                            "id": 1,
                            "name": "urgent",
                            "counter": 5,
                            "color": 1,
                        },
                        {
                            "id": 2,
                            "name": "billing",
                            "counter": 10,
                            "color": 2,
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

        result = client.tags.list()

        assert len(result.tags) == 2
        assert result.tags[0].name == "urgent"
        assert result.tags[0].counter == 5
        assert result.tags[1].name == "billing"

    @responses.activate
    def test_list_tags_for_conversation(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test listing tags for a specific conversation."""
        responses.add(
            responses.GET,
            f"{base_url}/api/tags",
            json={
                "_embedded": {
                    "tags": [
                        {
                            "id": 1,
                            "name": "urgent",
                            "counter": 5,
                            "color": 1,
                        },
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

        result = client.tags.list(conversation_id=7)

        assert len(result.tags) == 1
        assert result.tags[0].name == "urgent"
