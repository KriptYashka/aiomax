import datetime
from collections import defaultdict, deque

from magic_filter import F

from core.bot import Bot
from core.events import (
    EventMessageCreated,
    EventMessageEdited,
    EventMessageRemoved,
    EventMessageCallback,
)
from core.handlers.router import Router
from core.keyboards import Keyboard, ButtonCallback
from core.objects.message import NewMessageBody

router = Router()

LAST_MESSAGES = defaultdict(lambda: deque(maxlen=2))


def main_menu_keyboard() -> Keyboard:
    kb = Keyboard()
    kb.add_button(ButtonCallback("Создать", "created_info"))
    kb.add_button(ButtonCallback("Изменить", "edited_info"))
    kb.add_button(ButtonCallback("Удалить", "removed_info"))
    kb.add_button(ButtonCallback("Ответ (answers)", "answer_notify"))
    return kb


@router.message()
async def on_message(event: EventMessageCreated, bot: Bot):
    """
    Сохраняем сообщение в историю чата и показываем меню с 4 callback-кнопками.
    """
    msg = event.message
    chat_id = msg.recipient.chat_id

    LAST_MESSAGES[chat_id].append(msg)

    text = (
        "Сообщение получено и сохранено в историю.\n"
        "Клавиатура ниже демонстрирует:\n"
        "- обработку создания/изменения/удаления\n"
        "- ответ на callback через /answers\n\n"
        "Команда: отправьте текст `/prev` чтобы получить предпоследнее сообщение."
    )

    new_message = NewMessageBody(
        text=text,
        attachments=[main_menu_keyboard().get_keyboard()],
    )
    await bot.send(
        new_message,
        user_id=msg.sender.user_id,
    )


@router.message(F.message.body.text == "/prev")
async def get_previous_message(event: EventMessageCreated, bot: Bot):
    """
    Команда: вернуть предпоследнее сообщение в этом чате.
    """
    msg = event.message
    chat_id = msg.recipient.chat_id

    history = LAST_MESSAGES.get(chat_id)
    if not history or len(history) < 2:
        await bot.send(
            "Недостаточно истории: в чате пока меньше двух сообщений.",
            user_id=msg.sender.user_id,
        )
        return

    prev_msg = history[0]
    text = prev_msg.body.text or "(без текста)"

    await bot.send(
        f"Предпоследнее сообщение в чате:\n{text}",
        user_id=msg.sender.user_id,
    )


@router.callback_query()
async def on_callback(event: EventMessageCallback, bot: Bot):
    """
    Демонстрация ответа на callback через /answers.
    """
    cb = event.callback
    payload = cb.payload

    if payload == "answer_notify":
        await bot.answer_callback(
            callback_id=cb.callback_id,
            notification="Это уведомление отправлено через /answers.",
        )
    else:
        mapping = {
            "created_info": "Пример обработки события создания сообщения.",
            "edited_info": "Пример обработки события изменения сообщения.",
            "removed_info": "Пример обработки события удаления сообщения.",
        }
        note = mapping.get(payload, "Неизвестное действие.")
        await bot.answer_callback(
            callback_id=cb.callback_id,
            notification=note,
        )

        if payload == "edited_info":
            new_message = NewMessageBody(
                text=f"Сообщение обновлено {datetime.datetime.now().strftime('%H:%M:%S')}",
            )
            await bot.edit_message(
                event.message.body.id,
                new_message,
            )

        if payload == "removed_info":
            await bot.delete_message(
                event.message.body.id,
            )


@router.edit_message()
async def on_edited(event: EventMessageEdited, bot: Bot):
    msg = event.message
    await bot.send(
        "Сообщение было изменено (event.message_edited).",
        chat_id=msg.recipient.chat_id,
    )


@router.delete_message()
async def on_deleted(event: EventMessageRemoved, bot: Bot):
    await bot.send(
        f"Сообщение {event.message_id} было удалено (event.message_removed).",
        chat_id=event.chat_id,
    )


