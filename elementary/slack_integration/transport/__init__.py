"""Convenience utilities for working with Slack transports."""

from .slack_transport import SlackTransport
from .slack_web_transport import SlackWebTransport
from .slack_webhook_transport import SlackWebhookTransport


def create_transport(
    token: str | None = None,
    webhook: str | None = None,
) -> SlackTransport | None:
    """Instantiate a :class:`SlackTransport` for the provided credentials."""
    if token:
        return SlackWebTransport(token=token)
    if webhook:
        return SlackWebhookTransport(url=webhook)
    return None
