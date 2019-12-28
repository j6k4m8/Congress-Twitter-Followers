#!/usr/bin/env python3

"""
Get a list of members of the CSPAN "Members of Congress" list.

Prints to stdout.
"""


import tweepy

T = tweepy.API(
    auth_handler=tweepy.auth.OAuthHandler(
        consumer_key='',
        consumer_secret='',
    )
)


congress_accts = []
for page in tweepy.Cursor(T.list_members, owner_screen_name="cspan", slug="members-of-congress").pages():
    congress_accts.extend(page)

print("\n".join(congress_accts))
