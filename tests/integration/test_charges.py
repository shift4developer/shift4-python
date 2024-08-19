from . import random_string
from .data.charges import valid_charge_req
from .data.customers import valid_customer_req
from .testcase import TestCase


class TestCharges(TestCase):
    def test_create_and_get(self, api):
        # given
        charge_req = valid_charge_req()

        # when
        created = api.charges.create(charge_req)
        got = api.charges.get(created["id"])

        # then
        assert created == got
        assert created["amount"] == charge_req["amount"]
        assert created["currency"] == charge_req["currency"]
        self.assert_card_matches_request(created["card"], charge_req["card"])

    def test_update(self, api):
        # given
        charge_req = valid_charge_req()
        created = api.charges.create(charge_req)

        # when
        updated = api.charges.update(
            created["id"],
            {
                "description": "updated description",
                "metadata": {"key": "updated value"},
            },
        )
        # then
        assert created["description"] == charge_req["description"]
        assert updated["description"] == "updated description"

        assert created["metadata"]["key"] == charge_req["metadata"]["key"]
        assert updated["metadata"]["key"] == "updated value"

        assert updated["amount"] == charge_req["amount"]
        assert updated["currency"] == charge_req["currency"]
        self.assert_card_matches_request(updated["card"], charge_req["card"])

    def test_capture(self, api):
        # given
        charge_req = valid_charge_req(captured=False)
        created = api.charges.create(charge_req)

        # when
        captured = api.charges.capture(created["id"])

        # then
        assert not created["captured"]
        assert captured["captured"]

    def test_refund(self, api):
        # given
        charge_req = valid_charge_req()
        created = api.charges.create(charge_req)

        # when
        refunded = api.charges.refund(created["id"])

        # then
        assert not created["refunded"]
        assert refunded["refunded"]

    def test_list(self, api):
        # given
        customer = api.customers.create(valid_customer_req())
        charge_req = valid_charge_req(customerId=customer["id"])
        charge1 = api.charges.create(charge_req)
        charge2 = api.charges.create(charge_req)
        charge3 = api.charges.create(charge_req)

        # when
        all_charges = api.charges.list({"customerId": customer["id"]})
        charges_after_last_id = api.charges.list(
            {"customerId": customer["id"], "startingAfterId": charge3["id"]}
        )

        # then
        self.assert_list_response_contains_exactly_by_id(
            all_charges, [charge3, charge2, charge1]
        )
        self.assert_list_response_contains_exactly_by_id(
            charges_after_last_id, [charge2, charge1]
        )

    def test_will_not_create_duplicate_if_same_idempotency_key_is_used(self, api):
        # given
        idempotency_key = random_string()
        charge_req = valid_charge_req()

        # when
        first_call_response = api.charges.create(
            charge_req,
            request_options={"idempotency_key": idempotency_key},
        )
        second_call_response = api.charges.create(
            charge_req,
            request_options={"idempotency_key": idempotency_key},
        )

        # then
        assert first_call_response == second_call_response

    def test_will_create_two_instances_if_different_idempotency_keys_are_used(
        self, api
    ):
        # given
        charge_req = valid_charge_req()

        # when
        first_call_response = api.charges.create(
            charge_req,
            request_options={"idempotency_key": random_string()},
        )
        second_call_response = api.charges.create(
            charge_req,
            request_options={"idempotency_key": random_string()},
        )

        # then
        assert first_call_response != second_call_response

    def test_will_create_two_instances_if_no_idempotency_keys_are_used(self, api):
        # given
        charge_req = valid_charge_req()

        # when
        first_call_response = api.charges.create(charge_req)
        second_call_response = api.charges.create(charge_req)

        # then
        assert first_call_response != second_call_response

    def test_will_throw_exception_if_same_idempotency_key_is_used_for_two_different_create_requests(
        self, api
    ):
        # given
        idempotency_key = random_string()
        charge_req = valid_charge_req()

        # when
        api.charges.create(
            charge_req,
            request_options={"idempotency_key": idempotency_key},
        )
        charge_req["amount"] = "42"
        exception = self.assert_shift4_exception(
            api.charges.create,
            charge_req,
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
        charge_req = valid_charge_req()
        created = api.charges.create(charge_req)
        update_request_params = {
            "description": "updated description",
            "metadata": {"key": "updated value"},
        }

        # when
        api.charges.update(
            created["id"],
            update_request_params,
            request_options={"idempotency_key": idempotency_key},
        )
        update_request_params["description"] = "other description"
        exception = self.assert_shift4_exception(
            api.charges.update,
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
