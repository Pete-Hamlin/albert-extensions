"""
Allows searching of Pocket reading list via the launcher. You will first be required to run the authenticate action before you can query your list.
"""

import webbrowser
import json


from os import path
from time import sleep

import requests
from albertv0 import *
from .pocket_api import *

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Pocket'
__version__ = '1.0'
__trigger__ = 'pk '
__author__ = 'Pete Hamlin'
__icon__ = '{}/icon.svg'.format(path.dirname(__file__))

def handleQuery(query):
    if not query.isTriggered:
        return

    items = []
    # if not query.isValid:
    #     return

    sleep(0.2)
    item_list = get_list()
    for key, item in item_list.items():
        if query.string in item['given_url']:
            debug('Matched URL {}'.format(item['given_url']))
            items.append(append_item(item))
            continue
        # Match authors
        if 'authors' in item:
            for key, author in item['authors'].items():
                if query.string in author['name']:
                    debug('Matched author {}'.format(author['name']))
                    items.append(append_item(item))
                    continue
        # Match tags
        if 'tags' in item:
            for key, tag in item['tags'].items():
                if query.string in tag['tag']:
                    debug('Matched tag {}'.format(tag['tag']))
                    items.append(append_item(item))
                    continue

    item = Item(id=__prettyname__,
                icon=__icon__,
                text="(Re)Authenticate",
                subtext="Attempt to (re)generate auth token from Pocket API",
                completion=__trigger__,
                urgency=ItemBase.Alert,
                actions=[
                    FuncAction(text="FuncAction",
                               callable=lambda: authenticate())
                                ])
    items.append(item)
    return items

def append_item(value):
    actions = [UrlAction("Open in browser", value['given_url']),
               ClipAction("Copy to clipboard", value['given_url'])]
    subtext = "{}...".format(value['given_url'][:30])
    if 'given_title' in value and value['given_title']:
        text = value['given_title'][:60]
    else:
        text = value['given_url'][:60]
    if 'authors' in value:
        for key, author in value['authors'].items():
            subtext = subtext + " | {}".format(author['name'])
    if 'tags' in value:
        for key, tag in value['tags'].items():
            subtext = subtext + " | {}".format(tag['tag'])
    item = Item(id=__prettyname__,
                text=text,
                subtext=subtext,
                actions=actions
               )
    return item

