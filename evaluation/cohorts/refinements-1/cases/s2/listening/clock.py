from datetime import timezone


def utc(value):
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('an aware timestamp is required')
    return value.astimezone(timezone.utc)
