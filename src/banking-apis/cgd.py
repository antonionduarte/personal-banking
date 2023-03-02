import dotenv
import json
import requests

NORDIGEN_SECRET_KEY_ENV = "NORDIGEN_SECRET_KEY"
NORDIGEN_SECRET_ID_ENV = "NORDIGEN_SECRET_ID"

NORDIGEN_API = "https://ob.nordigen.com/api/v2/"
NORDIGEN_API_NEW_TOKEN = "token/new/"
NORDIGEN_API_COUNTRY_BANKS = "institutions/?country={country_code}"
NORDIGEN_API_USER_AGREEMENT = "agreements/enduser/"
NORDIGEN_API_REQUISITIONS = "requisitions/"
NORDIGEN_API_ACCOUNTS = "accounts/"

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

    url = NORDIGEN_API + NORDIGEN_API_REQUISITIONS

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_key}',
    }

    agreement_id = user_agreement['id']

    data = {
        'redirect': 'https://www.google.com',
        'institution_id': CAIXA_GERAL_DEPOSITOS_ID,
        'reference': REFERENCE_ID,
        'agreement': f'{agreement_id}',
        'user_language': 'EN',
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if not response.ok:
        raise Exception(f"Error: Error performing link requisition: {response.text}")

    return json.loads(response.text)


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


def request_link_accounts(user_link):
    access_key = request_access_token()['access']

    url = NORDIGEN_API + NORDIGEN_API_REQUISITIONS + f'{user_link["id"]}'

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_key}'
    }
    
    response = requests.get(url, headers=headers)

    if not response.ok:
        raise Exception(f"Error: Error performing bank list request: {response.text}")

    return json.loads(response.text)


def request_account_transactions(account_id):
    access_key = request_access_token()['access']

    url = NORDIGEN_API + NORDIGEN_API_ACCOUNTS + f'{account_id}/' + 'transactions/'

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_key}'
    }

    response = requests.get(url, headers=headers)
    
    if not response.ok:
        raise Exception(f"Error: Error requesting account transactions: {response.text}")

    return json.loads(response.text)


if __name__ == "__main__":
    """ Main function for testing """
    # access_token = api.request_access_token()
    # banks = api.request_bank_list()

    """ Gets the list of banks """
    # banks_str = json.dumps(banks)
    # file = open('banks.json', 'w')
    # file.write(banks_str)
    # file.close()
    # print(api.request_end_user_agreement())
    
    """ Gets a user agreement and saves it to a file """
    # user_agreement = request_end_user_agreement()
    # user_agreement_file = open('user_agreement.json', 'w')
    # user_agreement_file.write(json.dumps(user_agreement))
    # user_agreement_file.close()

    """ Imports user agreement from the file and uses it to request bank link """
    # with open('user_agreement.json', 'r') as user_agreement_file:
    #     user_agreement = json.loads(user_agreement_file.read())    
    #     bank_link = request_build_link(user_agreement)
    #     with open('user_bank_link.json', 'w') as user_bank_link_file:
    #         user_bank_link_file.write(json.dumps(bank_link))
    
    with open('user_bank_link.json', 'r') as user_bank_link:
        user_link = json.loads(user_bank_link.read())
        accounts = request_link_accounts(user_link)

        for account in accounts['accounts']:
            transactions = request_account_transactions(account)

            with open(f'{account}.json', 'w') as account_transactions:
                account_transactions.write(json.dumps(transactions))
