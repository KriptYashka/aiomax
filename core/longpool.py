import asyncio
import logging
from http.client import HTTPException
from typing import Optional, Union

from api import MaxApi
from core.events.base import EventTypes as Types, Event
from core.events.message import EventMessageCreated, EventMessageCallback, EventMessageEdited, EventMessageRemoved


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
            api: MaxApi,
            limit: int = 100,
            timeout: int = 30,
            marker: Optional[int] = None,
            types: Union[list, str, None] = None,
    ):
        self._lgr = logging.getLogger(__name__)
        self.api = api
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

    async def run(self):
        self._lgr.info("Long poll started")
        while self.working:
            try:
                response = await self.get_events()
                print(response)
            except HTTPException as e:
                self._lgr.error(f"Long poll HTTP error: {e}")
            except asyncio.CancelledError:
                self._lgr.error("Cancelled by user")
                self.working = False
            except Exception as e:
                self._lgr.error(f"Long poll error: {e}")

