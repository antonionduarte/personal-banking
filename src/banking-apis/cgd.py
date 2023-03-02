import dotenv
import json
import requests

NORDIGEN_SECRET_KEY_ENV = "NORDIGEN_SECRET_KEY"
NORDIGEN_SECRET_ID_ENV = "NORDIGEN_SECRET_ID"

NORDIGEN_API = "https://ob.nordigen.com/api/v2/"
NORDIGEN_API_NEW_TOKEN = "token/new/"
NORDIGEN_API_COUNTRY_BANKS = "institutions/?country={country_code}"
NORDIGEN_API_USER_AGREEMENT = "agreements/enduser/"

NORDIGEN_BANK_ID = ""
NORDIGEN_COUNTRY_CODE_PORTUGAL = "pt"

REFERENCE_ID = "123456"

CAIXA_GERAL_DEPOSITOS_ID = "CAIXA_GERAL_DEPOSITOS_CGDIPTPL"

nordigen_key = dotenv.get_key(dotenv_path=".env", key_to_get=NORDIGEN_SECRET_KEY_ENV)
nordigen_id = dotenv.get_key(dotenv_path=".env", key_to_get=NORDIGEN_SECRET_ID_ENV)

"""

TODO:
    - Should I request a new access token in every request? ... maybe?
    - Throw exceptions when the response code isn't 200. We NEED to do this.

"""

def request_access_token():
    url = NORDIGEN_API + NORDIGEN_API_NEW_TOKEN

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        'secret_id': nordigen_id,
        'secret_key': nordigen_key
    }

    json_data = json.dumps(data)

    response = requests.post(url, headers=headers, data=json_data)

    if not response.ok:
        raise Exception(f"ERROR: Error performing CGDApi access token request: {response.text}")

    return json.loads(response.text)


def request_end_user_agreement():
    access_key = request_access_token()['access']

    url = NORDIGEN_API + NORDIGEN_API_USER_AGREEMENT

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_key}',
    }

    data = {
        'institution_id': CAIXA_GERAL_DEPOSITOS_ID,
        'max_historical_days': '90',
        'access_valid_for_days': '90',
        'access_scope': ['balances', 'details', 'transactions']
    }

    json_data = json.dumps(data)

    response = requests.post(url, headers=headers, data=json_data)

    if not response.ok:
        raise Exception(f"ERROR: Error performing CGDApi user agreement: {response.text}")

    return json.loads(response.text)


def request_build_link(user_agreement):
    access_key = request_access_token()['access']

    url = ""

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_key}',
    }

    # TODO: Complete this.

    data = {
        'redirect': 'http://www.google.com',
        'institution_id': CAIXA_GERAL_DEPOSITOS_ID,
        'reference': REFERENCE_ID,
        'agreement': {user_agreement},
        'user_language': 'EN'
    }

    pass


def request_transaction_history():
    access_key = request_access_token()

    pass


def request_bank_list():
    access_key = request_access_token()['access']

    url = NORDIGEN_API + NORDIGEN_API_COUNTRY_BANKS.format(country_code=NORDIGEN_COUNTRY_CODE_PORTUGAL)

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_key}'
    }

    response = requests.get(url, headers=headers)

    if not response.ok:
        raise Exception(f"Error: Error performing CGDApi request bank list: {response.text}")

    return json.loads(response.text)


def request_account_balance():
    access_key = request_access_token()

    pass


if __name__ == "__main__":
    """ Main function for testing """
    # access_token = api.request_access_token()
    # banks = api.request_bank_list()

    # banks_str = json.dumps(banks)
    # file = open('banks.json', 'w')
    # file.write(banks_str)
    # file.close()
    # print(api.request_end_user_agreement())
    print(request_end_user_agreement())
