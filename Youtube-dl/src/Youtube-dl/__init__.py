# -*- coding: utf-8 -*-

"""Query and download YouTube videos"""

import json
import re
import time
from os import path
from shutil import which
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from albertv0 import *

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Youtube-dl'
__version__ = '1.0'
__trigger__ = 'ytdl '
__author__ = 'Pete Hamlin'
__dependencies__ = ['youtube-dl']
__icon__ = iconLookup('youtube')  # path.dirname(__file__) + '/icons/YouTube.png'

if which("youtube-dl") is None:
    raise Exception("'youtube-dl' is not in $PATH.")

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/62.0.3202.62 Safari/537.36'
    )
}

re_videos = re.compile(r"^\s*window\[\"ytInitialData\"\] = (.*);$", re.MULTILINE)

def handleQuery(query):
    if query.isTriggered and query.string.strip():

        # avoid rate limiting
        time.sleep(0.2)
        if not query.isValid:
            return

        url_values = urlencode({'search_query': query.string.strip()})
        url = 'https://www.youtube.com/results?%s' % url_values
        req = Request(url=url, headers=HEADERS)
        with urlopen(req) as response:
            match = re.search(re_videos, response.read().decode())
            if match:
                results = json.loads(match.group(1))
                results = results['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
                items = []
                for result in results:
                    for type, data in result.items():
                        try:
                            if type == 'videoRenderer':
                                uid = data['videoId']
                                subtext = 'Video'
                                if 'lengthText' in data:
                                    subtext = subtext + " | %s" % data['lengthText']['simpleText'].strip()
                                if 'shortViewCountText' in data:
                                    subtext = subtext + " | %s" % data['shortViewCountText']['simpleText'].strip()
                                if 'publishedTimeText' in data:
                                    subtext = subtext + " | %s" % data['publishedTimeText']['simpleText'].strip()
                                command = 'youtube-dl --extract-audio --audio-format mp3 %s' % uid
                                actions = [ 
                                    TermAction("Command", ['echo {}'.format(command)]),
                                    TermAction("Download mp3", ['youtube-dl --extract-audio --audio-format mp3 {}'.format(uid)]), 
                                    TermAction("Download Video", ['youtube-dl {}'.format(uid)])
                                    ]
                                # actions = [UrlAction('Watch on Youtube', 'https://youtube.com/watch?v=%s' % uid)]
                            else:
                                continue
                        except Exception as e:
                            critical(e)
                            critical(json.dumps(result, indent=4))

                        item = Item(uid=__prettyname__,
                                    icon=data['thumbnail']['thumbnails'][0]['url'].split('?', 1)[0] if data['thumbnail']['thumbnails'] else __icon__,
                                    text=data['title']['simpleText'],
                                    subtext=subtext,
                                    completion=query.rawString,
                                    actions=actions
                                )
                        items.append(item)
                return items
