from . import random_email, random_string
from .data.cards import valid_card_req
from .data.plans import one_week_plan_req
from .data.subscriptions import subscription_req
from .testcase import TestCase


class TestSubscriptions(TestCase):
    def test_create_and_get(self, api):
        # given
        customer = api.customers.create(
            {"email": random_email(), "card": valid_card_req()}
        )
        plan = api.plans.create(one_week_plan_req())

        # when
        created = api.subscriptions.create(
            subscription_req(customerId=customer["id"], planId=plan["id"])
        )
        got = api.subscriptions.get(created["id"])

        # then
        assert created["id"] is not None
        assert created == got
        assert created["customerId"] == customer["id"]
        assert created["planId"] == plan["id"]

    def test_update(self, api):
        # given
        customer = api.customers.create(
            {"email": random_email(), "card": valid_card_req()}
        )
        plan = api.plans.create(one_week_plan_req())
        created = api.subscriptions.create(
            subscription_req(customerId=customer["id"], planId=plan["id"])
        )
        # when
        api.subscriptions.update(
            created["id"],
            {
                "shipping": {
                    "name": "Updated shipping",
                    "address": {
                        "line1": "Updated line1",
                        "line2": "Updated line2",
                        "zip": "Updated zip",
                        "city": "Updated city",
                        "state": "Updated state",
                        "country": "CH",
                    },
                }
            },
        )
        updated = api.subscriptions.get(created["id"])

        # then
        assert "shipping" not in created
        assert updated["id"] == created["id"]
        assert updated["planId"] == plan["id"]

        shipping = updated["shipping"]
        assert shipping["name"] == "Updated shipping"
        assert shipping["address"]["line1"] == "Updated line1"
        assert shipping["address"]["line2"] == "Updated line2"
        assert shipping["address"]["zip"] == "Updated zip"
        assert shipping["address"]["city"] == "Updated city"
        assert shipping["address"]["state"] == "Updated state"
        assert shipping["address"]["country"] == "CH"

    def test_will_not_create_duplicate_if_same_idempotency_key_is_used(self, api):
        # given
        idempotency_key = random_string()
        customer = api.customers.create(
            {"email": random_email(), "card": valid_card_req()}
        )
        plan = api.plans.create(one_week_plan_req())
        subscription_request = subscription_req(
            customerId=customer["id"], planId=plan["id"]
        )

        # when
        first_call_response = api.subscriptions.create(
            subscription_request,
            request_options={"idempotency_key": idempotency_key},
        )
        second_call_response = api.subscriptions.create(
            subscription_request,
            request_options={"idempotency_key": idempotency_key},
        )

        # then
        assert first_call_response == second_call_response

    def test_will_create_two_instances_if_different_idempotency_keys_are_used(
        self, api
    ):
        # given
        customer = api.customers.create(
            {"email": random_email(), "card": valid_card_req()}
        )
        plan = api.plans.create(one_week_plan_req())
        subscription_request = subscription_req(
            customerId=customer["id"], planId=plan["id"]
        )

        # when
        first_call_response = api.subscriptions.create(
            subscription_request,
            request_options={"idempotency_key": random_string()},
        )
        second_call_response = api.subscriptions.create(
            subscription_request,
            request_options={"idempotency_key": random_string()},
        )

        # then
        assert first_call_response != second_call_response

    def test_will_create_two_instances_if_no_idempotency_keys_are_used(self, api):
        # given
        customer = api.customers.create(
            {"email": random_email(), "card": valid_card_req()}
        )
        plan = api.plans.create(one_week_plan_req())
        subscription_request = subscription_req(
            customerId=customer["id"], planId=plan["id"]
        )

        # when
        first_call_response = api.subscriptions.create(subscription_request)
        second_call_response = api.subscriptions.create(subscription_request)

        # then
        assert first_call_response != second_call_response

    def test_will_throw_exception_if_same_idempotency_key_is_used_for_two_different_create_requests(
        self, api
    ):
        # given
        idempotency_key = random_string()
        customer = api.customers.create(
            {"email": random_email(), "card": valid_card_req()}
        )
        plan = api.plans.create(one_week_plan_req())
        subscription_request = subscription_req(
            customerId=customer["id"], planId=plan["id"]
        )

        # when
        api.subscriptions.create(
            subscription_request,
            request_options={"idempotency_key": idempotency_key},
        )
        subscription_request["planId"] = "42"
        exception = self.assert_shift4_exception(
            api.subscriptions.create,
            subscription_request,
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
        customer = api.customers.create(
            {"email": random_email(), "card": valid_card_req()}
        )
        plan = api.plans.create(one_week_plan_req())
        subscription_request = subscription_req(
            customerId=customer["id"], planId=plan["id"]
        )
        created = api.subscriptions.create(subscription_request)

        idempotency_key = random_string()
        update_request_params = {
            "shipping": {
                "name": "Updated shipping",
                "address": {
                    "line1": "Updated line1",
                    "line2": "Updated line2",
                    "zip": "Updated zip",
                    "city": "Updated city",
                    "state": "Updated state",
                    "country": "CH",
                },
            }
        }

        # when
        api.subscriptions.update(
            created["id"],
            update_request_params,
            request_options={"idempotency_key": idempotency_key},
        )
        update_request_params["shipping"]["name"] = "different name"
        exception = self.assert_shift4_exception(
            api.subscriptions.update,
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


def find_charge_success(response):
    for event in response["list"]:
        if event["type"] == "CHARGE_SUCCEEDED":
            return event
