#!/usr/bin/env python3

import requests
import json
from bs4 import BeautifulSoup

banner = '''
==================================
RTBF Auvio - Download Video Helper
==================================
Generate direct video link from	video ID.

Usage:
Find the video ID at the end of the original URL, e.g. for the following URL, video id is 2409087:
https://www.rtbf.be/auvio/detail_fit-tonic?id=2409087

'''

def ask_vid():
    vid = None
    isinvalid = True
    while isinvalid:
        vid = input('Video ID: ')

        try:
            isinvalid = not isinstance(int(vid), int) 
        except ValueError:
            print('This should only contain numbers, try again.')
            print()

    return vid

def get_video_link(vid):
    print('[*] Fetching RTBF Auvio website for video %s' % vid)

    p = {'id': vid}
    r = requests.get('https://www.rtbf.be/auvio/embed/media', params=p)
    
    # Verify 200 OK
    if r.status_code != requests.codes.ok:
        print('[-] HTTP response status unexpected: %s' % r.status_code)
        return None

    # Verify content exists
    if 'Ce contenu n\'est plus disponible' in r.text:
        print('[-] This video ID does not exists')
        return None

    # Parse response for video link
    soup = BeautifulSoup(r.text, 'html5lib')
    
    try:
        j = json.loads(soup.find(id="js-embed-player")['data-media'])
        return j['url']
    except:
        print('[-] Cannot find URL')
        return None

#############################################################################

# Welcome user with banner
print(banner)

# Ask vid, find and display link
vid = ask_vid()
print()

link = get_video_link(vid)
if link is not None:
    print('[+] URL found: %s' % link)
