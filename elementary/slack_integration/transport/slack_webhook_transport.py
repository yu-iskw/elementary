from __future__ import annotations

from typing import Iterable, Optional, Any

from slack_sdk import WebhookClient

from .slack_transport import SlackTransport
from ..utils.slack_rate_limiter import rate_limited_slack_call


class SlackWebhookTransport(SlackTransport):
    """Transport using Slack incoming webhooks."""

    def __init__(self, url: str) -> None:
        self.client = WebhookClient(url)

    @rate_limited_slack_call
    def send_message(self, channel: str, blocks: list, attachments: Optional[list] = None) -> Any:
        # Webhooks do not support specifying the channel dynamically in the request.
        return self.client.send(blocks=blocks, attachments=attachments)

    def send_file(self, channel: str, file_path: str, comment: str = "") -> Any:
        raise NotImplementedError("Webhook transport cannot upload files")

    def lookup_user_id(self, email: str) -> Optional[str]:
        return None

    def list_channels(self) -> Iterable[dict]:
        return []

    def list_usergroups(self) -> Iterable[dict]:
        return []
