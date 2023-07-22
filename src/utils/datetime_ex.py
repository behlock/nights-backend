from typing import Optional
from datetime import datetime

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def str_to_datetime(date_string: str) -> Optional[datetime]:
    try:
        datetime_obj = datetime.strptime(date_string, DATE_FORMAT)
        return datetime_obj

    except ValueError as e:
        print(f"Error: {e}")
        return None


def datetime_to_str(datetime: datetime) -> Optional[str]:
    try:
        date_string = datetime.strftime(DATE_FORMAT)
        return date_string

    except ValueError as e:
        print(f"Error: {e}")
        return None
