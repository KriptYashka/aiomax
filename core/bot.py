from core.api import MaxApi


class Bot:
    def __init__(
            self,
            token: str,
            *,
            proxy: str = None,
    ):
        self.api = MaxApi(token, proxy)

    async def send(self, text: str, user_id: int = None, chat_id=None, disable_link_preview=False):
        if user_id and chat_id:
            user_id = None
        params = {
            "user_id": user_id,
            "chat_id": chat_id,
            "disable_link_preview": str(disable_link_preview),
        }
        body = {
            "text": text,
            "attachments": None,
            "link": None,
            "format": "markdown",
        }
        await self.api.post("messages", params, body)
