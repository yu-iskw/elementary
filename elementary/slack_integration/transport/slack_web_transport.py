from __future__ import annotations

from typing import Iterable, Optional, Any

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .slack_transport import SlackTransport
from ..utils.slack_errors import SlackError
from ..utils.slack_rate_limiter import rate_limited_slack_call


class SlackWebTransport(SlackTransport):
    """Transport implementation using Slack's Web API."""

    def __init__(self, token: str) -> None:
        self.client = WebClient(token=token)

    @rate_limited_slack_call
    def send_message(self, channel: str, blocks: list, attachments: Optional[list] = None) -> Any:
        return self.client.chat_postMessage(
            channel=channel,
            blocks=blocks,
            attachments=attachments,
        )

    @rate_limited_slack_call
    def send_file(self, channel: str, file_path: str, comment: str = "") -> Any:
        return self.client.files_upload_v2(
            channel=channel,
            file=file_path,
            initial_comment=comment or None,
            request_file_info=False,
        )

    @rate_limited_slack_call
    def lookup_user_id(self, email: str) -> Optional[str]:
        try:
            resp = self.client.users_lookupByEmail(email=email)
            return resp["user"]["id"]
        except SlackApiError as exc:
            if exc.response.get("error") == "users_not_found":
                return None
            raise SlackError(str(exc))

    @rate_limited_slack_call
    def list_channels(self) -> Iterable[dict]:
        resp = self.client.conversations_list(
            types="public_channel,private_channel",
            exclude_archived=True,
            limit=1000,
        )
        return resp["channels"]

    @rate_limited_slack_call
    def list_usergroups(self) -> Iterable[dict]:
        resp = self.client.usergroups_list()
        return resp.get("usergroups", [])
