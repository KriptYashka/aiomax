from typing import Optional

from core.events.base import EventBot


class EventBotAdded(EventBot):
    is_channel: bool


class EventBotRemoved(EventBot):
    is_channel: bool


class EventBotStarted(EventBot):
    payload: Optional[str] = None


class EventBotStopped(EventBot):
    pass
