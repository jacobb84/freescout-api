"""Pytest configuration and fixtures for freescout-api tests."""

import pytest
import responses

from freescout import FreeScoutClient


@pytest.fixture
def base_url() -> str:
    """Return the base URL for tests."""
    return "https://support.example.com"


@pytest.fixture
def api_key() -> str:
    """Return the API key for tests."""
    return "test-api-key-12345"


@pytest.fixture
def client(base_url: str, api_key: str) -> FreeScoutClient:
    """Create a FreeScoutClient instance for testing."""
    return FreeScoutClient(base_url=base_url, api_key=api_key, max_retries=0)


@pytest.fixture
def mocked_responses():
    """Activate responses mock for HTTP requests."""
    with responses.RequestsMock() as rsps:
        yield rsps
