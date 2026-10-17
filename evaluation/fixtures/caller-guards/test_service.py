from service import register_user


def test_rejects_empty_name():
    try:
        register_user("  ")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")


def test_accepts_name():
    assert register_user(" Ada ") == {"display_name": "ada"}
