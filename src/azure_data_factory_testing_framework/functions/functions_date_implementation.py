from datetime import datetime


def utcnow() -> str:
    return datetime.utcnow().isoformat()


def ticks(date_time: str) -> float:
    return datetime.fromisoformat(date_time).timestamp()
