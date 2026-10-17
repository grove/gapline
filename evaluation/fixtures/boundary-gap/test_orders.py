from orders import consume, submit


def test_web_request_is_consumed():
    assert consume(submit(3)) == {"allocated": 3}


def test_independent_partner_request_is_consumed():
    assert consume({"quantity": 100}) == {"allocated": 100}


def test_submit_rejects_invalid_quantities():
    for quantity in (0, 101, -1, True, "3"):
        try:
            submit(quantity)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid quantity was accepted")
