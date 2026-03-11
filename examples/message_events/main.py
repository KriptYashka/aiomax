import asyncio
import os

from dotenv import load_dotenv

from core.bot import Bot
from core.longpoll import MaxLongPoll
from examples.message_events.dispatcher import dispatcher
from logs.logger import Logger


async def main():
    load_dotenv()
    Logger.setup_logging()

    token = os.getenv("TOKEN")
    proxy = os.getenv("HTTP_PROXY")

    bot = Bot(token, proxy=proxy)
    longpoll = MaxLongPoll(bot)

    await longpoll.run(dispatcher)


if __name__ == "__main__":
    asyncio.run(main())


