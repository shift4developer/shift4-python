Python library for Shift4 API
===================================
[![Build](https://github.com/shift4developer/shift4-python/actions/workflows/build.yml/badge.svg)](https://github.com/shift4developer/shift4-python/actions/workflows/build.yml)

Installation
------------

```
pip install shift4
```

Quick start
-----------

```python
import shift4 as shift4

shift4.secret_key = 'pk_test_my_secret_key'

try:
    customer = shift4.customers.create({
        'email': 'user@example.com',
        'description': 'User description'
    })
    print("Created customer:", customer)
    card = shift4.cards.create(customer['id'], {
        'number': '4242424242424242',
        'expMonth': '12',
        'expYear': '2023',
        'cvc': '123',
        'cardholderName': 'John Smith'
    })
    print("Created card:", card)
    charge = shift4.charges.create({
      'amount': 1000,
      'currency': 'EUR',
      'customerId': card['customerId']
    })
    print("Created charge:", charge)
except shift4.Shift4Exception as e:
  print(e)
```

API reference
-------------

Please refer to detailed API docs (linked) for all available fields

- charges
  - [create(params)](https://dev.shift4.com/docs/api#charge-create)
  - [get(charge_id)](https://dev.shift4.com/docs/api#charge-retrieve)
  - [update(charge_id, params)](https://dev.shift4.com/docs/api#charge-update)
  - [capture(charge_id)](https://dev.shift4.com/docs/api#charge-capture)
  - [refund(charge_id, [params])](https://dev.shift4.com/docs/api#charge-capture)
  - [list([params])](https://dev.shift4.com/docs/api#charge-list)
- customers
  - [create(params)](https://dev.shift4.com/docs/api#customer-create)
  - [get(customer_id)](https://dev.shift4.com/docs/api#customer-retrieve)
  - [update(customer_id, params)](https://dev.shift4.com/docs/api#customer-update)
  - [delete(customer_id)](https://dev.shift4.com/docs/api#customer-delete)
  - [list([params])](https://dev.shift4.com/docs/api#customer-list)
- cards
  - [create(customer_id, params)](https://dev.shift4.com/docs/api#card-create)
  - [get(customer_id, card_id)](https://dev.shift4.com/docs/api#card-retrieve)
  - [update(customer_id, card_id, params)](https://dev.shift4.com/docs/api#card-update)
  - [delete(customer_id, card_id)](https://dev.shift4.com/docs/api#card-delete)
  - [list(customer_id, [params])](https://dev.shift4.com/docs/api#card-list)
- subscriptions
  - [create(params)](https://dev.shift4.com/docs/api#subscription-create)
  - [get(subscription_id)](https://dev.shift4.com/docs/api#subscription-retrieve)
  - [update(subscription_id, params)](https://dev.shift4.com/docs/api#subscription-update)
  - [cancel(subscription_id, [params])](https://dev.shift4.com/docs/api#subscription-cancel)
  - [list([params])](https://dev.shift4.com/docs/api#subscription-list)
- plans
  - [create(params)](https://dev.shift4.com/docs/api#plan-create)
  - [get(plan_id)](https://dev.shift4.com/docs/api#plan-retrieve)
  - [update(plan_id, params)](https://dev.shift4.com/docs/api#plan-update)
  - [delete(plan_id)](https://dev.shift4.com/docs/api#plan-delete)
  - [list([params])](https://dev.shift4.com/docs/api#plan-list)
- events
  - [get(event_id)](https://dev.shift4.com/docs/api#event-retrieve)
  - [list([params])](https://dev.shift4.com/docs/api#event-list)
- tokens
  - [create(params)](https://dev.shift4.com/docs/api#token-create)
  - [get(token_id)](https://dev.shift4.com/docs/api#token-retrieve)
- blacklist
  - [create(params)](https://dev.shift4.com/docs/api#blacklist-rule-create)
  - [get(blacklist_rule_id)](https://dev.shift4.com/docs/api#blacklist-rule-retrieve)
  - [delete(blacklist_rule_id)](https://dev.shift4.com/docs/api#blacklist-rule-delete)
  - [list([params])](https://dev.shift4.com/docs/api#blacklist-rule-list)
- checkoutRequest
  - [sign(checkoutRequestObjectOrJson)](https://dev.shift4.com/docs/api#checkout-request-sign)
- credits
  - [create(params)](https://dev.shift4.com/docs/api#credit-create)
  - [get(credit_id)](https://dev.shift4.com/docs/api#credit-retrieve)
  - [update(credit_id, params)](https://dev.shift4.com/docs/api#credit-update)
  - [list([params])](https://dev.shift4.com/docs/api#credit-list)
- disputes
  - [get(dispute_id)](https://dev.shift4.com/docs/api#dispute-retrieve)
  - [update(dispute_id, params)](https://dev.shift4.com/docs/api#dispute-update)
  - [close(dispute_id)](https://dev.shift4.com/docs/api#dispute-close)
  - [list([params])](https://dev.shift4.com/docs/api#dispute-list)
- fileUploads
  - [upload(content, params)](https://dev.shift4.com/docs/api#file-upload-create)
  - [get(file_upload_id)](https://dev.shift4.com/docs/api#file-upload-retrieve)
  - [list([params])](https://dev.shift4.com/docs/api#file-upload-list)
- fraudWarnings
  - [get(fraud_warning_id)](https://dev.shift4.com/docs/api#fraud-warning-retrieve)
  - [list([params])](https://dev.shift4.com/docs/api#fraud-warning-list)
- paymentMethods
  - [create(params)](https://dev.shift4.com/docs/api#payment-method-create)
  - [retrieve(payment_method_id)](https://dev.shift4.com/docs/api#payment-method-retrieve)
  - [delete(payment_method_id)](https://dev.shift4.com/docs/api#payment-method-delete)
  - [list([params])](https://dev.shift4.com/docs/api#payment-methods-list)


For further information, please refer to our official documentation
at [https://dev.shift4.com/docs](https://dev.shift4.com/docs).


Developing
----------

Optionally setup a virtual environment
```sh
python -m venv ./venv --clear
source ./venv/bin/activate 
```

Install the package dependencies:
```sh
pip install -r requirements.txt -r test_requirements.txt
```

To connect to different backend:

```python
import shift4 as api

api.secret_key = 'pk_test_my_secret_key'
api.api_url = 'https://api.myshift4env.com'
api.uploads_url = 'https://uploads.myshift4env.com'
```

To run tests:

```sh
SECRET_KEY=pk_test_my_secret_key pytest tests
```

Format the package files using `black`:

```sh
black setup.py shift4/ tests/
```
