import requests
import json


API_URL = "https://api.soundcloud.com/"
APIV2_URL = "https://api-v2.soundcloud.com/"
WEB_URL = "https://www.soundcloud.com/"

EMBED_URL = "https://soundcloud.com/oembed"

def get_track(track_url):
    params = {
        'format': 'json',
        'url': track_url
    }

    response = requests.get(EMBED_URL, params=params)


    if '200' in str(response):
        print('OK')
        response_json = response.json()
        html = response_json['html']
    else:
        print('NOT OK')
        html = ''


    return html

# print(get_track('https://soundcloud.com/suzuki-growhouse/lcd-warhols'))

# print(get_track('efefefefef'))