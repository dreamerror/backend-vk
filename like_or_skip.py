import os

import requests

from get_album import get_photos_info

TOKEN = os.getenv('TOKEN')

like_url = 'https://api.vk.com/method/likes.add?type=photo&owner_id={GROUP_ID}&item_id={ITEM_ID}&access_token={TOKEN}&v=5.131'
skip_url = 'https://api.vk.com/method/likes.delete?type=photo&owner_id={GROUP_ID}&item_id={ITEM_ID}&access_token={TOKEN}&v=5.131'


def main():
    urls = [like_url, skip_url]
    for meme in get_photos_info():
        print("Meme author: ", meme['author'])
        print('Likes: ', meme['likes'])
        print('Meme URL: ', meme['meme_url'])
        choice = str(input('Do you want to like it or skip? [like/skip] '))
        while True:
            if choice in ['like', 'skip']:
                res = requests.get(urls[int(choice == 'skip')].format(GROUP_ID=meme['group_id'],
                                                                      ITEM_ID=meme['meme_id'], TOKEN=TOKEN)).json()
                try:
                    count = res['response']['likes']
                    print(f'Now meme has {count} likes')
                except KeyError:
                    print('Skipping...')
                break
            else:
                choice = str(input('Incorrect input, you can only [like] or [skip]'))


main()