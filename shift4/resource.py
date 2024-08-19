import sys

import requests

import shift4 as api
from shift4.__version__ import __version__


class Resource(object):
    def name(self):
        return self.__class__.__name__.lower()

    def _get(self, path, params=None, url=None):
        return self.__request("GET", path, params=params, url=url)

    def _post(self, path, json=None, url=None, request_options=None):
        return self.__request(
            "POST", path, json=json, url=url, request_options=request_options
        )

    def _multipart(self, path, params=None, files=None, url=None):
        return self.__request("POST", path, params=params, files=files, url=url)

    def _delete(self, path, params=None, url=None):
        return self.__request("DELETE", path, params=params, url=url)

    @classmethod
    def __request(
        cls,
        method,
        path,
        params=None,
        json=None,
        files=None,
        url=None,
        request_options=None,
    ):
        if url is None:
            url = api.api_url.rstrip("/")
        resp = requests.request(
            method,
            url=url + path,
            auth=(api.secret_key, ""),
            headers=cls.__create_headers(request_options),
            files=files,
            params=params,
            json=json,
        )

        json = resp.json()
        if resp.status_code == 200:
            return json
        error = json.get("error")
        if error is None:
            raise api.Shift4Exception("Internal error", None, json, None, None)
        raise api.Shift4Exception(
            error.get("type"),
            error.get("code"),
            error.get("message"),
            error.get("charge_id"),
            error.get("blacklist_rule_id"),
        )

    @classmethod
    def __create_headers(cls, request_options=None):
        user_agent = "Shift4-Python/%s (Python/%s.%s.%s)" % (
            __version__,
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro,
        )
        headers = {"User-Agent": user_agent}
        if request_options is not None and "idempotency_key" in request_options:
            headers["Idempotency-Key"] = request_options["idempotency_key"]
        return headers
