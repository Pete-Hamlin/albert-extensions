import json
import webbrowser
from os import path
from time import sleep

import requests

CONSUMER_KEY = '84233-56b6150ff55b2626c93016b1'
REDIRECT_URL = 'localhost'
TOKEN_PATH = '{}/token.conf'.format(path.dirname(__file__))
HEADERS = {
    'Content-Type': 'application/json',
    'X-Accept': 'application/json'
}

CONFIG = {
    'state': 'all',
    'detail_type': 'complete'
}

def get_auth_code():
    """Gets initial auth code

    Returns:
        String -- Auth code from Pockt server
    """

    payload = {
        'consumer_key': CONSUMER_KEY,
        'redirect_uri': REDIRECT_URL
    }
    response = requests.post(
        'https://getpocket.com/v3/oauth/request',
        data=json.dumps(payload),
        headers=HEADERS
    )
    code = response.json()
    return code['code']


def request_auth(code):
    """Goes out and requests user authentication page

    Arguments:
        code {string} -- Auth code provided by Pocket servers
    """

    url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_url={}'.format(
        code, REDIRECT_URL)
    webbrowser.open(url)


def token_request(code):
    """Requests pocket server for access token

    Arguments:
        code {String} -- Auth code provided by Pocket server

    Returns:
        String -- Access token provided by Pocket server
    """

    payload = {
        'consumer_key': CONSUMER_KEY,
        'code': code
    }
    response = requests.post(
        'https://getpocket.com/v3/oauth/authorize',
        params=payload,
        headers=HEADERS
    )
    if response.status_code == 403:
        print(response.headers)
        request_auth(code)
    else:
        token = response.json()
        return token['access_token']


def authenticate():
    """Wrapper function for the necessary requests to be made to the Pocket servers. gets token and writes it to local config file.
    """

    code = get_auth_code()
    print('Redirecting you to authorization page within your browser - If you have done this before the page will likely error with an invalid URL error. This is fine for you to proceed with.\n')
    request_auth(code)
    sleep(10)
    token = token_request(code)
    with open(TOKEN_PATH, 'w') as file:
        file.write(token)


def get_list():
    with open(TOKEN_PATH, 'r') as file:
        token = file.readline()
    params = {
        'consumer_key': CONSUMER_KEY,
        'access_token': token,
        'detailType': CONFIG['detail_type'],
        'state': CONFIG['state']
    }
    response = requests.post('https://getpocket.com/v3/get', params=params)
    if response.status_code == 200:
        result_list = response.json()
        return result_list['list']