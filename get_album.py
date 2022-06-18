import os

import requests

TOKEN = os.getenv("TOKEN")

album_url = f"https://api.vk.com/method/photos.get?owner_id=-197700721&album_id=284717200&access_token={TOKEN}&v=5.131"
likes_url = "https://api.vk.com/method/likes.getList?owner_id=-197700721&type=photo&item_id={ITEM_ID}&access_token={TOKEN}&v=5.131"
users_url = "https://api.vk.com/method/users.get?user_ids={USER_ID}&access_token={TOKEN}&v=5.131"


def get_photos_info():
    items = requests.get(album_url).json()['response']['items']
    result = list()

    for item in items:
        likes_count = requests.get(likes_url.format(ITEM_ID=item['id'], TOKEN=TOKEN)).json()['response']['count']
        user = requests.get(users_url.format(USER_ID=item['user_id'], TOKEN=TOKEN)).json()['response'][0]
        meme_url = item['sizes'][-1]['url']
        res = {
            'author': user['first_name'] + ' ' + user['last_name'],
            'group_id': -197700721,
            'likes': likes_count,
            'meme_url': meme_url,
            'meme_id': item['id']
        }
        yield res


def get_photos():
    for item in get_photos_info():
        yield item['author'], item['likes'], item['meme_url']


if __name__ == "__main__":
    for i in get_photos():
        print(i)
