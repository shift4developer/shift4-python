class RequestOptions:
    __idempotency_key = None

    def set_idempotency_key(self, idempotency_key):
        self.__idempotency_key = idempotency_key

    def has_idempotency_key(self):
        return self.__idempotency_key is not None

    def get_idempotency_key(self):
        return self.__idempotency_key
