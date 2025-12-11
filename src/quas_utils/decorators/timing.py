"""
Timing decorator for Flask applications.
"""

from functools import wraps
from time import perf_counter
from typing import Any, Callable

from quas_utils.logging.loggers import console_log


def get_time(func: Callable) -> Callable:
    """
    Measure execution time for a callable and log the duration at INFO level.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: float = perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = perf_counter()
        console_log(
            "INFO",
            f"'{func.__name__}()' took {end_time - start_time:.3f} seconds to execute",
        )
        return result

    return wrapper