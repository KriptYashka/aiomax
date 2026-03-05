from __future__ import annotations

from typing import Any, Final, Generator, Optional

import core.events as types_event
from core.handlers.observer import EventObserver
from core.handlers.responce import ResponseStatus

INTERNAL_UPDATE_TYPES: Final[frozenset[str]] = frozenset({"update", "error"})


class Router:
    """
    Маршрутизатор может перенаправлять обновления, и в него встроены такие типы обновлений, как сообщения, запросы обратного вызова,
опросы и все другие типы событий.

    Обработчики событий могут быть зарегистрированы в observer двумя способами:

    - Метод - :obj:`router.<event_type>.register(handler, <filters, ...>)`
    - Декторатор - :obj:`@router.<event_type>(<filters, ...>)`
    """

    def __init__(self, *, name: Optional[str] = None) -> None:
        """
        :param name: Optional router name, can be useful for debugging
        """

        self.name = name or hex(id(self))

        self._parent_router: Optional[Router] = None
        self.sub_routers: list[Router] = []

        # Observers
        self.message = EventObserver()
        self.edit_message = EventObserver()
        self.delete_message = EventObserver()
        self.callback_query = EventObserver()

        self.bot_added = EventObserver()
        self.bot_removed = EventObserver()
        self.bot_started = EventObserver()
        self.bot_stopped = EventObserver()

        self.dialog_muted = EventObserver()
        self.dialog_unmuted = EventObserver()
        self.dialog_cleared = EventObserver()
        self.dialog_removed = EventObserver()

        self.chat_title_changed = EventObserver()

        self.user_added = EventObserver()
        self.user_removed = EventObserver()

        self.startup = EventObserver()
        self.shutdown = EventObserver()

        self.observers: dict[type[types_event.Event], EventObserver] = {
            types_event.EventMessageCreated: self.message,
            types_event.EventMessageEdited: self.edit_message,
            types_event.EventMessageRemoved: self.delete_message,
            types_event.EventMessageCallback: self.callback_query,

            types_event.EventBotAdded: self.bot_added,
            types_event.EventBotRemoved: self.bot_removed,
            types_event.EventBotStarted: self.bot_started,
            types_event.EventBotStopped: self.bot_stopped,

            types_event.EventDialogMuted: self.dialog_muted,
            types_event.EventDialogUnmuted: self.dialog_unmuted,
            types_event.EventDialogCleared: self.dialog_cleared,
            types_event.EventDialogRemoved: self.dialog_removed,

            types_event.EventChatTitleChanged: self.chat_title_changed,

            types_event.EventUserAdded: self.user_added,
            types_event.EventUserRemoved: self.user_removed,
        }

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name!r}"

    def __repr__(self) -> str:
        return f"<{self}>"

    def resolve_used_update_types(self, skip_events: Optional[set[str]] = None) -> list[type[types_event.Event]]:
        """
        Разрешить имена зарегистрированных событий

        Полезно для получения обновлений только для зарегистрированных типов событий.

        :param skip_events: Имена для пропуска
        :return: Множество зарегистрированных имен
        """
        handlers_in_use: set[type[types_event.Event]] = set()
        if skip_events is None:
            skip_events = set()
        skip_events = {*skip_events, *INTERNAL_UPDATE_TYPES}

        for router in self.chain_tail:
            for update_class, observer in router.observers.items():
                if observer.handlers and update_class not in skip_events:
                    handlers_in_use.add(update_class)

        return list(handlers_in_use)

    async def propagate_event(self, event: types_event.Event, **kwargs: Any) -> Any:
        kwargs.update(event_router=self)
        observer = self.observers.get(event.__class__)

        async def _wrapped(event: types_event.Event, **data: Any) -> Any:
            return await self._propagate_event(
                observer=observer, event=event, **data
            )

        return await _wrapped(event, **kwargs)

    async def _propagate_event(
            self,
            observer: Optional[EventObserver],
            event: types_event.Event,
            **kwargs: Any,
    ) -> Any:
        response = ResponseStatus.UNHANDLED
        if observer:
            # Проверьте глобально определенные фильтры, прежде чем будет проверен любой другой обработчик.
            # Этот флажок установлен здесь вместо метода `trigger`, чтобы добавить возможность
            # передавать контекст обработчикам из глобальных фильтров.
            result, data = await observer.check_root_filters(event, **kwargs)
            if not result:
                return ResponseStatus.UNHANDLED
            kwargs.update(data)

            response = await observer.trigger(event, **kwargs)
            if response is ResponseStatus.REJECTED:  # pragma: no cover
                # Возможно только в том случае, если какой-либо обработчик возвращает ОТКЛОНЕННЫЙ результат
                return ResponseStatus.UNHANDLED
            if response is not ResponseStatus.UNHANDLED:
                return response

        for router in self.sub_routers:
            response = await router.propagate_event(event=event, **kwargs)
            if response is not ResponseStatus.UNHANDLED:
                break

        return response

    @property
    def chain_head(self) -> Generator[Router, None, None]:
        router: Optional[Router] = self
        while router:
            yield router
            router = router.parent_router

    @property
    def chain_tail(self) -> Generator[Router, None, None]:
        yield self
        for router in self.sub_routers:
            yield from router.chain_tail

    @property
    def parent_router(self) -> Optional[Router]:
        return self._parent_router

    @parent_router.setter
    def parent_router(self, router: Router) -> None:
        """
        Внутренний установщик свойств родительского маршрутизатора для этого маршрутизатора.
        Не используйте этот метод в собственном коде.
        Все маршрутизаторы должны быть включены с помощью метода `include_router`.

        Здесь не разрешены самостоятельные и циклические ссылки

        :param router: Роутер
        """
        if not isinstance(router, Router):
            raise ValueError(f"router should be instance of Router not {type(router).__name__!r}")
        if self._parent_router:
            raise RuntimeError(f"Router is already attached to {self._parent_router!r}")
        if self == router:
            raise RuntimeError("Self-referencing routers is not allowed")

        parent: Optional[Router] = router
        while parent is not None:
            if parent == self:
                raise RuntimeError("Circular referencing of Router is not allowed")

            parent = parent.parent_router

        self._parent_router = router
        router.sub_routers.append(self)

    def include_router(self, router: Router) -> Router:
        """
        Подключить другой маршрутизатор.

        :param router:
        :return:
        """
        if not isinstance(router, Router):
            raise ValueError(
                f"router should be instance of Router not {type(router).__class__.__name__}"
            )
        router.parent_router = self
        return router

    def include_routers(self, *routers: Router) -> None:
        """
        Подключить список маршрутизаторов.

        :param routers:
        :return:
        """
        if not routers:
            raise ValueError("At least one router must be provided")
        for router in routers:
            self.include_router(router)

    async def emit_startup(self, *args: Any, **kwargs: Any) -> None:
        """
        Рекурсивный вызов обратных вызовов запуска

        :param args:
        :param kwargs:
        :return:
        """
        kwargs.update(router=self)
        await self.startup.trigger(*args, **kwargs)
        for router in self.sub_routers:
            await router.emit_startup(*args, **kwargs)

    async def emit_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """
        Рекурсивный вызов обратных вызовов shutdown для плавного завершения работы

        :param args:
        :param kwargs:
        :return:
        """
        kwargs.update(router=self)
        await self.shutdown.trigger(*args, **kwargs)
        for router in self.sub_routers:
            await router.emit_shutdown(*args, **kwargs)
