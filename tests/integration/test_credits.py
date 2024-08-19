from . import random_string
from .data.credits import valid_credit_req
from .data.customers import valid_customer_req
from .testcase import TestCase


class TestCredits(TestCase):
    def test_create_and_get(self, api):
        # given
        credit_req = valid_credit_req()

        # when
        created = api.credits.create(credit_req)
        got = api.credits.get(created["id"])

        # then
        assert created == got
        assert created["amount"] == credit_req["amount"]
        assert created["currency"] == credit_req["currency"]
        self.assert_card_matches_request(created["card"], credit_req["card"])

    def test_update(self, api):
        # given
        credit_req = valid_credit_req()
        created = api.credits.create(credit_req)

        # when
        updated = api.credits.update(
            created["id"],
            {
                "description": "updated description",
                "metadata": {"key": "updated value"},
            },
        )
        # then
        assert created["description"] == credit_req["description"]
        assert updated["description"] == "updated description"

        assert created["metadata"]["key"] == credit_req["metadata"]["key"]
        assert updated["metadata"]["key"] == "updated value"

        assert updated["amount"] == credit_req["amount"]
        assert updated["currency"] == credit_req["currency"]
        self.assert_card_matches_request(updated["card"], credit_req["card"])

    def test_list(self, api):
        # given
        customer = api.customers.create(valid_customer_req())
        credit_req = valid_credit_req(customerId=customer["id"])
        credit1 = api.credits.create(credit_req)
        credit2 = api.credits.create(credit_req)
        credit3 = api.credits.create(credit_req)

        # when
        all_credits = api.credits.list({"customerId": customer["id"]})
        credits_after_last_id = api.credits.list(
            {"customerId": customer["id"], "startingAfterId": credit3["id"]}
        )

        # then
        self.assert_list_response_contains_exactly_by_id(
            all_credits, [credit3, credit2, credit1]
        )
        self.assert_list_response_contains_exactly_by_id(
            credits_after_last_id, [credit2, credit1]
        )

    def test_will_not_create_duplicate_if_same_idempotency_key_is_used(self, api):
        # given
        idempotency_key = random_string()
        credit_req = valid_credit_req()

        # when
        first_call_response = api.credits.create(
            credit_req,
            request_options={"idempotency_key": idempotency_key},
        )
        second_call_response = api.credits.create(
            credit_req,
            request_options={"idempotency_key": idempotency_key},
        )

        # then
        assert first_call_response == second_call_response

    def test_will_create_two_instances_if_different_idempotency_keys_are_used(
        self, api
    ):
        # given
        credit_req = valid_credit_req()

        # when
        first_call_response = api.credits.create(
            credit_req,
            request_options={"idempotency_key": random_string()},
        )
        second_call_response = api.credits.create(
            credit_req,
            request_options={"idempotency_key": random_string()},
        )

        # then
        assert first_call_response != second_call_response

    def test_will_create_two_instances_if_no_idempotency_keys_are_used(self, api):
        # given
        credit_req = valid_credit_req()

        # when
        first_call_response = api.credits.create(credit_req)
        second_call_response = api.credits.create(credit_req)

        # then
        assert first_call_response != second_call_response

    def test_will_throw_exception_if_same_idempotency_key_is_used_for_two_different_create_requests(
        self, api
    ):
        # given
        idempotency_key = random_string()
        credit_req = valid_credit_req()

        # when
        api.credits.create(
            credit_req,
            request_options={"idempotency_key": idempotency_key},
        )
        credit_req["amount"] = "42"
        exception = self.assert_shift4_exception(
            api.credits.create,
            credit_req,
            request_options={"idempotency_key": idempotency_key},
        )

        # then
        assert exception.type == "invalid_request"
        assert exception.code is None
        assert (
            exception.message
            == "Idempotent key used for request with different parameters."
        )

    def test_will_throw_exception_if_same_idempotency_key_is_used_for_two_different_update_requests(
        self, api
    ):
        # given
        idempotency_key = random_string()
        credit_req = valid_credit_req()
        created = api.credits.create(credit_req)
        update_request_params = {
            "description": "updated description",
            "metadata": {"key": "updated value"},
        }

        # when
        api.credits.update(
            created["id"],
            update_request_params,
            request_options={"idempotency_key": idempotency_key},
        )
        update_request_params["description"] = "other description"
        exception = self.assert_shift4_exception(
            api.credits.update,
            created["id"],
            update_request_params,
            request_options={"idempotency_key": idempotency_key},
        )

        # then
        assert exception.type == "invalid_request"
        assert exception.code is None
        assert (
            exception.message
            == "Idempotent key used for request with different parameters."
        )
