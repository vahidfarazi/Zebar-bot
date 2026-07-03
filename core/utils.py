from datetime import datetime

from core.settings import (
    WORK_START,
    WORK_END,
    WEEKEND,
)


def is_work_time():

    now = datetime.now()

    if now.weekday() in WEEKEND:
        return False

    if now.hour < WORK_START:
        return False

    if now.hour >= WORK_END:
        return False

    return True
