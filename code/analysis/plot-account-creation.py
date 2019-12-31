
# coding: utf-8

# # Generate plots by party

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from typing import List
from functools import lru_cache


# In[8]:


import pandas as pd
import json
import datetime
import tqdm


# In[4]:


import matplotlib.pyplot as plt
import numpy as np


# In[125]:


affiliation_data = pd.read_csv(
    "./repo/data/twitter_affiliation_bioguide.txt", sep=" ",
    names=("screen_name", "party", "bioguide")
)


# In[126]:


user_data = pd.read_csv(
    "./repo/data/users.tsv", sep="\t",
    parse_dates=[['join_date', 'join_time']]
)
user_data.set_index("username", inplace=True)


# In[131]:


@lru_cache(maxsize=2048)
def get_follower_screen_names(screen_name: str) -> List[str]:
    try:
        with open(f"./repo/data/members/{screen_name}.txt", "r") as fh:
            return [
                line.strip() for line in fh.readlines()
                if not line.startswith("#")
            ]
    except:
        return []
        
@lru_cache(maxsize=2048)
def get_follower_metadata(screen_name: str) -> pd.DataFrame:
    return user_data[user_data.index.isin(get_follower_screen_names(screen_name))]


# In[132]:


join_dates = {
    "R": set(),
    "D": set(),
    "I": set()
}
for i, member in tqdm.tqdm(affiliation_data.iterrows(), total=len(affiliation_data)):
    followers = get_follower_metadata(member.screen_name)
    join_dates[member.party].update(followers.join_date_join_time)


# In[133]:


len(join_dates['R']), len(join_dates['D']), len(join_dates['I'])


# In[15]:


len(join_dates['R']), len(join_dates['D']), len(join_dates['I'])


# In[134]:


dem_creation_times = pd.to_datetime(list(join_dates['D']))
rep_creation_times = pd.to_datetime(list(join_dates['R']))


# In[135]:


bin_duration = 7 # days
bin_count = int((max(dem_creation_times) - min(dem_creation_times)) / datetime.timedelta(bin_duration))
print(bin_count)


# In[157]:


def plot_over_time():
    START_DATE = datetime.datetime(2008, 1, 1)
    END_DATE = datetime.datetime(2020, 1, 1)
    ANNOTATION_Y = 320
    ANNOTATION_OFFSET_MULT = 6

    events = [
        (datetime.datetime(2016, 11, 8), datetime.timedelta(1), 0, "2016 Election Day"),
        (datetime.datetime(2017, 1, 20), datetime.timedelta(2), -5, "Inauguration/Women's March"),
        (datetime.datetime(2018, 11, 6), datetime.timedelta(1), 0, "2018 Midterm Election Day"),
        (datetime.datetime(2019, 4, 18), datetime.timedelta(1), -10, "Mueller Report Released"),
        (datetime.datetime(2019, 9, 24), datetime.timedelta(70), 10, "Impeachment Hearings Begin")
    ]

    RATIO = 8
    with plt.style.context(('fivethirtyeight')):
        plt.rcParams["font.family"] = "Fira Code"
        plt.tight_layout(0.5)
        plt.figure(figsize=(2*RATIO, 1*RATIO))

        # Histograms
        plt.hist(rep_creation_times, weights=[-2]*len(rep_creation_times), bins=bin_count, color='#B8390B')
        plt.hist(dem_creation_times, bins=bin_count, color='#0096FF')

        # Events
        for start, duration, offset, title in events:
            plt.axvspan(start, start+max(datetime.timedelta(10), duration), alpha=0.2, color='purple')
            plt.text(
                start, ANNOTATION_Y + offset*ANNOTATION_OFFSET_MULT, 
                title, fontdict={'family': 'sans-serif', 'size': 10}, ha='right', va='top'
            )

        # Formatting
        plt.xlim(START_DATE, END_DATE)
        plt.title(f"Account Creation over Time (n={len(user_data)})")
        plt.ylabel("Magnitude of accounts")
        plt.xlabel(f"Date of account creation (bin={bin_duration} days)")
        plt.show()


# In[158]:


plot_over_time()


# In[124]:


plot_over_time()

