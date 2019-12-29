#!/usr/bin/env python3

"""
Get a list of members of the CSPAN "Members of Congress" list.

Prints to stdout.
"""


import tweepy
import os

T = tweepy.API(
    auth_handler=tweepy.auth.OAuthHandler(
        consumer_key=os.getenv("T_CONSUMER_KEY"),
        consumer_secret=os.getenv("T_CONSUMER_SECRET"),
    )
)


congress_accts = []
for page in tweepy.Cursor(T.list_members, owner_screen_name="SenateDems", slug="senaterepublicans").pages():
    congress_accts.extend(page)

print("\n".join([u.screen_name for u in congress_accts]))
