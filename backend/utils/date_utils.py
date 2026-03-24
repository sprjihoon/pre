from datetime import date, timedelta

WEEKDAY_NAMES_KR = ["월", "화", "수", "목", "금", "토", "일"]


def get_weekday_kr(d: date) -> str:
    return WEEKDAY_NAMES_KR[d.weekday()]


def date_range(start: date, end: date) -> list[date]:
    days = (end - start).days + 1
    return [start + timedelta(days=i) for i in range(days)]
