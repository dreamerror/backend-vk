import os
import json
import random
import dataclasses

import requests

from like_or_skip import like_url, skip_url

TOKEN = os.getenv('TOKEN')


@dataclasses.dataclass
class Meme:
    author: str
    group_id: int
    likes: int
    meme_url: str
    meme_id: int


with open('memes.json') as memes:
    all_memes = json.load(memes)['memes']

for i in range(len(all_memes)):
    all_memes[i] = Meme(all_memes[i]['author'], all_memes[i]['group_id'], all_memes[i]['likes'],
                        all_memes[i]['meme_url'], all_memes[i]['meme_id'])

special_meme = random.choice(all_memes)


def main():
    no_special_count = 0
    urls = [like_url, skip_url]
    while True:
        meme = random.choice(all_memes)
        if no_special_count == len(all_memes)//3:
            meme = special_meme
        if meme != special_meme:
            if meme.likes >= special_meme.likes:
                if not random.choice((True, False, False)):
                    meme = random.choice(all_memes)
                    no_special_count += 1
            no_special_count += 1
        print("Meme author: ", meme.author)
        print('Likes: ', meme.likes)
        print('Meme URL: ', meme.meme_url)
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
