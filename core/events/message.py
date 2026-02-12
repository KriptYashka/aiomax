from typing import Optional

from core.events.base import Event
from core.objects import Message, Callback


class EventMessageCreated(Event):
    message: Message


class EventMessageCallback(Event):
    callback: Callback
    message: Optional[Message] = None


class EventMessageEdited(Event):
    message: Message


class EventMessageRemoved(Event):
    message_id: str
    chat_id: int
    user_id: int
