from magic_filter import F

from core.bot import Bot
from core.events import EventMessageCreated, EventMessageCallback
from core.handlers.router import Router
from core.keyboards import Keyboard, ButtonCallback
from core.objects.message import NewMessageBody

router = Router()


@router.message()
async def handle_message(event: EventMessageCreated, bot: Bot):
    message = event.message
    keyboard = Keyboard()
    keyboard.add_button(ButtonCallback("Test Button", "test"))
    await bot.send("Hello, " + message.body.text, [keyboard.get_keyboard()], user_id=message.sender.user_id)

@router.callback_query(F.callback.payload == "test")
async def handle_callback_query(event: EventMessageCallback, bot: Bot):
    message = NewMessageBody(
        text="Нажата красная кнопка"
    )
    await bot.send_model(message, user_id=event.callback.user.user_id)