from __future__ import annotations

from typing import Any, Dict, Callable, Optional

from elementary.messages.formats.block_kit import format_block_kit
from elementary.messages.message_body import MessageBody


class SlackFormatter:
    """Convert internal MessageBody objects into Slack Block Kit payloads."""

    @staticmethod
    def format_message(
        message_body: MessageBody,
        resolve_mention: Optional[Callable[[str], Optional[str]]] = None,
    ) -> Dict[str, Any]:
        formatted = format_block_kit(message_body, resolve_mention=resolve_mention)
        return {
            "blocks": formatted.blocks,
            "attachments": formatted.attachments,
        }
