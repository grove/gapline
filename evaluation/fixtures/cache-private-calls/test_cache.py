from unittest.mock import Mock, patch

from cache import Lookup


def test_construction_and_lookup_smoke():
    Lookup(lambda key: key.upper()).get("ada")


def test_successful_value_is_fetched_once():
    fetch = Mock(return_value="Ada")
    lookup = Lookup(fetch)
    assert lookup.get("ada") == "Ada"
    assert lookup.get("ada") == "Ada"
    fetch.assert_called_once_with("ada")


def test_different_keys_are_independent():
    lookup = Lookup(str.upper)
    assert lookup.get("ada") == "ADA"
    assert lookup.get("grace") == "GRACE"


def test_failed_fetch_can_be_retried():
    fetch = Mock(side_effect=[TimeoutError("not available"), "Ada"])
    lookup = Lookup(fetch)
    try:
        lookup.get("ada")
    except TimeoutError:
        pass
    else:
        raise AssertionError("fetch failure was swallowed")
    assert lookup.get("ada") == "Ada"
    assert fetch.call_count == 2


def test_lookup_calls_private_loader():
    lookup = Lookup(str.upper)
    with patch.object(lookup, "_load", wraps=lookup._load) as load:
        assert lookup.get("ada") == "ADA"
        load.assert_called_once_with("ada")
