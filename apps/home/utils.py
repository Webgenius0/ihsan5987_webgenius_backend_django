from rest_framework.throttling import UserRateThrottle
from django.utils.timesince import timesince
import re


def timesince_short(datetime_obj):
    """
    Convert Django's timesince output to short form for mobile displays.
    Examples:
        "1 day, 2 hours" → "1d"
        "2 hours, 30 minutes" → "2h"
        "3 weeks, 1 day" → "3w"
        "0 minutes" → "0m"
    """
    time_str = timesince(datetime_obj)

    # Split by comma and take only the first part (most significant unit)
    first_part = time_str.split(",")[0].strip()

    # Extract number and unit using regex
    match = re.match(r"(\d+)\s+(\w+)", first_part)

    if not match:
        return "0m"

    number = match.group(1)
    unit = match.group(2)

    # Map full unit names to short forms
    unit_map = {
        "year": "y",
        "years": "y",
        "month": "mo",
        "months": "mo",
        "week": "w",
        "weeks": "w",
        "day": "d",
        "days": "d",
        "hour": "h",
        "hours": "h",
        "minute": "m",
        "minutes": "m",
        "second": "s",
        "seconds": "s",
    }

    short_unit = unit_map.get(unit, unit[0])

    return f"{number}{short_unit}"


class SearchGenThrottle(UserRateThrottle):
    scope = "search_gen"
