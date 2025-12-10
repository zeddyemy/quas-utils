"""
Date and time utilities for the QUAS ecosystem.

Provides UTC-aware helpers, formatting/parsing, and fixed GMT+1 conversion.
"""

from datetime import date, datetime, timedelta, timezone

__all__ = ["QuasDateTime", "to_gmt1_or_none"]


def _ordinal_suffix(day: int) -> str:
    """
    Return the ordinal suffix for a day value (e.g., 1 -> 'st', 2 -> 'nd').
    """
    if 11 <= day % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")


class QuasDateTime:
    """
    Utility methods for handling timezone-aware and naive datetime objects in UTC.
    """

    @staticmethod
    def aware_utcnow() -> datetime:
        """
        Return the current time as a timezone-aware UTC datetime.
        """
        return datetime.now(timezone.utc)

    @staticmethod
    def aware_utcfromtimestamp(timestamp: float) -> datetime:
        """
        Convert a POSIX timestamp to a timezone-aware UTC datetime.
        """
        return datetime.fromtimestamp(timestamp, timezone.utc)

    @staticmethod
    def naive_utcnow() -> datetime:
        """
        Return the current time as a naive (timezone-less) UTC datetime.
        """
        return QuasDateTime.aware_utcnow().replace(tzinfo=None)

    @staticmethod
    def naive_utcfromtimestamp(timestamp: float) -> datetime:
        """
        Convert a POSIX timestamp to a naive (timezone-less) UTC datetime.
        """
        return QuasDateTime.aware_utcfromtimestamp(timestamp).replace(tzinfo=None)

    @staticmethod
    def format_date_readable(dt: date) -> str:
        """
        Format a date or datetime as a readable string with an ordinal day suffix.
        """
        suffix = _ordinal_suffix(dt.day)
        return f"{dt.day}{suffix} {dt.strftime('%B')}"

    @staticmethod
    def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format a datetime object using the provided format string.
        """
        return dt.strftime(fmt)

    @staticmethod
    def parse_datetime(dt_str: str, fmt: str) -> datetime:
        """
        Parse a datetime object from a formatted string.
        """
        return datetime.strptime(dt_str, fmt)

    @staticmethod
    def convert_if_not_none(dt: datetime | None) -> datetime | None:
        """
        Convert a datetime to GMT+1 when present; return None otherwise.
        """
        return QuasDateTime.convert_to_gmt_plus_1(dt) if dt is not None else None

    @staticmethod
    def convert_to_gmt_plus_1(dt: datetime) -> datetime:
        """
        Convert a UTC datetime to GMT+1 (fixed offset, no DST adjustments).

        Raises:
            ValueError: if dt is None.
        """
        if dt is None:
            raise ValueError("The datetime object cannot be None.")
        return dt + timedelta(hours=1)


def to_gmt1_or_none(dt: datetime | None) -> datetime | None:
    """
    Convert a datetime to GMT+1 when present; return None otherwise.
    """
    return QuasDateTime.convert_to_gmt_plus_1(dt) if dt is not None else None

