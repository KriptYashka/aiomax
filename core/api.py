import asyncio
import time
from enum import Enum

import aiohttp

from core.exceptions.common import web_exception_for_status
from logs.logger import Logger


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
        Logger.setup_logging()
        self.token = token
        self.proxy = proxy

        self.RPS_DELAY = 1 / 30
        self.last_request_dt = time.time()

        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }

        self.session = aiohttp.ClientSession()

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    async def _delay(self):
        delay_time = max(self.RPS_DELAY - (time.time() - self.last_request_dt), 0)
        if delay_time:
            await asyncio.sleep(delay_time)

    async def get(self, method: str, params: dict = None):
        url = self.__base_url + method
        return await self._send(HTTPMethod.GET, url, params)

    async def post(self, method: str, params: dict = None, data: dict = None):
        url = self.__base_url + method
        return await self._send(HTTPMethod.POST, url, params, data)

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
            params: dict = None,
            data: dict = None,
    ) -> dict:
        await self._delay()
        cleared_params = dict([(key, value) for key, value in params.items() if value])
        method_params = {
            "url": url,
            "params": cleared_params,
            "headers": self.headers,
            "proxy": self.proxy,
            "json": data,
        }

        Logger.logger.debug(f"Request {http_method.name} {url} params={method_params['params']}")
        async with HTTPMethod.get_session_method(self.session, http_method)(**method_params) as response:
            content = await response.json()
        response.close()
        if response.status != 200:
            text = f"[{response.status}] {content.get('code')}. Message: {content.get('message')}"
            raise web_exception_for_status(response.status, reason=text)
        Logger.logger.debug(f"Response {response.status} from {url}: {content}")
        return content

    async def close(self):
        await self.session.close()
