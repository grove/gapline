from notifications import recipients


def test_primary_group():
    assert recipients(["ada"], []) == ["ada"]


def test_secondary_group():
    assert recipients([], ["grace"]) == ["grace"]


def test_disjoint_groups_keep_order():
    assert recipients(["ada"], ["grace"]) == ["ada", "grace"]
