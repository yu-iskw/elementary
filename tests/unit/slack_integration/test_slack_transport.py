from unittest.mock import MagicMock

import pytest

from elementary.slack_integration.transport.slack_web_transport import SlackWebTransport


@pytest.fixture
def mock_client(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("elementary.slack_integration.transport.slack_web_transport.WebClient", MagicMock(return_value=mock))
    return mock


def test_send_message(mock_client):
    transport = SlackWebTransport(token="x")
    transport.send_message("C", [1])
    mock_client.chat_postMessage.assert_called_once()


def test_list_usergroups(mock_client):
    mock_client.usergroups_list.return_value = {"usergroups": [{"id": "S1"}]}
    transport = SlackWebTransport(token="x")
    groups = list(transport.list_usergroups())
    assert groups == [{"id": "S1"}]
