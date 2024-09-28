import functools
import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def retry_async(retries=3, delay=2, exception_types=(Exception,)):
    """
    A decorator to automatically retry a function in case of specified exceptions.

    :param retries: Number of retry attempts.
    :param delay: Delay between retries in seconds.
    :param exception_types: Tuple of exception types to catch and retry on.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return await func(*args, **kwargs)
                except exception_types as e:
                    attempt += 1
                    logger.warning(f"Function '{func.__name__}' failed on attempt {attempt}/{retries}: {str(e)}")

                    # Try to find session in args: update_player_vanilla_stats_async
                    session = None
                    for arg in args:
                        if isinstance(arg, AsyncSession):
                            session = arg
                            logger.warning(f"Function '{func.__name__}' rolling back session!")
                            await session.rollback()  
                            break

                    if attempt < retries:
                        await asyncio.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator