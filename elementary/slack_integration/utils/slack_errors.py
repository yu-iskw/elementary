class SlackError(Exception):
    """Base class for Slack related errors."""


class SlackRateLimitError(SlackError):
    pass


class SlackAuthError(SlackError):
    pass
