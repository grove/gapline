from dataclasses import dataclass
from datetime import timezone


def instant(value):
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('timestamp must be aware')
    return value.astimezone(timezone.utc)


@dataclass(frozen=True)
class Reading:
    sensor: str
    at: object
    celsius: float


def parse(row):
    sensor, at, value, unit = row
    if not isinstance(sensor, str) or not sensor.strip():
        raise ValueError('sensor must be named')
    at = instant(at)
    if type(value) not in (int, float):
        raise ValueError('temperature must be numeric')
    if unit == 'F':
        lower, upper = -459.67, 1832
    elif unit == 'C':
        lower, upper = -273.15, 1000
    else:
        raise ValueError('unit must be C or F')
    if not lower <= value <= upper:
        raise ValueError('temperature outside supported sensor range')
    celsius = (value - 32) * 5 / 9 if unit == 'F' else float(value)
    return Reading(sensor, at, celsius)
