from shift4.resource import Resource


class Subscriptions(Resource):
    def create(self, params, request_options=None):
        return self._post("/subscriptions", params, request_options=request_options)

    def get(self, subscription_id):
        return self._get("/subscriptions/%s" % subscription_id)

    def update(self, subscription_id, params, request_options=None):
        return self._post(
            "/subscriptions/%s" % subscription_id,
            params,
            request_options=request_options,
        )

    def cancel(self, subscription_id):
        return self._delete("/subscriptions/%s" % subscription_id)

    def list(self, params=None):
        return self._get("/subscriptions", params)
