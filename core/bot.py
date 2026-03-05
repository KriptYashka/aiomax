from pydantic import BaseModel

from core.api import MaxApi
from core.objects.message import Attachment


class Bot:
    def __init__(
            self,
            token: str,
            *,
            proxy: str = None,
    ):
        self.api = MaxApi(token, proxy)

    async def send(
            self,
            text: str,
            attachments: list[Attachment] = None,
            *,
            user_id: int = None,
            chat_id: int = None,
            disable_link_preview: bool = False,
    ):
        if user_id and chat_id:
            user_id = None
        attachments = attachments or []
        params = {
            "user_id": user_id,
            "chat_id": chat_id,
            "disable_link_preview": str(disable_link_preview),
        }
        body = {
            "text": text,
            "attachments": [item.model_dump() if isinstance(item, BaseModel) else item for item in attachments],
            "link": None,
            "format": "markdown",
        }
        await self.api.post("messages", params, body)
