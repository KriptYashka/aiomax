import asyncio
import os

from dotenv import load_dotenv

from api import MaxApi
from core.longpoll import MaxLongPoll
from logs.logger import setup_logging


async def main():
    setup_logging()
    load_dotenv()
    token = os.getenv("TOKEN")
    proxy = os.getenv("HTTP_PROXY")

    api = MaxApi(token, proxy)
    longpoll = MaxLongPoll(api)

    await longpoll.run()


if __name__ == "__main__":
    asyncio.run(main())
