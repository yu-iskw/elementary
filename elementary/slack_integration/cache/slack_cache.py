from __future__ import annotations

import time
from typing import Callable, Dict, Iterable, Optional


class SlackCache:
    """Simple time-based cache for Slack lookups."""

    def __init__(self, ttl_seconds: int = 3600) -> None:
        self.ttl_seconds = ttl_seconds
        self._user_id_cache: Dict[str, tuple[str, float]] = {}
        self._groups_cache: Optional[tuple[Iterable[dict], float]] = None

    def get_user_id(self, email: str, fetch_func: Callable[[str], Optional[str]]) -> Optional[str]:
        cached = self._user_id_cache.get(email)
        now = time.time()
        if cached and now - cached[1] < self.ttl_seconds:
            return cached[0]
        user_id = fetch_func(email)
        if user_id:
            self._user_id_cache[email] = (user_id, now)
        return user_id

    def get_usergroups(self, fetch_func: Callable[[], Iterable[dict]]) -> Iterable[dict]:
        now = time.time()
        if self._groups_cache and now - self._groups_cache[1] < self.ttl_seconds:
            return self._groups_cache[0]
        groups = list(fetch_func())
        self._groups_cache = (groups, now)
        return groups
