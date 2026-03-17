"""Tests for the Users resource."""

import responses

from freescout import FreeScoutClient


class TestUsersList:
    """Tests for listing users."""

    @responses.activate
    def test_list_users(self, client: FreeScoutClient, base_url: str) -> None:
        """Test listing users."""
        responses.add(
            responses.GET,
            f"{base_url}/api/users",
            json={
                "_embedded": {
                    "users": [
                        {
                            "id": 1,
                            "firstName": "John",
                            "lastName": "Doe",
                            "email": "johndoe@example.org",
                            "role": "admin",
                            "timezone": "Etc/GMT-3",
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

        result = client.users.list()

        assert len(result.users) == 1
        assert result.users[0].id == 1
        assert result.users[0].first_name == "John"
        assert result.users[0].email == "johndoe@example.org"

    @responses.activate
    def test_list_users_with_email_filter(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test listing users with email filter."""
        responses.add(
            responses.GET,
            f"{base_url}/api/users",
            json={
                "_embedded": {"users": []},
                "page": {
                    "size": 50,
                    "totalElements": 0,
                    "totalPages": 0,
                    "number": 1,
                },
            },
            status=200,
        )

        result = client.users.list(email="nonexistent@example.org")

        assert len(result.users) == 0


class TestUsersGet:
    """Tests for getting a single user."""

    @responses.activate
    def test_get_user(self, client: FreeScoutClient, base_url: str) -> None:
        """Test getting a single user."""
        responses.add(
            responses.GET,
            f"{base_url}/api/users/1",
            json={
                "id": 1,
                "firstName": "John",
                "lastName": "Doe",
                "email": "johndoe@example.org",
                "role": "admin",
                "jobTitle": "Support Agent",
                "phone": "+1867342345",
                "timezone": "Etc/GMT-3",
                "language": "en",
            },
            status=200,
        )

        user = client.users.get(1)

        assert user.id == 1
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.role == "admin"


class TestUsersCreate:
    """Tests for creating users."""

    @responses.activate
    def test_create_user(self, client: FreeScoutClient, base_url: str) -> None:
        """Test creating a user."""
        responses.add(
            responses.POST,
            f"{base_url}/api/users",
            headers={"Resource-ID": "17"},
            status=201,
        )

        user_id = client.users.create(
            first_name="Jane",
            last_name="Smith",
            email="janesmith@example.org",
            password="securepassword123",
            job_title="Support Agent",
            timezone="Europe/Paris",
        )

        assert user_id == 17


class TestUsersDelete:
    """Tests for deleting users."""

    @responses.activate
    def test_delete_user(self, client: FreeScoutClient, base_url: str) -> None:
        """Test deleting a user."""
        responses.add(
            responses.DELETE,
            f"{base_url}/api/users/17",
            status=204,
        )

        client.users.delete(17)

        assert len(responses.calls) == 1
