from core.bot import Bot
from core.events import EventMessageCreated
from core.handlers.router import Router
from core.keyboards import Keyboard, ButtonCallback
from core.objects.message import NewMessageBody

router = Router()


@router.message()
async def handle_message(event: EventMessageCreated, bot: Bot):
    message = event.message
    try:
        n, m = map(int, message.body.text.split())
    except Exception:
        await bot.send("Введите два числа\nКол-во строк\nКол-во колонок", user_id=message.sender.user_id)
        return

    buttons = [
        [ButtonCallback(str(i * m + j + 1), payload=str(i * m + j + 1)) for j in range(m)] for i in range(n)
    ]
    keyboard = Keyboard(buttons)

    new_message = NewMessageBody(
        text=f"Кнопки {n}x{m}",
        attachments=[keyboard.get_keyboard()],
    )
    await bot.send(new_message, user_id=message.sender.user_id)
