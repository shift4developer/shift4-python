from shift4.resource import Resource


class Disputes(Resource):
    def get(self, dispute_id):
        return self._get("/disputes/%s" % dispute_id)

    def update(self, dispute_id, params, request_options=None):
        return self._post(
            "/disputes/%s" % dispute_id, params, request_options=request_options
        )

    def close(self, dispute_id, request_options=None):
        return self._post(
            "/disputes/%s/close" % dispute_id, request_options=request_options
        )

    def list(self, params=None):
        return self._get("/disputes", params)
