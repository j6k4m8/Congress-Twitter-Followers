import subprocess
import tqdm
import os
from joblib import Parallel, delayed


def save_user_info(user):
    if os.path.exists(f"../data/users/{user}.json"):
        return
    try:
        subprocess.check_output(
            f"twint --user-full --json -u {user} -o ../data/users/{user}.json".split()
        )
    except subprocess.CalledProcessError as e:
        print(e)

def get_all_users():
    all_users = set()
    with open("./followers.twint.data", 'r') as fh:
        for line in fh.readlines():
            rep, followers = line.split(": ")
            followers = followers.split(",")
            all_users.update(followers)
    return all_users

all_users = get_all_users()

Parallel(n_jobs=4)(delayed(save_user_info)(u) for u in tqdm.tqdm(all_users))
