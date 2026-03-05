from magic_filter import F

from core.api import MaxApi
from core.bot import Bot
from core.events import EventMessageCreated
from core.handlers.router import Router

router = Router()


@router.message()
async def handle_message(event: EventMessageCreated, bot: Bot):
    message = event.message
    await bot.send("Hello, " + message.body.text, message.sender.user_id)

