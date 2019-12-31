import subprocess
import tweepy
import tqdm
import json
from joblib import Parallel, delayed 

T = tweepy.API()

congress_accts = []
for page in tweepy.Cursor(T.list_members, owner_screen_name="cspan", slug="members-of-congress").pages():
    congress_accts.extend(page)


def get_followers(user):
    return subprocess.check_output(f"twint -u {user} --followers".split()).decode().split()

import time

followers = {}
def save_followers(c):
    vals = []
    while vals == []:
        vals = get_followers(c.screen_name)
        if vals == []:
            time.sleep(20)
            print(".", end="")
    followers[c.screen_name] = vals
    with open("followers.twint.data", 'a') as fh:
        fh.write("{}: {}\n".format(c.screen_name, ",".join(vals)))
        
Parallel(n_jobs=4)(delayed(save_followers)(c) for c in tqdm.tqdm(congress_accts))
