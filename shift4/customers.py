from shift4.resource import Resource


class Customers(Resource):
    def create(self, params, request_options=None):
        return self._post("/customers", params, request_options=request_options)

    def get(self, customer_id):
        return self._get("/customers/%s" % customer_id)

    def update(self, customer_id, params, request_options=None):
        return self._post(
            "/customers/%s" % customer_id, params, request_options=request_options
        )

    def delete(self, customer_id):
        return self._delete("/customers/%s" % customer_id)

    def list(self, params=None):
        return self._get("/customers", params)
