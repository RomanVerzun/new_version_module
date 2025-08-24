"""Asynchronous helpers and decorators."""

import asyncio
import functools
import time
from typing import Any, Callable

from aiohttp import ClientSession

SLEEP_MSG = "засыпаю на {seconds} секунд"
SLEEP_DONE_MSG = "сон в течении {seconds} секунд закончился"
RUNNING_MSG = "Выполняется {func} с аргументами {args} {kwargs}"
FINISHED_MSG = "{func} завершилась за {total:.4f} секунды"


async def delay(seconds: int) -> int:
    """Pause execution for a given number of seconds."""
    print(SLEEP_MSG.format(seconds=seconds))
    await asyncio.sleep(seconds)
    print(SLEEP_DONE_MSG.format(seconds=seconds))
    return seconds


def async_timed() -> Callable:
    """Decorator for timing asynchronous functions."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(RUNNING_MSG.format(func=func, args=args, kwargs=kwargs))
            start_time = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed = time.time() - start_time
                print(FINISHED_MSG.format(func=func, total=elapsed))

        return wrapped

    return decorator


async def fetch_status(
    session: ClientSession, url: str, delay: int = 0
) -> int:
    """Fetch the HTTP status code for a URL after an optional delay."""
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status
