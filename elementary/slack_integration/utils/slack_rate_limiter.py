from __future__ import annotations

from ratelimit import limits, sleep_and_retry


def rate_limited_slack_call(func):
    """Decorator to apply Slack rate limiting to API calls."""

    @sleep_and_retry
    @limits(calls=50, period=60)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
