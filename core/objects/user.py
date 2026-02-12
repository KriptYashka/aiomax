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
