#!/usr/bin/env python3

from typing import List
from functools import lru_cache

import pandas as pd
import json
import datetime
import tqdm

import matplotlib.pyplot as plt
import numpy as np

affiliation_data = pd.read_csv(
    "../data/twitter_affiliation_bioguide.txt", sep=" ",
    names=("screen_name", "party", "bioguide")
)

user_data = pd.read_csv(
    "../data/users.tsv", sep="\t",
    parse_dates=[['join_date', 'join_time']]
)
user_data.set_index("username", inplace=True)

@lru_cache(maxsize=2048)
def get_follower_screen_names(screen_name: str) -> List[str]:
    try:
        with open(f"../data/members/{screen_name}.txt", "r") as fh:
            return [
                line.strip() for line in fh.readlines()
                if not line.startswith("#")
            ]
    except:
        return []
        
@lru_cache(maxsize=2048)
def get_follower_metadata(screen_name: str) -> pd.DataFrame:
    return user_data[user_data.index.isin(get_follower_screen_names(screen_name))]

join_dates = {
    "R": set(),
    "D": set(),
    "I": set()
}
for i, member in tqdm.tqdm(affiliation_data.iterrows()):
    followers = get_follower_metadata(member.screen_name)
    join_dates[member.party].update(followers.join_date_join_time)

dem_creation_times = pd.to_datetime(list(join_dates['D']))
rep_creation_times = pd.to_datetime(list(join_dates['R']))

bin_duration = 7 # days
bin_count = (max(dem_creation_times) - min(dem_creation_times)) / datetime.timedelta(7)

events = [
    (datetime.datetime(2016, 11, 8), datetime.timedelta(1), "2016 Election Day"),
    (datetime.datetime(2018, 11, 6), datetime.timedelta(1), "2018 Midterm Elections")
]

RATIO = 8
with plt.style.context(('fivethirtyeight')):
    plt.rcParams["font.family"] = "Fira Code"
    plt.figure(figsize=(2*RATIO, 1*RATIO))
    # Events
    for start, duration, title in events:
        plt.axvspan(start, start+min(datetime.timedelta(2), duration), alpha=1, color='green')
        plt.text(start, 60, title, fontdict={'family': 'sans-serif', 'size': 10}, ha='right', va='top')
    # Histograms
    plt.hist(rep_creation_times, weights=[-2]*len(rep_creation_times), bins=500, color='#B8390B')
    plt.hist(dem_creation_times, bins=500, color='#0096FF')
    plt.title("Account Creation over Time")
    plt.ylabel("Magnitude of accounts")
    plt.xlabel(f"Date of account creation (bin={bin_duration} days)")
    plt.show()


