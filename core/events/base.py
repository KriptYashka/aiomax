from abc import ABC
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from core.objects import User


class EventTypes(Enum):
    MESSAGE_CREATED = "message_created"
    MESSAGE_CALLBACK = "message_callback"
    MESSAGE_EDITED = "message_edited"
    MESSAGE_REMOVED = "message_removed"

    BOT_ADDED = "bot_added"
    BOT_REMOVED = "bot_removed"
    BOT_STARTED = "bot_started"
    BOT_STOPPED = "bot_stopped"

    DIALOG_MUTED = "dialog_muted"
    DIALOG_UNMUTED = "dialog_unmuted"
    DIALOG_REMOVED = "dialog_removed"
    DIALOG_CLEARED = "dialog_cleared"

    USER_ADDED = "user_added"
    USER_REMOVED = "user_removed"

    CHAT_TITLE_CHANGED = "chat_title_changed"


class Event(BaseModel):
    update_type: EventTypes
    timestamp: int
    user_locale: Optional[str] = None


class EventBot(Event):
    chat_id: int
    user: User


class EventDialog(Event):
    chat_id: int
    user: User


class EventUser(Event):
    chat_id: int
    user: User
    is_channel: bool
