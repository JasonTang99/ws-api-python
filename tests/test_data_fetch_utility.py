from unittest.mock import MagicMock, patch

import pytest
import requests

from data_fetch_utility import DataFetchUtility


@pytest.fixture
def utility():
    return DataFetchUtility(base_url="https://api.example.com", token="test_token")


def test_init_sets_base_url(utility):
    assert utility.base_url == "https://api.example.com"


def test_init_sets_auth_header(utility):
    assert utility.headers == {"Authorization": "Bearer test_token"}


@patch("requests.get")
def test_fetch_data_returns_json_on_success(mock_get, utility):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"id": 1, "name": "account"}
    mock_get.return_value = mock_resp

    result = utility.fetch_data("accounts")

    assert result == {"id": 1, "name": "account"}
    mock_get.assert_called_once_with(
        "https://api.example.com/accounts",
        headers={"Authorization": "Bearer test_token"},
        params=None,
    )


@patch("requests.get")
def test_fetch_data_passes_query_params(mock_get, utility):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"id": 2}]
    mock_get.return_value = mock_resp

    params = {"page": 1, "limit": 10}
    result = utility.fetch_data("accounts", params=params)

    assert result == [{"id": 2}]
    mock_get.assert_called_once_with(
        "https://api.example.com/accounts",
        headers={"Authorization": "Bearer test_token"},
        params=params,
    )


@patch("requests.get")
def test_fetch_data_returns_none_on_http_error(mock_get, utility, caplog):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_resp

    with caplog.at_level("ERROR"):
        result = utility.fetch_data("nonexistent")

    assert result is None
    assert "Error fetching data" in caplog.text


@patch("requests.get")
def test_fetch_data_returns_none_on_connection_error(mock_get, utility, caplog):
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

    with caplog.at_level("ERROR"):
        result = utility.fetch_data("accounts")

    assert result is None
    assert "Error fetching data" in caplog.text


def test_fetch_data_does_not_expose_write_methods(utility):
    """Ensure no write/mutating methods are present on the utility."""
    for method_name in ("post", "put", "patch", "delete", "push", "send"):
        assert not hasattr(utility, method_name), (
            f"DataFetchUtility must not expose '{method_name}'"
        )
