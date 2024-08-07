from shift4.resource import Resource


class Charges(Resource):
    def create(self, params, request_options=None):
        return self._post("/charges", params, request_options=request_options)

    def get(self, charge_id):
        return self._get("/charges/%s" % charge_id)

    def update(self, charge_id, params, request_options=None):
        return self._post(
            "/charges/%s" % charge_id, params, request_options=request_options
        )

    def list(self, params=None):
        return self._get("/charges", params)

    def capture(self, charge_id, request_options=None):
        return self._post(
            "/charges/%s/capture" % charge_id, request_options=request_options
        )

    def refund(self, charge_id, params=None, request_options=None):
        return self._post(
            "/charges/%s/refund" % charge_id, params, request_options=request_options
        )
