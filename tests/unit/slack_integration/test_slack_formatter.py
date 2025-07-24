from elementary.messages.blocks import LineBlock, LinesBlock, TextBlock, MentionBlock
from elementary.messages.message_body import MessageBody

from elementary.slack_integration.formatter.slack_formatter import SlackFormatter


def test_format_message():
    body = MessageBody(blocks=[LinesBlock(lines=[LineBlock(inlines=[TextBlock(text="hi")])])])
    formatted = SlackFormatter.format_message(body)
    assert "blocks" in formatted
    assert isinstance(formatted["blocks"], list)


def test_format_message_resolve_mention():
    body = MessageBody(blocks=[LinesBlock(lines=[LineBlock(inlines=[MentionBlock(user="user")])])])
    formatted = SlackFormatter.format_message(body, resolve_mention=lambda u: "ID" )
    assert formatted["blocks"][0]["text"]["text"] == "<@ID>"
