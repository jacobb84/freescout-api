"""Tests for exception handling."""

import responses

import pytest

from freescout import FreeScoutClient
from freescout.exceptions import (
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    ServerError,
    ValidationError,
)


class TestExceptionHandling:
    """Tests for API error handling."""

    @responses.activate
    def test_authentication_error(
        self, client: FreeScoutClient, base_url: str
    ) -> None:
        """Test 401 Unauthorized error."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations",
            json={"message": "Invalid API key"},
            status=401,
        )

        with pytest.raises(AuthenticationError) as exc_info:
            client.conversations.list()

        assert exc_info.value.status_code == 401
        assert "Invalid API key" in str(exc_info.value)

    @responses.activate
    def test_forbidden_error(self, client: FreeScoutClient, base_url: str) -> None:
        """Test 403 Forbidden error."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations/1",
            json={"message": "Access denied"},
            status=403,
        )

        with pytest.raises(ForbiddenError) as exc_info:
            client.conversations.get(1)

        assert exc_info.value.status_code == 403

    @responses.activate
    def test_not_found_error(self, client: FreeScoutClient, base_url: str) -> None:
        """Test 404 Not Found error."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations/999",
            json={"message": "Conversation not found"},
            status=404,
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.conversations.get(999)

        assert exc_info.value.status_code == 404

    @responses.activate
    def test_validation_error(self, client: FreeScoutClient, base_url: str) -> None:
        """Test 400 Bad Request error with validation details."""
        responses.add(
            responses.POST,
            f"{base_url}/api/conversations",
            json={
                "message": "Bad request",
                "errorCode": "BAD REQUEST",
                "_embedded": {
                    "errors": [
                        {
                            "path": "subject",
                            "message": "may not be empty",
                            "source": "JSON",
                        },
                        {
                            "path": "status",
                            "message": "Expected one of: 'active', 'pending', 'closed'",
                            "rejectedValue": "invalid",
                            "source": "JSON",
                        },
                    ]
                },
            },
            status=400,
        )

        with pytest.raises(ValidationError) as exc_info:
            client.conversations.create(
                mailbox_id=1,
                subject="",
                customer={"email": "test@example.com"},
                threads=[{"type": "customer", "text": "test"}],
            )

        assert exc_info.value.status_code == 400
        assert len(exc_info.value.errors) == 2
        assert exc_info.value.errors[0]["path"] == "subject"

    @responses.activate
    def test_server_error(self, client: FreeScoutClient, base_url: str) -> None:
        """Test 500 Internal Server Error."""
        responses.add(
            responses.GET,
            f"{base_url}/api/conversations",
            json={"message": "Internal server error"},
            status=500,
        )

        with pytest.raises(ServerError) as exc_info:
            client.conversations.list()

        assert exc_info.value.status_code == 500


class TestExceptionStringRepresentation:
    """Tests for exception string representation."""

    def test_exception_with_status_code(self) -> None:
        """Test exception string includes status code."""
        exc = NotFoundError("Resource not found", status_code=404)
        assert "[404]" in str(exc)
        assert "Resource not found" in str(exc)

    def test_exception_without_status_code(self) -> None:
        """Test exception string without status code."""
        exc = ValidationError("Invalid input")
        assert str(exc) == "Invalid input"
