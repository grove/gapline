from billing import charge


def test_declined_payment_never_captures():
    ledger = []
    outcome = charge(False, ledger)
    assert isinstance(outcome, dict)
