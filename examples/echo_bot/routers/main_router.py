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
    keyboard.add_button(ButtonCallback("Echo", "echo"))
    await bot.send("Hello, " + message.body.text, [keyboard.get_keyboard()], user_id=message.sender.user_id)

@router.callback_query(F.callback.payload == "echo")
async def handle_callback_query(event: EventMessageCallback, bot: Bot):
    message = NewMessageBody(
        text=event.message.body.text,
    )
    await bot.send_model(message, user_id=event.callback.user.user_id)