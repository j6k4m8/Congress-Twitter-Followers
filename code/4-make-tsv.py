import json
import pandas as pd
import glob
import tqdm

PATH = "../data/users/"
users = glob.glob(PATH + "*.json")

user_info = pd.DataFrame()
user_info = user_info.append([json.load(open(u, 'r')) for u in users])
print(len(user_info))

user_info.to_csv("../data/users.tsv", "\t", quoting=2)
