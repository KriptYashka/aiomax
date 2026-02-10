import logging
from typing import Optional, Union

import aiohttp

from aiohttp.web_exceptions import HTTPError

from api import MaxApi


class MaxLongPoll(object):
    """
    Класс для работы с Bots Long Poll сервером
    Args:
        api: Объект API.
        limit: Максимальное количество обновлений для получения.
        timeout: Тайм-аут в секундах для долгого опроса.
        marker: Если передан, бот получит обновления, которые еще не были получены.
                Если не передан, получит все новые обновления.
        types: Список событий, запрашиваемых с опроса.
    """

    #: Классы для событий по типам
    # CLASS_BY_EVENT_TYPE = {
    #     VkBotEventType.MESSAGE_NEW.value: VkBotMessageEvent,
    #     VkBotEventType.MESSAGE_REPLY.value: VkBotMessageEvent,
    #     VkBotEventType.MESSAGE_EDIT.value: VkBotMessageEvent,
    #     VkBotEventType.MESSAGE_EVENT.value: VkBotCallbackEvent,
    # }
    #
    # #: Класс для событий
    # DEFAULT_EVENT_CLASS = VkBotEvent

    def __init__(
            self,
            api: MaxApi,
            limit: int = 100,
            timeout: int = 30,
            marker: Optional[int] = None,
            types: Union[list, str, None] = None,
    ):
        self.api = api
        self.params = {
            'limit': limit,
            'timeout': timeout,
            'marker': marker,
            'types': ",".join(types) if isinstance(types, list) else types,
        }

        self.url = None

    # def _parse_event(self, raw_event):
    #     event_class = self.CLASS_BY_EVENT_TYPE.get(
    #         raw_event['type'],
    #         self.DEFAULT_EVENT_CLASS
    #     )
    #     return event_class(raw_event)


    async def get_events(self):
        response = await self.api.get("updates", self.params)
        return response
