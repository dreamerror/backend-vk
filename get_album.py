import os

import requests

TOKEN = os.getenv("TOKEN")

album_url = f"https://api.vk.com/method/photos.get?owner_id=-197700721&album_id=284717200&access_token={TOKEN}&v=5.131"
likes_url = "https://api.vk.com/method/likes.getList?owner_id=-197700721&type=photo&item_id={ITEM_ID}&access_token={TOKEN}&v=5.131"
users_url = "https://api.vk.com/method/users.get?user_ids={USER_ID}&access_token={TOKEN}&v=5.131"

items = requests.get(album_url).json()['response']['items']

for item in items:
    likes_count = requests.get(likes_url.format(ITEM_ID=item['id'], TOKEN=TOKEN)).json()['response']['count']
    user = requests.get(users_url.format(USER_ID=item['user_id'], TOKEN=TOKEN)).json()['response'][0]
    print(user['first_name'], user['last_name'], likes_count)
