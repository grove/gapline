class Client:
    def __init__(self, retry_count=0):
        self.retry_count = retry_count

    def should_retry(self, attempts_used):
        return attempts_used < self.retry_count
