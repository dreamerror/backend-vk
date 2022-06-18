import os
import json

import requests

from get_album import users_url

TOKEN = os.getenv('TOKEN')

meme_group_id = -95648824  # мемы про котов (по ржать)

memes_url = "https://api.vk.com/method/photos.get"


def get_memes(group_id: int, album_id: str, token: str, count: int, offset: int = 0):
    items = requests.get(memes_url, params={
        'owner_id': group_id,
        'album_id': album_id,
        'count': count,
        'access_token': token,
        'offset': offset,
        'extended': 1,
        'v': 5.131
    }).json()['response']['items']

    for item in items:
        user = requests.get(users_url.format(USER_ID=item['user_id'], TOKEN=TOKEN)).json()['response'][0]
        meme_url = item['sizes'][-1]['url']
        res = {
            'author': user['first_name'] + ' ' + user['last_name'],
            'group_id': group_id,
            'likes': item['likes']['count'],
            'meme_url': meme_url,
            'meme_id': item['id']
        }
        yield res


def save(count: int):
    res = {'memes': []}
    offset = 0
    while count:
        if count > 200:
            count -= 200
            cur_count = 200
        else:
            cur_count = count
            count = 0
        for item in get_memes(meme_group_id, 'wall', TOKEN, cur_count):
            res['memes'].append(item)
        offset += 200
    with open('memes.json', 'w') as memes:
        json.dump(res, memes)


save(1000)
