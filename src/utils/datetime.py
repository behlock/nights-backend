from datetime import datetime


def str_to_datetime(date_string):
    try:
        # Define the format of the input date string
        date_format = "%Y-%m-%dT%H:%M:%S.%f"

        # Use datetime.strptime() to parse the string into a datetime object
        datetime_obj = datetime.strptime(date_string, date_format)
        return datetime_obj

    except ValueError as e:
        print(f"Error: {e}")
        return None
