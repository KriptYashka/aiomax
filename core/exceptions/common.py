import inspect
import logging

from aiohttp import web_exceptions as we


class HTTPExceptionController:
    _stop_pooling = (
        we.HTTPUnauthorized, # 401
        we.HTTPServerError,  # 5xx
    )

    _logging_levels = {
        logging.DEBUG: (

        ),
        logging.INFO: (

        ),
        logging.WARNING: (
            we.HTTPProxyAuthenticationRequired, we.HTTPConflict, we.HTTPUnauthorized
        ),
        logging.ERROR: (
            we.HTTPServerError,
        ),
        logging.CRITICAL: (

        )
    }

    @classmethod
    def need_stop_polling(cls, exception: we.HTTPException):
        return issubclass(exception.__class__, cls._stop_pooling)

    @classmethod
    def log(cls, logger: logging.Logger, exception: we.HTTPException, **kwargs):
        for level in cls._logging_levels:
            types_exception = cls._logging_levels[level]
            if issubclass(exception.__class__, types_exception):
                logger.log(level, exception, **kwargs)
                return

_STATUS_TO_WEB_EXC = {
    cls.status_code: cls
    for _, cls in inspect.getmembers(we, inspect.isclass)
    if issubclass(cls, we.HTTPException) and getattr(cls, "status_code", None)
}

def web_exception_for_status(status: int, **kwargs) -> we.HTTPException:
    """
    Возвращает экземпляр подходящего aiohttp.web_exceptions.* по коду статуса.
    В kwargs можно передать text=..., headers=..., reason=... и т.п.
    """
    exc_cls = _STATUS_TO_WEB_EXC.get(status, we.HTTPException)
    return exc_cls(**kwargs)