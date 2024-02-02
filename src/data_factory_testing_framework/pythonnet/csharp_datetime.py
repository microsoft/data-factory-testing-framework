#  These imports are dotnet namespace imports which are registered via __init__.py
import System  # noqa: F401
from System import DateTime  # noqa: F401


class CSharpDateTime:
    def __init__(self, date_time: DateTime) -> None:
        """Initializes a new instance of the CSharpDateTime class."""
        self.date_time = date_time

    @staticmethod
    def parse(timestamp: str) -> "CSharpDateTime":
        return CSharpDateTime(
            DateTime.Parse(
                timestamp,
                System.Globalization.CultureInfo.InvariantCulture,
                System.Globalization.DateTimeStyles.RoundtripKind,
            )
        )

    @staticmethod
    def utcnow() -> "CSharpDateTime":
        return CSharpDateTime(DateTime.UtcNow)

    def ticks(self) -> int:
        return self.date_time.get_Ticks()

    def add_seconds(self, seconds: int) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.AddSeconds(seconds))

    def add_minutes(self, seconds: int) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.AddMinutes(seconds))

    def add_hours(self, hours: int) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.AddHours(hours))

    def add_days(self, days: int) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.AddDays(days))

    def add_months(self, months: int) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.AddMonths(months))

    def add_years(self, years: int) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.AddYears(years))

    def day_of_week(self) -> int:
        return int(self.date_time.get_DayOfWeek())

    def day_of_month(self) -> int:
        return int(self.date_time.get_Day())

    def day_of_year(self) -> int:
        return int(self.date_time.get_DayOfYear())

    def format_date_time(self, fmt: str = None) -> str:
        if fmt is None:
            fmt = "o"

        return self.date_time.ToString(fmt)

    def start_of_day(self) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.Date)

    def start_of_hour(self) -> "CSharpDateTime":
        return CSharpDateTime(self.date_time.Date.AddHours(self.date_time.Hour))

    def start_of_month(self) -> "CSharpDateTime":
        return CSharpDateTime(
            DateTime(self.date_time.Year, self.date_time.Month, 1, 0, 0, 0, self.date_time.get_Kind())
        )

    def convert_timestamp_to_target_timezone(self, target_timezone: str) -> "CSharpDateTime":
        target_time_zone = System.TimeZoneInfo.FindSystemTimeZoneById(target_timezone)
        return CSharpDateTime(System.TimeZoneInfo.ConvertTime(self.date_time, target_time_zone))

    def convert_timestamp_from_timezone_to_target_timezone(
        self, source_timezone: str, target_timezone: str
    ) -> "CSharpDateTime":
        source_time_zone = System.TimeZoneInfo.FindSystemTimeZoneById(source_timezone)
        target_time_zone = System.TimeZoneInfo.FindSystemTimeZoneById(target_timezone)
        return CSharpDateTime(System.TimeZoneInfo.ConvertTime(self.date_time, source_time_zone, target_time_zone))

    def convert_timestamp_from_timezone_to_utc(self, source_timezone: str) -> "CSharpDateTime":
        source_time_zone = System.TimeZoneInfo.FindSystemTimeZoneById(source_timezone)
        return CSharpDateTime(System.TimeZoneInfo.ConvertTimeToUtc(self.date_time, source_time_zone))
