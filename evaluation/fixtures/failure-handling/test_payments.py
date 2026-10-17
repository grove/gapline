from payments import PaymentClient


class AlwaysSucceeds:
    def charge(self, account, amount):
        return {"approved": True}


def test_successful_payment():
    result = PaymentClient(AlwaysSucceeds()).charge("demo", 10)
    assert result["approved"]
