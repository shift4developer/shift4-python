from shift4.resource import Resource


class Credits(Resource):
    def create(self, params, request_options=None):
        return self._post("/credits", params, request_options=request_options)

    def get(self, credit_id):
        return self._get("/credits/%s" % credit_id)

    def update(self, credit_id, params, request_options=None):
        return self._post(
            "/credits/%s" % credit_id, params, request_options=request_options
        )

    def list(self, params=None):
        return self._get("/credits", params)
