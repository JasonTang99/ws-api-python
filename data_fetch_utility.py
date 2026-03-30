"""
data_fetch_utility.py

A read-only helper utility for fetching data from a REST API.
This module provides no capability to modify or push data; it is strictly
limited to HTTP GET requests.

Usage example::

    from data_fetch_utility import DataFetchUtility

    utility = DataFetchUtility(base_url="https://api.example.com", token="your_token")
    data = utility.fetch_data("accounts", params={"page": 1})
"""

import logging

import requests

logger = logging.getLogger(__name__)


class DataFetchUtility:
    """Utility class for fetching data from a REST API (read-only).

    This class wraps HTTP GET requests and handles common error scenarios,
    returning parsed JSON responses.  No write, update, or delete operations
    are exposed.

    Attributes:
        base_url (str): The base URL of the API (e.g. ``"https://api.example.com"``).
        headers (dict): HTTP headers sent with every request, including the
            ``Authorization: Bearer <token>`` header.
    """

    def __init__(self, base_url: str, token: str) -> None:
        """Initialise the utility with an API base URL and bearer token.

        Args:
            base_url (str): Base URL for the API, without a trailing slash.
            token (str): Bearer token used for API authorisation.
        """
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}

    def fetch_data(self, endpoint: str, params: dict = None) -> dict | None:
        """Fetch data from a given endpoint with optional query parameters.

        Sends an HTTP GET request to ``<base_url>/<endpoint>`` and returns the
        parsed JSON body.  If the server returns an HTTP error status (4xx/5xx)
        or a network-level error occurs, the exception is caught, an error
        message is printed, and ``None`` is returned.

        Args:
            endpoint (str): The API endpoint path, relative to ``base_url``
                (e.g. ``"accounts"`` or ``"accounts/123/positions"``).
            params (dict, optional): Query parameters to append to the request
                URL.  Defaults to ``None``.

        Returns:
            dict | None: Parsed JSON response body, or ``None`` on error.
        """
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
            return response.json()  # Assumes the API returns JSON
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching data: %s", e)
            return None
