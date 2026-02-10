import dataclasses
import json
import logging

from keyboards import ButtonType, Button


@dataclasses.dataclass
class KeyboardConfig:
    MAX_INLINE_LINES = 30
    MAX_INLINE_COLS = 7
    MAX_INLINE_COLS_OTHER = 3
    OTHER = [ButtonType.LINK, ButtonType.APP, ButtonType.LOCATION, ButtonType.CONTACT]

    @staticmethod
    def can_append_on_line(line: list[Button], new_button_type: ButtonType):
        common_condition = len(line) <= KeyboardConfig.MAX_INLINE_COLS
        other_condition = len(line) <= KeyboardConfig.MAX_INLINE_COLS_OTHER

        if not common_condition:
            return False
        if new_button_type in KeyboardConfig.OTHER or any(map(lambda b: b.type in KeyboardConfig.OTHER, line)):
            return other_condition
        return True


class Keyboard(object):
    """
    Класс для создания клавиатуры для бота (https://dev.max.ru/docs-api#%D0%9A%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D0%B0)
    """

    def __init__(self):
        self.inline = True  # На данный момент доступна только inline-клавиатура
        self.lines = [[]]

    def _json_lines(self):
        return [
            [btn.to_dict() for btn in line]
            for line in self.lines
        ]

    def get_keyboard(self):
        """
        Возвращает JSON клавиатуры без пустых строк и кнопок.
        """

        class ButtonEncoder(json.JSONEncoder):
            def default(self, obj):
                if issubclass(type(obj), Button):
                    return obj.__dict__
                elif isinstance(obj, ButtonType):
                    return obj.value
                return json.JSONEncoder.default(self, obj)

        keyboard = {
            "type": "inline_keyboard",
            "payload": {
                "buttons": self.lines,
            }
        }
        return json.dumps(keyboard, ensure_ascii=False, cls=ButtonEncoder)

    def _calc_and_get_line(self, new_button: Button):
        if not KeyboardConfig.can_append_on_line(line=self.lines[-1], new_button_type=new_button.type):
            self.add_line()
        return self.lines[-1]

    def add_line(self):
        """
        Создаёт новую линию, на которой можно размещать кнопки.
        """
        self.lines.append([])
        if len(self.lines) > KeyboardConfig.MAX_INLINE_LINES:
            logging.warning(f"Keyboard lines exceeds max lines limit. Max limit: {KeyboardConfig.MAX_INLINE_LINES}")

    def add_button(self, button: Button):
        """
        Вычисляет нужную линию и добавляет кнопку.
        """
        current_line = self._calc_and_get_line(button)
        current_line.append(button)
