import asyncio
import logging
import time
from enum import Enum
from http.client import HTTPException, responses

import aiohttp


class HTTPMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5

    @classmethod
    def get_session_method(cls, session: aiohttp.ClientSession, method: "HTTPMethod"):
        methods = {
            HTTPMethod.GET: session.get,
            HTTPMethod.POST: session.post,
            HTTPMethod.PUT: session.put,
            HTTPMethod.PATCH: session.patch,
            HTTPMethod.DELETE: session.delete,
        }
        return methods[method]


class MaxApi:
    """
    Отправляет запросы по MAX API и контролирует кол-во запросов в секунду.
    """
    __base_url = "https://platform-api.max.ru/"

    def __init__(self, token: str, proxy: str = None):
        self.token = token
        self.proxy = proxy

        self.RPS_DELAY = 1 / 30
        self.last_request_dt = time.time()

        self.headers = {
            "Authorization": self.token + "a",
            "Content-Type": "application/json",
        }

        self.session = aiohttp.ClientSession()

    async def _delay(self):
        delay_time = max(self.RPS_DELAY - (time.time() - self.last_request_dt), 0)
        if delay_time:
            await asyncio.sleep(delay_time)

    async def get(self, method: str, params: dict = None):
        url = self.__base_url + method
        return await self._send(HTTPMethod.GET, url, params)

    async def post(self, method: str, params: dict = None):
        url = self.__base_url + method
        return await self._send(HTTPMethod.POST, url, params)

    async def put(self, method: str, params: dict = None):
        url = self.__base_url + method
        return await self._send(HTTPMethod.PUT, url, params)

    async def patch(self, method: str, params: dict = None):
        url = self.__base_url + method
        return await self._send(HTTPMethod.PATCH, url, params)

    async def delete(self, method: str, params: dict = None):
        url = self.__base_url + method
        return await self._send(HTTPMethod.DELETE, url, params)

    async def _send(
            self,
            http_method: HTTPMethod,
            url: str,
            params: dict = None
    ) -> dict:
        await self._delay()
        params = {
            "url": url,
            "data": params,
            "headers": self.headers,
            "proxy": self.proxy,
        }
        async with HTTPMethod.get_session_method(self.session, http_method)(**params) as response:
            data = await response.json()
        if response.status != 200:
            raise HTTPException(f"[{response.status}] {data.get('code')}. Message: {data.get('message')}")
        return data

    async def close(self):
        await self.session.close()
