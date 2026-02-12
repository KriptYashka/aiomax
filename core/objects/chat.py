from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from core.objects import Message


class ChatTypes(Enum):
    CHAT = "chat"
    DIALOG = "dialog"  # TODO: Надо проверить эмпирическим путём, что есть


class ChatStatus(Enum):
    """
    Attributes:
        ACTIVE: Бот является активным участником чата.
        REMOVED: Бот был удалён из чата.
        LEFT: Бот покинул чат.
        CLOSED: Чат был закрыт.
    """
    ACTIVE = "active"
    REMOVED = "removed"
    LEFT = "left"
    CLOSED = "closed"


class Image(BaseModel):
    url: str


class Chat(BaseModel):
    chat_id: int
    type: ChatTypes
    status: ChatStatus
    title: Optional[str] = None
    icon: Optional[Image] = None
    last_event_time: int
    participants_count: int
    owner_id: Optional[int] = None
    participants: Optional[list] = None
    is_public: bool
    link: Optional[str] = None
    description: Optional[str] = None
    dialog_with_user: Optional[dict] = None
    chat_message_id: Optional[str] = None
    pinned_message: Optional[Message] = None
