from pydantic import BaseModel, Field

from core.objects import UserWithPhoto


class BotCommand(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1, max_length=128)

class BotInfo(UserWithPhoto):
    commands: list[BotCommand] = None