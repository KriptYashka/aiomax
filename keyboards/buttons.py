from abc import ABC
from enum import Enum


class ButtonType(Enum):
    """
    Возможные типы кнопки
    """

    UNKNOWN = "unknown"
    CALLBACK = "callback"
    LINK = "link"
    CONTACT = "request_contact"
    LOCATION = "request_geo_location"
    APP = "open_app"
    MESSAGE = "message"


class Button(ABC):
    """
    Кнопка в клавиатуре.
    Args:
        button_type: Тип кнопки.
        text: Видимый текст кнопки. Длина: [1, 128].
    Notes:
        Названия аттрибутов должны совпадать с API MAX кнопок.
    """

    def __init__(self, button_type: ButtonType, text: str) -> None:
        self.type = button_type
        self.text = text

    def to_dict(self):
        return vars(self)


class ButtonMessage(Button):
    """
    Отправляет текстовое сообщение в чат.
    Args:
        text: Видимый текст кнопки. Длина: [1, 128].
    Notes:
        Названия аттрибутов должны совпадать с API MAX кнопок.
    """
    def __init__(self, text: str):
        super().__init__(ButtonType.MESSAGE, text)


class ButtonCallback(Button):
    """
    Отправляет Callback-запрос боту.
    Args:
        text: Видимый текст кнопки. Длина: [1, 128].
        payload: Данные кнопки. Длина: [0, 1024].
    Notes:
        Названия аттрибутов должны совпадать с API MAX кнопок.
    """
    def __init__(self, text: str, payload: str):
        super().__init__(ButtonType.CALLBACK, text)
        self.payload = payload


class ButtonLink(Button):
    """
    Отправляет кнопку со ссылкой.
    Args:
        text: Видимый текст кнопки. Длина: [1, 128].
        url: ...
    Notes:
        Названия аттрибутов должны совпадать с API MAX кнопок.
    """
    def __init__(self, text: str, url: str):
        super().__init__(ButtonType.LINK, text)
        self.url = url


class ButtonLocation(Button):
    """
    Отправляет кнопку с запросом геолокации.
    Args:
        text: Видимый текст кнопки. Длина: [1, 128].
        quick: Флаг отправляет местоположение без запроса подтверждения пользователя
    Notes:
        Названия аттрибутов должны совпадать с API MAX кнопок.
    """
    def __init__(self, text: str, quick: bool = False):
        super().__init__(ButtonType.LOCATION, text)
        self.quick = quick


class ButtonContact(Button):
    """
    Отправляет кнопку с запросом контакта пользователя.
    Args:
        text: Видимый текст кнопки. Длина: [1, 128].

    """
    def __init__(self, text: str):
        super().__init__(ButtonType.CONTACT, text)


class ButtonOpenApp(Button):
    """
    Отправляет кнопку с открытием приложения.
    Args:
        text: Видимый текст кнопки. Длина: [1, 128].
        web_app: Публичное имя (username) бота или ссылка на него, чьё мини-приложение надо запустить.
        contact_id: ID бота, чьё мини-приложение надо запустить.
        payload: Параметр запуска, который будет передан в ``initData`` мини-приложения.
    Notes:
        Названия аттрибутов должны совпадать с API MAX кнопок.
    """
    def __init__(self, text: str, web_app: str = None, contact_id: int = None, payload: str = None):
        super().__init__(ButtonType.APP, text)
        if web_app:
            self.web_app = web_app
        if contact_id:
            self.contact_id = contact_id
        if payload:
            self.payload = payload
