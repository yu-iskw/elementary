from unittest.mock import MagicMock

from elementary.messages.blocks import LineBlock, LinesBlock, TextBlock, MentionBlock
from elementary.messages.message_body import MessageBody
from elementary.slack_integration.slack_service import SlackService
from elementary.slack_integration.formatter.slack_formatter import SlackFormatter
from elementary.slack_integration.cache.slack_cache import SlackCache


class DummyTransport:
    def __init__(self):
        self.send_message = MagicMock(return_value={"ok": True})
        self.send_file = MagicMock()
        self.lookup_user_id = MagicMock(return_value="U123")
        self.list_channels = MagicMock(return_value=[]) 


def _body():
    return MessageBody(blocks=[LinesBlock(lines=[LineBlock(inlines=[TextBlock(text="hi")])])])


def _body_with_mention():
    return MessageBody(blocks=[LinesBlock(lines=[LineBlock(inlines=[MentionBlock(user="user@example.com")])])])


def test_send_alert_with_email():
    transport = DummyTransport()
    service = SlackService(transport, SlackFormatter(), SlackCache())
    service.send_alert("user@example.com", _body())
    transport.lookup_user_id.assert_called_once_with("user@example.com")
    transport.send_message.assert_called_once()


def test_send_alert_resolves_mentions():
    transport = DummyTransport()
    service = SlackService(transport, SlackFormatter(), SlackCache())
    service.send_alert("C1", _body_with_mention())
    transport.lookup_user_id.assert_called_once_with("user@example.com")
    transport.send_message.assert_called_once()
