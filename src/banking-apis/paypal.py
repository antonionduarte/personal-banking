import dotenv
import json
import requests


PAYPAL_API = 'https://api-m.sandbox.paypal.com/v1/'
PAYPAL_AUTHENTICATION = 'oauth2/token'
PAYPAL_BALANCES = "reporting/balances?currency_code=ALL&include_crypto_currencies=false"


PAYPAL_CLIENT_ID_ENV = 'PAYPAL_CLIENT_ID'
PAYPAL_SECRET_ENV = 'PAYPAL_SECRET'


paypal_client_id = dotenv.get_key(dotenv_path=".env", key_to_get=PAYPAL_CLIENT_ID_ENV) or ""
paypal_secret = dotenv.get_key(dotenv_path=".env", key_to_get=PAYPAL_SECRET_ENV) or ""


def request_account_transactions():
    auth = request_authentication()

    pass


def request_account_balance():
    url = PAYPAL_API + PAYPAL_BALANCES
    auth = request_authentication()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth["access_token"]}'
    }

    response = requests.get(url, headers=headers)

    # TODO: Throw except

    return json.loads(response.text)


def request_authentication():
    url = PAYPAL_API + PAYPAL_AUTHENTICATION

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }    

    data = 'grant_type=client_credentials'
    auth = (paypal_client_id, paypal_secret)

    response = requests.post(url, headers=headers, data=data, auth=auth)

    # TODO: Throw except

    return json.loads(response.text)


if __name__ == "__main__":
    bal = request_account_balance()

    print(bal)

