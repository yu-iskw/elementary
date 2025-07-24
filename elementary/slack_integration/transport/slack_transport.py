from abc import ABC, abstractmethod
from typing import Optional, Iterable, Any


class SlackTransport(ABC):
    """Abstract interface for Slack transports."""

    @abstractmethod
    def send_message(self, channel: str, blocks: list, attachments: Optional[list] = None) -> Any:
        """Send a message represented by blocks to a channel or user."""
        raise NotImplementedError

    @abstractmethod
    def send_file(self, channel: str, file_path: str, comment: str = "") -> Any:
        """Upload a file to the given channel."""
        raise NotImplementedError

    @abstractmethod
    def lookup_user_id(self, email: str) -> Optional[str]:
        """Resolve a user ID from an email address."""
        raise NotImplementedError

    @abstractmethod
    def list_channels(self) -> Iterable[dict]:
        """List channels visible to the integration."""
        raise NotImplementedError

    @abstractmethod
    def list_usergroups(self) -> Iterable[dict]:
        """List Slack user groups available to the integration."""
        raise NotImplementedError
