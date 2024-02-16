from data_factory_testing_framework._pythonnet.csharp_datetime import CSharpDateTime


def utcnow(fmt: str = None) -> str:
    """Return the current timestamp.

    Args:
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.

    Note: This function does not implement formatting for now and
    """
    return CSharpDateTime.utcnow().format_date_time(fmt)


def ticks(timestamp: str) -> int:
    """Return the ticks property value for a specified timestamp. A tick is a 100-nanosecond interval.

    Args:
        timestamp (str): The string for a timestamp
    """
    return CSharpDateTime.parse(timestamp).ticks()


def add_days(timestamp: str, days: int, fmt: str = None) -> str:
    """Add a number of days to a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
        days (int): The positive or negative number of days to add
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).add_days(days).format_date_time(fmt)


def add_hours(timestamp: str, hours: int, fmt: str = None) -> str:
    """Add a number of hours to a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
        hours (int): The positive or negative number of hours to add
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).add_hours(hours).format_date_time(fmt)


def add_minutes(timestamp: str, minutes: int, fmt: str = None) -> str:
    """Add a number of minutes to a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
        minutes (int): The positive or negative number of minutes to add
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).add_minutes(minutes).format_date_time(fmt)


def add_seconds(timestamp: str, seconds: int, fmt: str = None) -> str:
    """Add a number of seconds to a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
        seconds (int): The positive or negative number of seconds to add
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).add_seconds(seconds).format_date_time(fmt)


def add_to_time(timestamp: str, interval: int, time_unit: str, fmt: str = None) -> str:
    """Add a number of time units to a timestamp. See also getFutureTime.

    Args:
        timestamp (str): The string that contains the timestamp
        interval (int): The number of specified time units to add
        time_unit (str): The unit of time to use with interval: "Second", "Minute", "Hour", "Day", "Week", "Month", "Year"
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    if time_unit == "Second":
        return add_seconds(timestamp, interval, fmt)
    elif time_unit == "Minute":
        return add_minutes(timestamp, interval, fmt)
    elif time_unit == "Hour":
        return add_hours(timestamp, interval, fmt)
    elif time_unit == "Day":
        return add_days(timestamp, interval, fmt)
    elif time_unit == "Week":
        return CSharpDateTime.parse(timestamp).add_days(7 * interval).format_date_time(fmt)
    elif time_unit == "Month":
        return CSharpDateTime.parse(timestamp).add_months(interval).format_date_time(fmt)
    elif time_unit == "Year":
        return CSharpDateTime.parse(timestamp).add_years(interval).format_date_time(fmt)
    else:
        raise ValueError(f"Invalid time unit: {time_unit}")


def convert_from_utc(timestamp: str, destination_timezone: str, fmt: str = None) -> str:
    """Convert a timestamp from Universal Time Coordinated (UTC) to the target time zone.

    Args:
        timestamp (str): The string that contains the timestamp
        destination_timezone (str): The name for the target time zone.
        For time zone names, see Microsoft Time Zone Values, but you might have to remove any punctuation from the time zone name.
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return (
        CSharpDateTime.parse(timestamp).convert_timestamp_to_target_timezone(destination_timezone).format_date_time(fmt)
    )


def convert_time_zone(timestamp: str, source_timezone: str, destination_timezone: str, fmt: str = None) -> str:
    """Convert a timestamp from the source time zone to the target time zone.

    Args:
        timestamp (str): The string that contains the timestamp
        source_timezone (str): The name for the source time zone.
        For time zone names, see Microsoft Time Zone Values, but you might have to remove any punctuation from the time zone name.
        destination_timezone (str): The name for the target time zone.
        For time zone names, see Microsoft Time Zone Values, but you might have to remove any punctuation from the time zone name.
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return (
        CSharpDateTime.parse(timestamp)
        .convert_timestamp_from_timezone_to_target_timezone(source_timezone, destination_timezone)
        .format_date_time(fmt)
    )


def convert_to_utc(timestamp: str, source_timezone: str, fmt: str = None) -> str:
    """Convert a timestamp from the source time zone to Universal Time Coordinated (UTC).

    Args:
        timestamp (str): The string that contains the timestamp
        source_timezone (str): The name for the source time zone.
        For time zone names, see Microsoft Time Zone Values, but you might have to remove any punctuation from the time zone name.
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).convert_timestamp_from_timezone_to_utc(source_timezone).format_date_time(fmt)


def day_of_month(timestamp: str) -> int:
    """Return the day of the month component from a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
    """
    return CSharpDateTime.parse(timestamp).day_of_month()


def day_of_week(timestamp: str) -> int:
    """Return the day of the week component from a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
    """
    return CSharpDateTime.parse(timestamp).day_of_week()


def day_of_year(timestamp: str) -> int:
    """Return the day of the year component from a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
    """
    return CSharpDateTime.parse(timestamp).day_of_year()


def format_date_time(timestamp: str, fmt: str = None) -> str:
    """Return the timestamp as a string in optional format.

    Args:
        timestamp (str): The string that contains the timestamp
        fmt (str): The format to use when converting the timestamp to a string
    """
    return CSharpDateTime.parse(timestamp).format_date_time(fmt)


def get_future_time(interval: int, time_unit: str, fmt: str = None) -> str:
    """Return the current timestamp plus the specified time units. See also addToTime.

    Args:
        interval (str): The number of specified time units to add
        time_unit (str): The unit of time to use with interval: "Second", "Minute", "Hour", "Day", "Week", "Month", "Year"
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return add_to_time(utcnow(), interval, time_unit, fmt)


def get_past_time(interval: int, time_unit: str, fmt: str = None) -> str:
    """Return the current timestamp minus the specified time units. See also subtractFromTime.

    Args:
        interval (str): The number of specified time units to subtract
        time_unit (str): The unit of time to use with interval: "Second", "Minute", "Hour", "Day", "Week", "Month", "Year"
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return add_to_time(utcnow(), -interval, time_unit, fmt)


def start_of_day(timestamp: str, fmt: str = None) -> str:
    """Return the start of the day for a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).start_of_day().format_date_time(fmt)


def start_of_hour(timestamp: str, fmt: str = None) -> str:
    """Return the start of the hour for a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).start_of_hour().format_date_time(fmt)


def start_of_month(timestamp: str, fmt: str = None) -> str:
    """Return the start of the month for a timestamp.

    Args:
        timestamp (str): The string that contains the timestamp
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return CSharpDateTime.parse(timestamp).start_of_month().format_date_time(fmt)


def subtract_from_time(timestamp: str, interval: int, time_unit: str, fmt: str = None) -> str:
    """Subtract a number of time units from a timestamp. See also getPastTime.

    Args:
        timestamp (str): The string that contains the timestamp
        interval (int): The number of specified time units to subtract
        time_unit (str): The unit of time to use with interval: "Second", "Minute", "Hour", "Day", "Week", "Month", "Year"
        fmt (str, optional): Optionally, you can specify a different format with the <format> parameter.
    """
    return add_to_time(timestamp, -interval, time_unit, fmt)
