from magic_filter import F

from core.api import MaxApi
from core.bot import Bot
from core.events import EventMessageCreated
from core.handlers.router import Router
from core.keyboards import Keyboard, ButtonCallback

router = Router()


@router.message()
async def handle_message(event: EventMessageCreated, bot: Bot):
    message = event.message
    keyboard = Keyboard()
    keyboard.add_button(ButtonCallback("Red", "red"))
    await bot.send("Hello, " + message.body.text, [keyboard.get_keyboard()], user_id=message.sender.user_id)

