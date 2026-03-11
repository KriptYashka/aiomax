from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Recipient(BaseModel):
    chat_id: int


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: bool
    last_activity_time: int


class UserWithPhoto(User):
    avatar_url: str = None
    full_avatar_url: str = None


class ChatAdminPermission(str, Enum):
    READ_ALL = "read_all_messages"
    ADD_REMOVE_MEMBERS = "add_remove_members"
    ADD_ADMINS = "add_admins"
    CHANGE_CHAT_INFO = "change_chat_info"
    PIN_MESSAGE = "pin_message"
    WRITE = "write"
    EDIT_LINK = "edit_link"


class ChatMember(UserWithPhoto):
    last_access_time: int = None
    is_owner: bool
    is_admin: bool
    join_time: int
    permission: list[ChatAdminPermission] = None
    alias: str = None
