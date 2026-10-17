from notifications import recipients


def test_disjoint_groups_keep_order():
    assert recipients(["ada"], ["grace"]) == ["ada", "grace"]


def test_each_occurrence_remains_a_delivery():
    assert recipients(["ada", "ada"], ["ada"]) == ["ada", "ada", "ada"]


def test_no_requests():
    assert recipients([], []) == []
