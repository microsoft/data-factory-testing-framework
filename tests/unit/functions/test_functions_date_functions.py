import data_factory_testing_framework._functions.functions_date_implementation as date_functions
import pytest
from _pytest.mark import param
from data_factory_testing_framework.pythonnet.csharp_datetime import CSharpDateTime


def test_utcnow(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr(CSharpDateTime, "utcnow", lambda: CSharpDateTime.parse("2023-11-24T12:11:54.7531321Z"))

    # Act
    actual = date_functions.utcnow()

    # Assert
    assert actual == "2023-11-24T12:11:54.7531321Z"


@pytest.mark.parametrize(
    "date_time_str, expected_ticks",
    [
        param("2023-11-24T12:11:54.753132", 638364247147531320, id="ticks"),
        param("2023-11-24T00:00:00", 638363808000000000, id="ticks_without_microseconds"),
    ],
)
def test_ticks(date_time_str: str, expected_ticks: int) -> None:
    # Act
    actual = CSharpDateTime.parse(date_time_str).ticks()

    # Assert
    assert actual == expected_ticks


@pytest.mark.parametrize(
    "seconds, expected",
    [
        param(-5, "2023-11-24T12:11:44.7531321Z", id="negative"),
        param(125, "2023-11-24T12:13:54.7531321Z", id="positive"),
        param(3601, "2023-11-24T13:11:50.7531321Z", id="positive_one_hour"),
        param(3600 * 24, "2023-11-25T12:11:49.7531321Z", id="positive_one_day"),
    ],
)
def test_add_seconds(seconds: int, expected: str) -> None:
    result: str = date_functions.add_seconds("2023-11-24T12:11:49.7531321Z", seconds)
    assert result == expected


@pytest.mark.parametrize(
    "minutes, expected",
    [
        param(-5, "2023-11-24T12:06:49.7531321Z", id="negative"),
        param(125, "2023-11-24T14:16:49.7531321Z", id="positive"),
    ],
)
def test_add_minutes(minutes: int, expected: str) -> None:
    result: str = date_functions.add_minutes("2023-11-24T12:11:49.7531321Z", minutes)
    assert result == expected


@pytest.mark.parametrize(
    "hours, expected",
    [
        param(-2, "2023-11-24T10:11:49.7531321Z", id="negative"),
        param(3, "2023-11-24T15:11:49.7531321Z", id="positive"),
    ],
)
def test_add_hours(hours: int, expected: str) -> None:
    result: str = date_functions.add_hours("2023-11-24T12:11:49.7531321Z", hours)
    assert result == expected


@pytest.mark.parametrize(
    "days, expected",
    [
        param(-1, "2023-11-23T12:11:49.7531321Z", id="negative"),
        param(2, "2023-11-26T12:11:49.7531321Z", id="positive"),
        param(30, "2023-12-24T12:11:49.7531321Z", id="month"),
    ],
)
def test_add_days(days: int, expected: str) -> None:
    result: str = date_functions.add_days("2023-11-24T12:11:49.7531321Z", days)
    assert result == expected


@pytest.mark.parametrize(
    "interval, time_unit, expected",
    [
        param(-1, "Second", "2023-11-24T12:11:48.7531321Z", id="negative-second"),
        param(-1, "Minute", "2023-11-24T12:10:49.7531321Z", id="negative-minute"),
        param(-1, "Hour", "2023-11-24T11:11:49.7531321Z", id="negative-hour"),
        param(-1, "Day", "2023-11-23T12:11:49.7531321Z", id="negative-day"),
        param(-1, "Week", "2023-11-17T12:11:49.7531321Z", id="negative-week"),
        param(-1, "Month", "2023-10-24T12:11:49.7531321Z", id="negative-month"),
        param(-1, "Year", "2022-11-24T12:11:49.7531321Z", id="negative-year"),
        param(5, "Second", "2023-11-24T12:11:54.7531321Z", id="positive-second"),
        param(5, "Minute", "2023-11-24T12:16:49.7531321Z", id="positive-minute"),
        param(5, "Hour", "2023-11-24T17:11:49.7531321Z", id="positive-hour"),
        param(5, "Day", "2023-11-29T12:11:49.7531321Z", id="positive-day"),
        param(5, "Week", "2023-12-29T12:11:49.7531321Z", id="positive-week"),
        param(5, "Month", "2024-04-24T12:11:49.7531321Z", id="positive-month"),
        param(5, "Year", "2028-11-24T12:11:49.7531321Z", id="positive-year"),
    ],
)
def test_add_to_time(interval: int, time_unit: str, expected: str) -> None:
    result: str = date_functions.add_to_time("2023-11-24T12:11:49.7531321Z", interval, time_unit)
    assert result == expected


def test_add_to_time_unknown_interval_throws_error() -> None:
    with pytest.raises(ValueError):
        date_functions.add_to_time("2023-11-24T12:11:49.7531321Z", 5, "Unknown")


@pytest.mark.parametrize(
    "interval, time_unit, expected",
    [
        param(-1, "Second", "2023-11-24T12:11:48.7531321Z", id="negative-second"),
        param(-1, "Minute", "2023-11-24T12:10:49.7531321Z", id="negative-minute"),
        param(-1, "Hour", "2023-11-24T11:11:49.7531321Z", id="negative-hour"),
        param(-1, "Day", "2023-11-23T12:11:49.7531321Z", id="negative-day"),
        param(-1, "Week", "2023-11-17T12:11:49.7531321Z", id="negative-week"),
        param(-1, "Month", "2023-10-24T12:11:49.7531321Z", id="negative-month"),
        param(-1, "Year", "2022-11-24T12:11:49.7531321Z", id="negative-year"),
        param(5, "Second", "2023-11-24T12:11:54.7531321Z", id="positive-second"),
        param(5, "Minute", "2023-11-24T12:16:49.7531321Z", id="positive-minute"),
        param(5, "Hour", "2023-11-24T17:11:49.7531321Z", id="positive-hour"),
        param(5, "Day", "2023-11-29T12:11:49.7531321Z", id="positive-day"),
        param(5, "Week", "2023-12-29T12:11:49.7531321Z", id="positive-week"),
        param(5, "Month", "2024-04-24T12:11:49.7531321Z", id="positive-month"),
        param(5, "Year", "2028-11-24T12:11:49.7531321Z", id="positive-year"),
    ],
)
def test_get_future_time(interval: int, time_unit: str, expected: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(CSharpDateTime, "utcnow", lambda: CSharpDateTime.parse("2023-11-24T12:11:49.7531321Z"))
    result: str = date_functions.get_future_time(interval, time_unit)
    assert result == expected


@pytest.mark.parametrize(
    "interval, time_unit, expected",
    [
        param(1, "Second", "2023-11-24T12:11:48.7531321Z", id="negative-second"),
        param(1, "Minute", "2023-11-24T12:10:49.7531321Z", id="negative-minute"),
        param(1, "Hour", "2023-11-24T11:11:49.7531321Z", id="negative-hour"),
        param(1, "Day", "2023-11-23T12:11:49.7531321Z", id="negative-day"),
        param(1, "Week", "2023-11-17T12:11:49.7531321Z", id="negative-week"),
        param(1, "Month", "2023-10-24T12:11:49.7531321Z", id="negative-month"),
        param(1, "Year", "2022-11-24T12:11:49.7531321Z", id="negative-year"),
        param(-5, "Second", "2023-11-24T12:11:54.7531321Z", id="positive-second"),
        param(-5, "Minute", "2023-11-24T12:16:49.7531321Z", id="positive-minute"),
        param(-5, "Hour", "2023-11-24T17:11:49.7531321Z", id="positive-hour"),
        param(-5, "Day", "2023-11-29T12:11:49.7531321Z", id="positive-day"),
        param(-5, "Week", "2023-12-29T12:11:49.7531321Z", id="positive-week"),
        param(-5, "Month", "2024-04-24T12:11:49.7531321Z", id="positive-month"),
        param(-5, "Year", "2028-11-24T12:11:49.7531321Z", id="positive-year"),
    ],
)
def test_subtract_to_time(interval: int, time_unit: str, expected: str) -> None:
    result: str = date_functions.subtract_from_time("2023-11-24T12:11:49.7531321Z", interval, time_unit)
    assert result == expected


@pytest.mark.parametrize(
    "interval, time_unit, expected",
    [
        param(1, "Second", "2023-11-24T12:11:48.7531321Z", id="negative-second"),
        param(1, "Minute", "2023-11-24T12:10:49.7531321Z", id="negative-minute"),
        param(1, "Hour", "2023-11-24T11:11:49.7531321Z", id="negative-hour"),
        param(1, "Day", "2023-11-23T12:11:49.7531321Z", id="negative-day"),
        param(1, "Week", "2023-11-17T12:11:49.7531321Z", id="negative-week"),
        param(1, "Month", "2023-10-24T12:11:49.7531321Z", id="negative-month"),
        param(1, "Year", "2022-11-24T12:11:49.7531321Z", id="negative-year"),
        param(-5, "Second", "2023-11-24T12:11:54.7531321Z", id="positive-second"),
        param(-5, "Minute", "2023-11-24T12:16:49.7531321Z", id="positive-minute"),
        param(-5, "Hour", "2023-11-24T17:11:49.7531321Z", id="positive-hour"),
        param(-5, "Day", "2023-11-29T12:11:49.7531321Z", id="positive-day"),
        param(-5, "Week", "2023-12-29T12:11:49.7531321Z", id="positive-week"),
        param(-5, "Month", "2024-04-24T12:11:49.7531321Z", id="positive-month"),
        param(-5, "Year", "2028-11-24T12:11:49.7531321Z", id="positive-year"),
    ],
)
def test_get_past_time(interval: int, time_unit: str, expected: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(CSharpDateTime, "utcnow", lambda: CSharpDateTime.parse("2023-11-24T12:11:49.7531321Z"))

    result: str = date_functions.get_past_time(interval, time_unit)
    assert result == expected


@pytest.mark.parametrize(
    "timestamp, expected",
    [
        param("2023-11-24T12:11:49.7531321Z", "2023-11-24T00:00:00.0000000Z"),
        param("2024-01-05T23:59:49.7531321Z", "2024-01-05T00:00:00.0000000Z"),
    ],
)
def test_start_of_day(timestamp: str, expected: str) -> None:
    result: str = date_functions.start_of_day(timestamp)
    assert result == expected


@pytest.mark.parametrize(
    "timestamp, expected",
    [
        param("2023-11-24T12:11:49.7531321Z", "2023-11-24T12:00:00.0000000Z"),
        param("2024-01-05T23:59:49.7531321Z", "2024-01-05T23:00:00.0000000Z"),
    ],
)
def test_start_of_hour(timestamp: str, expected: str) -> None:
    result: str = date_functions.start_of_hour(timestamp)
    assert result == expected


@pytest.mark.parametrize(
    "timestamp, expected",
    [
        param("2023-11-24T12:11:49.7531321Z", "2023-11-01T00:00:00.0000000Z"),
        param("2024-01-05T23:59:49.7531321Z", "2024-01-01T00:00:00.0000000Z"),
    ],
)
def test_start_of_month(timestamp: str, expected: str) -> None:
    result: str = date_functions.start_of_month(timestamp)
    assert result == expected


def test_format_date_time() -> None:
    result: str = date_functions.format_date_time("2023-11-24T12:11:49")
    assert result == "2023-11-24T12:11:49.0000000"


@pytest.mark.parametrize(
    "timezone_name, expected",
    [
        param("SA Western Standard Time", "2023-11-24T08:11:49.7531321"),
        param("GMT Standard Time", "2023-11-24T12:11:49.7531321"),
        param("W. Europe Standard Time", "2023-11-24T13:11:49.7531321"),
    ],
)
def test_convert_from_utc(timezone_name: str, expected: str) -> None:
    result: str = date_functions.convert_from_utc("2023-11-24T12:11:49.7531321Z", timezone_name)
    assert result == expected


def test_convert_time_zone() -> None:
    result: str = date_functions.convert_time_zone(
        "2023-11-24T12:11:49.7531321", "SA Western Standard Time", "W. Europe Standard Time"
    )
    assert result == "2023-11-24T17:11:49.7531321"


def test_convert_to_utc() -> None:
    result: str = date_functions.convert_to_utc("2023-11-24T12:11:49.7531321", "W. Europe Standard Time")
    assert result == "2023-11-24T11:11:49.7531321Z"


@pytest.mark.parametrize(
    "timestamp, expected",
    [
        param("2023-11-24T12:11:49.7531321Z", 5),
        param("2024-01-04T23:59:49.7531321Z", 4),
        param("2024-05-17T23:59:49.7531321Z", 5),
    ],
)
def test_day_of_week(timestamp: str, expected: int) -> None:
    result: int = date_functions.day_of_week(timestamp)
    assert result == expected


@pytest.mark.parametrize(
    "timestamp, expected",
    [
        param("2023-11-24T12:11:49.7531321Z", 24),
        param("2024-01-04T23:59:49.7531321Z", 4),
        param("2024-05-17T23:59:49.7531321Z", 17),
    ],
)
def test_day_of_month(timestamp: str, expected: int) -> None:
    result: int = date_functions.day_of_month(timestamp)
    assert result == expected


@pytest.mark.parametrize(
    "timestamp, expected",
    [
        param("2023-11-24T12:11:49.7531321Z", 328),
        param("2024-01-04T23:59:49.7531321Z", 4),
        param("2024-05-17T23:59:49.7531321Z", 138),
    ],
)
def test_day_of_year(timestamp: str, expected: int) -> None:
    result: int = date_functions.day_of_year(timestamp)
    assert result == expected
