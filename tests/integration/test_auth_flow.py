import asyncio

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agentlens.client import Client
from agentlens.exceptions import ApiServerException


@pytest.fixture(autouse=True)
def reset_client():
    """Reset the client singleton between tests"""
    # Reset the singleton instance
    Client._Client__instance = None
    yield
    # Clean up after test
    Client._Client__instance = None


@pytest.mark.vcr()
def test_auth_flow(mock_api_key):
    """Test the authentication flow using the agentlens client."""
    with patch("agentlens.client.client.ApiClient") as mock_api_client:
        # Create mock API instance
        mock_api = MagicMock()
        mock_api.v3.fetch_auth_token = AsyncMock(return_value={"token": "mock_token", "project_id": "mock_project_id"})
        mock_api_client.return_value = mock_api

        # Initialize the client
        client = Client()
        session = client.init(api_key=mock_api_key)

        # Verify client is initialized
        assert client.initialized
        assert client.api is not None

        # Verify session is created if auto_start_session is True
        if client.config.auto_start_session:
            assert session is not None


@pytest.mark.vcr()
def test_auth_flow_invalid_key():
    """An invalid API key must not break init(), but the auth failure must be reported.

    Authentication runs in a background task so that init() never blocks the host program;
    the failure is surfaced as a warning and the client stays unauthenticated.
    """
    with (
        patch("agentlens.client.client.ApiClient") as mock_api_client,
        patch("agentlens.client.client.logger") as mock_logger,
    ):
        mock_api = MagicMock()
        mock_api.v3.fetch_auth_token = AsyncMock(side_effect=ApiServerException("Invalid API key"))
        mock_api_client.return_value = mock_api

        client = Client()
        client.init(api_key="invalid-key")  # must not raise

        # Run the auth step deterministically instead of racing the background thread
        result = asyncio.run(client._fetch_auth_async("invalid-key"))

        assert result is None
        assert client.get_current_jwt() is None
        warnings = " ".join(str(call.args[0]) for call in mock_logger.warning.call_args_list)
        assert "Invalid API key" in warnings
