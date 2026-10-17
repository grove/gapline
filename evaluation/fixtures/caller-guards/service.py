def _normalize(name):
    return name.strip().lower()


def register_user(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be non-empty")
    return {"display_name": _normalize(name)}
