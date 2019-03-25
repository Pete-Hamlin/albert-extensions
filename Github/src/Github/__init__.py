"""
Allows querying of the Github API to view/manipulate chosen repositories. Requires Oauth2 authentication in order to work.
"""

import json

import requests

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Github'
__version__ = '1.0'
__trigger__ = 'github '
__author__ = 'Pete Hamlin'
__icon__ = '{}/icon.svg'.format(path.dirname(__file__))

