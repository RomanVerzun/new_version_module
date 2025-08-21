"""Utility functions for the module testing application."""

import asyncio
import functools
import time
import logging
from typing import Callable, Any, Optional, Dict, List
from contextlib import contextmanager

try:
    import aiohttp
    from aiohttp import ClientSession
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    ClientSession = None


logger = logging.getLogger(__name__)


class RetryError(Exception):
    """Exception raised when retry attempts are exhausted."""
    pass


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying function calls with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            
            raise RetryError(f"Failed after {max_attempts} attempts") from last_exception
        return wrapper
    return decorator


@contextmanager
def safe_operation(operation_name: str):
    """Context manager for safe operations with proper error logging."""
    try:
        logger.debug(f"Starting operation: {operation_name}")
        yield
        logger.debug(f"Operation completed: {operation_name}")
    except Exception as e:
        logger.error(f"Operation failed: {operation_name} - {e}")
        raise


def validate_address(address: int, min_addr: int = 1, max_addr: int = 255) -> bool:
    """Validate module address is within acceptable range."""
    return isinstance(address, int) and min_addr <= address <= max_addr


def format_binary_data(hex_data: str) -> Optional[str]:
    """Convert hex data to binary string with proper error handling."""
    try:
        return ''.join(format(int(c, 16), '04b') for c in hex_data)
    except (ValueError, TypeError) as e:
        logger.error(f"Failed to format binary data from '{hex_data}': {e}")
        return None


def create_relay_mappings() -> Dict[str, List[tuple]]:
    """Create standardized mappings for relay operations."""
    return {
        'a_indices': [(23 - i, i + 1) for i in range(8)],
        'b_indices': [(34 - i, i + 6) for i in range(3)],
        'c_indices': [(39 - i, i + 1) for i in range(5)],
        'd_indices': [(0, 1), (1, 2), (30, 3), (31, 4), (5, 5), (4, 6), (3, 7), (2, 8)],
        'e_indices': [(29 - i, i + 1) for i in range(6)] + [(7, 7), (6, 8)],
        'f_indices': [(15 - i, i + 1) for i in range(8)]
    }


# Async utilities (existing functions with improvements)
async def delay(delay_seconds: int) -> int:
    """Async delay with logging."""
    logger.info(f'Засыпаю на {delay_seconds} секунд')
    await asyncio.sleep(delay_seconds)
    logger.info(f'Сон в течении {delay_seconds} секунд закончился')
    return delay_seconds


def async_timed():
    """Decorator for timing async functions."""
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            logger.info(f'Выполняется {func.__name__} с аргументами {args} {kwargs}')
            start = time.time()
            
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                logger.info(f'{func.__name__} завершилась за {total:.4f} секунды')
        return wrapped
    return wrapper


async def fetch_status(session: ClientSession, url: str, delay_time: int = 0) -> int:
    """Fetch HTTP status with optional delay."""
    if not AIOHTTP_AVAILABLE:
        raise ImportError("aiohttp is required for fetch_status")
    
    await asyncio.sleep(delay_time)
    async with session.get(url) as result:
        return result.status