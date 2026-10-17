from reports import prepare


def test_preserves_input_order_and_values():
    names = ["Grace", "Ada", "Ada"]
    result = prepare(names)
    assert result == ["Grace", "Ada", "Ada"]
    assert result is not names
    assert names == ["Grace", "Ada", "Ada"]
