from shift4.request_options import RequestOptions
from . import random_string
from .data.plans import one_week_plan_req
from .testcase import TestCase


class TestPlans(TestCase):
    def test_create_and_get(self, api):
        # given
        plan_req = one_week_plan_req()
        # when
        created = api.plans.create(plan_req)
        got = api.plans.get(created["id"])
        # then
        assert got["id"] == created["id"]
        assert got["amount"] == plan_req["amount"]
        assert got["currency"] == plan_req["currency"]
        assert got["interval"] == plan_req["interval"]
        assert got["name"] == plan_req["name"]

    def test_update(self, api):
        # given
        plan_req = one_week_plan_req()
        created = api.plans.create(plan_req)
        # when
        updated = api.plans.update(
            created["id"], {"amount": 222, "currency": "PLN", "name": "Updated plan"}
        )
        # then
        assert updated["id"] == created["id"]
        assert updated["interval"] == plan_req["interval"]
        assert updated["amount"] == 222
        assert updated["currency"] == "PLN"
        assert updated["name"] == "Updated plan"

    def test_delete(self, api):
        # given
        plan_req = one_week_plan_req()
        created = api.plans.create(plan_req)
        # when
        api.plans.delete(created["id"])
        updated = api.plans.get(created["id"])
        # then
        assert "deleted" not in created
        assert updated["deleted"]

    def test_list(self, api):
        # given
        plan1 = api.plans.create(one_week_plan_req())
        plan2 = api.plans.create(one_week_plan_req())
        deleted_plan = api.plans.create(one_week_plan_req())
        api.plans.delete(deleted_plan["id"])
        # when
        all_plans = api.plans.list({"limit": 100})
        deleted_plans = api.plans.list({"limit": 100, "deleted": True})

        # then
        self.assert_list_response_contains_in_any_order_by_id(all_plans, [plan2, plan1])
        self.assert_list_response_contains_in_any_order_by_id(
            deleted_plans, [deleted_plan]
        )

    def test_will_not_create_duplicate_if_same_idempotency_key_is_used(self, api):
        # given
        request_options = RequestOptions()
        request_options.set_idempotency_key(random_string())
        plan_req = one_week_plan_req()

        # when
        first_call_response = api.plans.create(
            plan_req, request_options=request_options
        )
        second_call_response = api.plans.create(
            plan_req, request_options=request_options
        )

        # then
        assert first_call_response == second_call_response

    def test_will_create_two_instances_if_different_idempotency_keys_are_used(
        self, api
    ):
        # given
        request_options = RequestOptions()
        request_options.set_idempotency_key(random_string())
        other_request_options = RequestOptions()
        other_request_options.set_idempotency_key(random_string())
        plan_req = one_week_plan_req()

        # when
        first_call_response = api.plans.create(
            plan_req, request_options=request_options
        )
        second_call_response = api.plans.create(
            plan_req, request_options=other_request_options
        )

        # then
        assert first_call_response != second_call_response

    def test_will_create_two_instances_if_no_idempotency_keys_are_used(self, api):
        # given
        plan_req = one_week_plan_req()

        # when
        first_call_response = api.plans.create(plan_req)
        second_call_response = api.plans.create(plan_req)

        # then
        assert first_call_response != second_call_response

    def test_will_throw_exception_if_same_idempotency_key_is_used_for_two_different_create_requests(
        self, api
    ):
        # given
        request_options = RequestOptions()
        request_options.set_idempotency_key(random_string())
        plan_req = one_week_plan_req()

        # when
        api.plans.create(plan_req, request_options=request_options)
        plan_req["amount"] = "42"
        exception = self.assert_shift4_exception(
            api.plans.create, plan_req, request_options=request_options
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
        request_options = RequestOptions()
        request_options.set_idempotency_key(random_string())
        plan_req = one_week_plan_req()
        created = api.plans.create(plan_req)
        update_request_params = {
            "amount": 42,
            "currency": "PLN",
            "name": "Updated plan",
        }

        # when
        api.plans.update(
            created["id"], update_request_params, request_options=request_options
        )
        update_request_params["amount"] = 58
        exception = self.assert_shift4_exception(
            api.plans.update,
            created["id"],
            update_request_params,
            request_options=request_options,
        )

        # then
        assert exception.type == "invalid_request"
        assert exception.code is None
        assert (
            exception.message
            == "Idempotent key used for request with different parameters."
        )
