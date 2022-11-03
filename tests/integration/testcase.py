import os

import pytest
from dotenv import load_dotenv

import shift4 as shift4

load_dotenv()


class TestCase:
    @pytest.fixture
    def api(self):
        previous_secret_key = shift4.secret_key
        previous_api_url = shift4.api_url
        previous_uploads_url = shift4.uploads_url

        shift4.secret_key = os.getenv("SECRET_KEY")
        shift4.api_url = os.getenv("API_URL", previous_api_url)
        shift4.uploads_url = os.getenv("UPLOADS_URL", previous_uploads_url)
        yield shift4

        shift4.secret_key = previous_secret_key
        shift4.uploads_url = previous_uploads_url
        shift4.api_url = previous_api_url

    def assert_shift4_exception(self, fun, *args, **kwargs):
        try:
            fun(*args, **kwargs)
        except shift4.Shift4Exception as e:
            return e
        except Exception as e:
            pytest.fail("Wrong exception type received: %s" % str(type(e)))
        else:
            pytest.fail("Didn't receive exception")

    def assert_card_matches_request(self, card, card_req):
        assert card["first6"] == card_req["number"][:6]
        assert card["last4"] == card_req["number"][-4:]
        assert card["expMonth"] == card_req["expMonth"]
        assert card["expYear"] == card_req["expYear"]
        assert card["cardholderName"] == card_req["cardholderName"]

    def assert_list_response_contains_exactly_by_id(self, response, objects):
        response_ids = list(map(lambda o: o["id"], response["list"]))
        object_ids = list(map(lambda o: o["id"], objects))
        assert response_ids == object_ids

    def assertListResponseContainsInAnyOrderById(self, response, objects):
        response_ids = list(map(lambda o: o["id"], response["list"]))
        object_ids = list(map(lambda o: o["id"], objects))
        for oid in object_ids:
            assert oid in response_ids
