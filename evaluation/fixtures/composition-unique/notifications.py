def recipients(primary, secondary):
    return [user_id for group in (primary, secondary) for user_id in group]
