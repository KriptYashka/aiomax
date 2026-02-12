from core.events.base import Event
from core.objects import User


class EventChatTitleChanged(Event):
    chat_id: int
    user: User
    title: str
