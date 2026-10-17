class PaymentClient:
    def __init__(self, provider):
        self.provider = provider

    def charge(self, account, amount):
        try:
            return self.provider.charge(account, amount)
        except TimeoutError:
            # Could be a timeout after the remote side effect.
            return self.provider.charge(account, amount)
