#!/usr/bin/env python3

import json
import pandas as pd
import glob
import tqdm
import matplotlib.pyplot as plt

PATH = "../../data/users/"
users = glob.glob(PATH + "*.json")

# TODO: slow
user_info = pd.DataFrame()
for u in tqdm.tqdm(users):
    user_info = user_info.append([json.load(open(u, 'r'))])


# TODO (jm): bin count is a random number right now
# Plot as histogram. Bin count totally arbitrarily chosen here.
plt.style.use('fivethirtyeight')
plt.title(f"Followers' Account Creation Dates (n={len(user_info)})")
plt.hist(pd.to_datetime(user_info.join_date), bins=150)

