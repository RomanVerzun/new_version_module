import asyncio
import functools
import aiohttp
import time
from typing import Callable, Any
from aiohttp import ClientSession

async def delay(delay_seconds: int) -> int:
    print(f' засыпаю на {delay_seconds} секунд')
    await asyncio.sleep(delay_seconds)
    print(f'сон в течении {delay_seconds} секунд закончился')
    return delay_seconds

def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'Выполняется {func} с аргументами {args} {kwargs}')
            start = time.time()
            
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func} завершилась за {total:.4f} секунды')
        return wrapped
    return wrapper

async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status