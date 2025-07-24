from __future__ import annotations

import re
from typing import Optional

from elementary.messages.message_body import MessageBody

from .transport.slack_transport import SlackTransport
from .formatter.slack_formatter import SlackFormatter
from .cache.slack_cache import SlackCache
from .utils.slack_errors import SlackError


class SlackService:
    """High level API for sending alerts and files to Slack."""

    def __init__(self, transport: SlackTransport, formatter: SlackFormatter | None = None, cache: SlackCache | None = None) -> None:
        self.transport = transport
        self.formatter = formatter or SlackFormatter()
        self.cache = cache or SlackCache()

        self._email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    def _resolve_mention(self, user: str) -> Optional[str]:
        if user.startswith("<@") or user.startswith("<!"):
            return None
        if self._email_regex.fullmatch(user):
            return self.cache.get_user_id(user, self.transport.lookup_user_id)
        handle = user.lstrip("@")
        for group in self.cache.get_usergroups(self.transport.list_usergroups):
            if group.get("handle") == handle:
                return f"!subteam^{group['id']}"
        return None

    def send_alert(self, email_or_channel: str, message_body: MessageBody):
        destination = email_or_channel
        if "@" in email_or_channel:
            user_id = self.cache.get_user_id(email_or_channel, self.transport.lookup_user_id)
            if not user_id:
                raise SlackError(f"User not found for email {email_or_channel}")
            destination = user_id
        payload = self.formatter.format_message(message_body, resolve_mention=self._resolve_mention)
        return self.transport.send_message(destination, payload["blocks"], payload.get("attachments"))

    def upload_report(self, channel: str, file_path: str, comment: str = ""):
        return self.transport.send_file(channel, file_path, comment)
