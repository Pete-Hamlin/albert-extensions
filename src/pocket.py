"""
Extension for the Linux launcher project Albert(URL).
"""

import webbrowser
import requests
# from albertv0 import *

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Pocket'
__version__ = '1.0'
__trigger__ = 'pk '
__author__ = 'Pete Hamlin'

CONSUMER_KEY = '84233-56b6150ff55b2626c93016b1'
REDIRECT_URL = 'localhost'

def get_auth_code():
    payload = {
        'consumer_key': CONSUMER_KEY,
        'redirect_uri': REDIRECT_URL
    }
    response = requests.post('https://getpocket.com/v3/oauth/request', params=payload)
    code = response.text.replace('code=', '')
    return code

def request_auth(code):
    url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_url={}'.format(code, REDIRECT_URL)
    print(url)
    webbrowser.open(url)

def token_request(code):
    payload = {
        'consumer_key': CONSUMER_KEY,
        'code': code
    }
    response = requests.post('https://getpocket.com/v3/oauth/authorize', params=payload)
    if response.status_code == 403:
        print(response.headers)
        request_auth(code)
    return response.text


def get_token():
    code = get_auth_code()
    request_auth(code)
    confirm = input('Please confirm successful auth with application (Y/n):')
    if confirm == 'y' or confirm == 'Y':
        token = token_request(code)
        print(token)

get_token()
