import asyncio
from typing import Optional, Union

from aiohttp.web_exceptions import HTTPException

from core.api import MaxApi
from core.bot import Bot
from core.events.base import EventTypes as Types, Event
from core.events.message import EventMessageCreated, EventMessageCallback, EventMessageEdited, EventMessageRemoved
from core.exceptions.common import HTTPExceptionController
from core.handlers.router import Router
from logs.logger import Logger


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

    CLASS_BY_EVENT_TYPE = {
        Types.MESSAGE_CREATED.value: EventMessageCreated,
        Types.MESSAGE_CALLBACK.value: EventMessageCallback,
        Types.MESSAGE_EDITED.value: EventMessageEdited,
        Types.MESSAGE_REMOVED.value: EventMessageRemoved,
    }

    DEFAULT_EVENT_CLASS = Event

    def __init__(
            self,
            bot: Bot,
            limit: int = 100,
            timeout: int = 30,
            marker: Optional[int] = None,
            types: Union[list, str, None] = None,
    ):
        self._lgr = Logger.logger.getChild('longpoll')
        self.api: MaxApi = bot.api
        self.bot = bot
        self.params = {
            'limit': limit,
            'timeout': timeout,
            'marker': marker,
            'types': ",".join(types) if isinstance(types, list) else types,
        }

        self.url = None
        self.working = True

    def _parse_event(self, raw_event: dict) -> Optional[Event]:
        event_pydantic_class = self.CLASS_BY_EVENT_TYPE.get(
            raw_event['update_type'],
            self.DEFAULT_EVENT_CLASS
        )
        return event_pydantic_class.model_validate(raw_event)

    async def get_events(self):
        response = await self.api.get("updates", self.params)
        events = []
        for update in response['updates']:
            events.append(self._parse_event(update))
        return events

    async def run(self, dispatcher: Router):
        self._lgr.info("Longpoll started")
        while self.working:
            try:
                events = await self.get_events()
                for event in events:
                    await dispatcher.propagate_event(event, bot=self.bot)
            except HTTPException as e:
                self.handle_http_exception(e)
            except asyncio.CancelledError:
                self._lgr.info("Cancelled by user")
                self.working = False
            except Exception as e:
                self._lgr.exception(f"Unhandled longpoll error: {e}")
        await self.api.close()
        self._lgr.info("Longpoll stopped")

    def handle_http_exception(self, exception: HTTPException):
        if HTTPExceptionController.need_stop_polling(exception):
            self.working = False
        HTTPExceptionController.log(self._lgr, exception)
