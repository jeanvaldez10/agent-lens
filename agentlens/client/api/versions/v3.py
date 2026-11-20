"""
V3 API client for the agentlens API.

This module provides the client for the V3 version of the agentlens API.
"""

from agentlens.client.api.base import BaseApiClient
from agentlens.client.api.types import AuthTokenResponse
from agentlens.client.http.http_client import HttpClient
from agentlens.logging import logger
from termcolor import colored


class V3Client(BaseApiClient):
    """Client for the agentlens V3 API"""

    def __init__(self, endpoint: str):
        """
        Initialize the V3 API client.

        Args:
            endpoint: The base URL for the API
        """
        # Set up with V3-specific auth endpoint
        super().__init__(endpoint)

    async def fetch_auth_token(self, api_key: str) -> AuthTokenResponse:
        """
        Asynchronously fetch authentication token.

        Args:
            api_key: The API key to authenticate with

        Returns:
            AuthTokenResponse containing token and project information, or None if failed
        """
        try:
            path = "/v3/auth/token"
            data = {"api_key": api_key}
            headers = self.prepare_headers()

            # Build full URL
            url = self._get_full_url(path)

            # Make async request
            response_data = await HttpClient.async_request(
                method="POST", url=url, data=data, headers=headers, timeout=30
            )

            token = response_data.get("token")
            if not token:
                logger.warning("Authentication failed: Perhaps an invalid API key?")
                return None

            # Check project premium status
            if response_data.get("project_prem_status") != "pro":
                logger.info(
                    colored(
                        "\x1b[34mYou're on the agentlens free plan 🤔\x1b[0m",
                        "blue",
                    )
                )

            return response_data

        except Exception:
            return None

    # Add V3-specific API methods here
