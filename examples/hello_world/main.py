import asyncio
import os

from dotenv import load_dotenv

from core.bot import Bot
from core.handlers.router import Router
from core.longpoll import MaxLongPoll

from dispatcher import dispatcher


async def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    proxy = os.getenv("HTTP_PROXY")

    bot = Bot(token, proxy=proxy)
    longpoll = MaxLongPoll(bot)

    await longpoll.run(dispatcher)


if __name__ == "__main__":
    asyncio.run(main())
