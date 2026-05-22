"""ISO-8601 datetime helpers.

The previous implementation hard-coded ``%Y-%m-%dT%H:%M:%S.%f`` and silently
returned ``None`` for any deviation. RA's responses occasionally drop the
microseconds field, which used to skip whole events. ``dateutil.parser.isoparse``
handles both forms transparently.
"""

from __future__ import annotations

from datetime import datetime

import structlog
from dateutil import parser as dt_parser

logger = structlog.get_logger(__name__)

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def str_to_datetime(date_string: str | None) -> datetime | None:
    if not date_string:
        return None
    try:
        return dt_parser.isoparse(date_string)
    except (ValueError, TypeError):
        logger.warning("datetime_parse_failed", value=date_string)
        return None


def datetime_to_str(value: datetime) -> str:
    return value.strftime(DATE_FORMAT)
