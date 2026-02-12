import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from api import MaxApi
from core.longpool import MaxLongPoll


async def main():
    # logging.basicConfig(filename=Path("logs/config.ini"))
    load_dotenv()
    token = os.getenv("TOKEN")
    proxy = os.getenv("HTTP_PROXY")

    api = MaxApi(token, proxy)
    longpool = MaxLongPoll(api)

    await longpool.run()


if __name__ == "__main__":
    asyncio.run(main())
