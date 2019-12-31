import json
import pandas as pd
import glob
import tqdm

PATH = "../data/users/"
users = glob.glob(PATH + "*.json")

user_info = pd.DataFrame()
user_info = user_info.append([json.load(open(u, 'r')) for u in tqdm.tqdm(users)])
print(len(user_info))

user_info.profile_image_url[
    user_info.profile_image_url == 'https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png'
] = None

user_info.to_csv("../data/users.tsv", "\t", quoting=2)
