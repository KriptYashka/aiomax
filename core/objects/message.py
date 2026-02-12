from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from core.objects import User, Recipient


class AttachmentTypes(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"
    STICKER = "sticker"
    CONTACT = "contact"
    INLINE_KEYBOARD = "inline_keyboard"
    SHARE = "share"
    LOCATION = "location"


class Attachment(BaseModel):
    type: AttachmentTypes
    payload: Optional[dict] = None
    # Location - единственный тип, который так "выделяется"... Нет возможности объединить Attachment.
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class MessageBody(BaseModel):
    id: str = Field(alias="mid")
    id_in_chat: int = Field(alias="seq")
    text: Optional[str]
    attachments: Optional[list[Attachment]] = None
    markup: Optional[list] = None


class MessageStat(BaseModel):
    views: int = Field(default=0)


class LinkedMessageTypes(Enum):
    FORWARD = "forward"
    REPLY = "reply"


class LinkedMessage(BaseModel):
    type: LinkedMessageTypes
    sender: Optional[User] = None
    chat_id: Optional[int] = None
    message: MessageBody


class Message(BaseModel):
    sender: Optional[User] = None
    recipient: Recipient
    timestamp: int
    link: Optional[LinkedMessage] = None
    body: MessageBody
    stat: Optional[MessageStat] = None
    url: Optional[str] = None


class TextFormat(Enum):
    MARKDOWN = "markdown"
    HTML = "html"


class NewMessageLink(BaseModel):
    type: LinkedMessageTypes
    message_id: str = Field(alias="mid")


class NewMessageBody(BaseModel):
    text: Optional[str] = Field(None, max_length=4000)
    attachments: Optional[list[Attachment]] = None
    link: Optional[NewMessageLink] = None
    notify: bool = Field(default=True)
    format: Optional[TextFormat] = Field(default=None)
