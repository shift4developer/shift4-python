from shift4.resource import Resource


class Plans(Resource):
    def create(self, params, request_options=None):
        return self._post("/plans", params, request_options=request_options)

    def get(self, plan_id):
        return self._get("/plans/%s" % plan_id)

    def update(self, plan_id, params, request_options=None):
        return self._post(
            "/plans/%s" % plan_id, params, request_options=request_options
        )

    def delete(self, plan_id):
        return self._delete("/plans/%s" % plan_id)

    def list(self, params=None):
        return self._get("/plans", params)
