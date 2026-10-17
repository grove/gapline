from slug import slug


def test_whitespace_and_case():
    assert slug("  Hello   World  ") == "hello-world"


def test_empty_text():
    assert slug("") == ""


def test_already_slugged():
    assert slug("already-slugged") == "already-slugged"
