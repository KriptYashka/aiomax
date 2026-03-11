from typing import Union

from pydantic import BaseModel, ValidationError

from core.api import MaxApi
from core.objects.bot import BotInfo
from core.objects.media import Video
from core.objects.message import NewMessageBody, Message
from logs.logger import Logger


class Bot:
    def __init__(
            self,
            token: str,
            *,
            proxy: str = None,
    ):
        self.api = MaxApi(token, proxy)
        self.lgr = Logger.logger

    def validate_and_parse(self, items: Union[dict, list], model: type[BaseModel]):
        instances = []
        if one_instance := isinstance(items, dict):
            items = [items]
        try:
            for item in items:
                instances.append(model(**item))
        except ValidationError as e:
            self.lgr.error("Validation error: {}".format(e))
            return None if one_instance else []
        except Exception as e:
            self.lgr.error("Unknown error: {}".format(e))
            return None if one_instance else []
        return instances[0] if one_instance else instances

    def check_success(self, response: dict):
        if not (success := bool(response["success"])):
            message = response["message"]
            self.lgr.error("Failed to edit message: {}".format(message))
        return success

    # API: Bots

    # API: Chats

    # API: Messages

    async def get_me(self):
        response = await self.api.get("me")
        return self.validate_and_parse(response, BotInfo)

    async def get_messages(
            self,
            chat_id: int = None,
            messages_ids: str = None,
            from_time: int = None,
            to_time: int = None,
            count: int = None,
    ):
        params = {
            "chat_id": chat_id,
            "messages_ids": messages_ids,
            "from": from_time,
            "to": to_time,
            "count": count,
        }
        response = await self.api.get("messages", params)
        messages = self.validate_and_parse(response["messages"], Message)
        return messages

    async def get_message(
            self,
            message_id: int,
    ):
        response = await self.api.get("messages/{}".format(message_id))
        return self.validate_and_parse(response, Message)

    async def send(
            self,
            model_or_text: Union[NewMessageBody, str],
            *,
            user_id: int = None,
            chat_id: int = None,
            disable_link_preview: bool = False,
    ):
        if user_id and chat_id:
            user_id = None
        params = {
            "user_id": user_id,
            "chat_id": chat_id,
            "disable_link_preview": str(disable_link_preview)
        }
        message = NewMessageBody(text=model_or_text) if isinstance(model_or_text, str) else model_or_text

        await self.api.post("messages", params, message.model_dump())

    async def edit_message(
            self,
            message_id: str,
            model_or_text: Union[NewMessageBody, str],
    ):
        params = {
            "message_id": message_id,
        }
        message = NewMessageBody(text=model_or_text) if isinstance(model_or_text, str) else model_or_text
        response = await self.api.put("messages", params, message.model_dump())
        success = self.check_success(response)
        return success

    async def delete_message(
            self,
            message_id: str,
    ):
        params = {
            "message_id": message_id,
        }
        response = await self.api.delete("messages", params)
        success = self.check_success(response)
        return success

    async def answer_callback(
            self,
            callback_id: str,
            message_to_edit: NewMessageBody = None,
            notification: str = None,
    ):
        if not (message_to_edit or notification):
            raise AttributeError("You must specify either `message_to_edit` or `notification`")
        params = {
            "callback_id": callback_id,
        }
        body = dict()
        if message_to_edit:
            body["message"] = message_to_edit.model_dump()
        if notification:
            body["notification"] = notification
        response = await self.api.post("answers", params, body)
        return self.check_success(response)

    async def get_videos(
            self,
            video_token: str,
    ):
        params = {
            "videoToken": video_token,
        }
        response = await self.api.get("messages", params)
        return self.validate_and_parse(response, Video)
