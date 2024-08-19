class RequestOptions:
    def __init__(self, idempotency_key=None):
        self.idempotency_key = idempotency_key

    def has_idempotency_key(self):
        return self.idempotency_key is not None

    def get_idempotency_key(self):
        return self.idempotency_key
