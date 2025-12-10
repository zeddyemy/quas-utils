import logging
from functools import wraps
from time import sleep
from typing import Any, Callable

try:
    from sqlalchemy.exc import DataError, DatabaseError, OperationalError  # type: ignore
except ImportError as exc:  # pragma: no cover - enforced via dependency
    raise ImportError(
        "SQLAlchemy is required for quas-utils retry decorator; install `SQLAlchemy`."
    ) from exc


def retry(retries: int = 3, delay: float = 1) -> Callable:
    """
    Retry a callable on failure, useful for Flask apps with database backends.

    Args:
        retries: Maximum attempts before propagating the last error.
        delay: Seconds to wait between attempts.

    Raises:
        ValueError: if retries < 1 or delay <= 0.
    """
    if retries < 1 or delay <= 0:
        raise ValueError("retries must be >= 1 and delay must be > 0")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error: Exception | None = None
            for attempt in range(1, retries + 1):
                try:
                    logging.info(f"Running ({attempt}): {func.__name__}()")
                    return func(*args, **kwargs)
                except (OperationalError, DataError, DatabaseError) as exc:
                    last_error = exc
                    logging.info(
                        f"DB error on attempt {attempt}/{retries}: {repr(exc)}"
                    )
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    logging.info(
                        f"Error on attempt {attempt}/{retries}: {repr(exc)}"
                    )

                if attempt < retries:
                    sleep(delay)

            assert last_error is not None
            raise last_error

        return wrapper

    return decorator
