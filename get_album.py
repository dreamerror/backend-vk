import json
import os

import requests

TOKEN = os.getenv("TOKEN")

album_url = "https://api.vk.com/method/photos.get"
likes_url = "https://api.vk.com/method/likes.getList?owner_id=-197700721&type=photo&item_id={ITEM_ID}&access_token={TOKEN}&v=5.131"
users_url = "https://api.vk.com/method/users.get?user_ids={USER_ID}&access_token={TOKEN}&v=5.131"

vezdekod_group_id = -197700721


def get_photos_info(group_id: int, album_id: int, token: str):
    items = requests.get(album_url, params={
        'owner_id': group_id,
        'album_id': album_id,
        'access_token': token,
        'v': 5.131
    }).json()['response']['items']

    for item in items:
        likes_count = requests.get(likes_url.format(ITEM_ID=item['id'], TOKEN=TOKEN)).json()['response']['count']
        user = requests.get(users_url.format(USER_ID=item['user_id'], TOKEN=TOKEN)).json()['response'][0]
        meme_url = item['sizes'][-1]['url']
        res = {
            'author': user['first_name'] + ' ' + user['last_name'],
            'group_id': group_id,
            'likes': likes_count,
            'meme_url': meme_url,
            'meme_id': item['id']
        }
        yield res


def get_photos():
    for item in get_photos_info(vezdekod_group_id, 284717200, TOKEN):
        yield item['author'], item['likes'], item['meme_url']


def save():
    res = {'memes': []}
    for item in get_photos_info(vezdekod_group_id, 284717200, TOKEN):
        res['memes'].append(item)
    with open('vezdekod.json', 'w') as vezde:
        json.dump(res, vezde)


if __name__ == "__main__":
    save()
    # for item in get_photos():
    #     #     print(item)

