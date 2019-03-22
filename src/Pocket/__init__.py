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

    item = Item(id=__prettyname__,
                icon=__icon__,
                text="(Re)Authenticate",
                subtext="Attempt to (re)generate auth token from Pocket API",
                completion=__trigger__ + 'Hellooohooo!',
                urgency=ItemBase.Alert,
                actions=[
                    FuncAction(text="FuncAction",
                               callable=lambda: authenticate()),
                    UrlAction(text="UrlAction",
                               url="https://www.google.de"),
                    ProcAction(text="ProcAction",
                               commandline=["espeak", "hello"],
                               cwd="~"),  # optional
                    TermAction(text="TermAction",
                               commandline=["sleep", "5"],
                               cwd="~/git")  # optional
                ])
    items.append(item)
    sleep(0.2)
    item_list = get_list()
    for key, item in item_list.items():
        if query.string in item['given_url']:
            info(item)
            # items.append(append_item(item))
    return items

def append_item(value):
    actions = [UrlAction("Open in browser", value['given_url'])]
    subtext = "{}...".format(value['given_title'][:30])
    if value['top_image_url']
    if 'authors' in value:
        for key, author in value['authors'].items():
            subtext = subtext + " | {}".format(author['name'])
    if 'tags' in value:
        for key, tag in value['tags'].items():
            subtext = subtext + " | {}".format(tag['tag'])
    item = Item(uid=__prettyname__,
                icon=value['top_image_url'] if value['top_image_url'] else __icon__,
                text=value['given_url'],
                subtext=subtext,
                actions=actions
               )
    return item

