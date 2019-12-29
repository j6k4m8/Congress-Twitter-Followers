#!/usr/bin/env python3

"""
Get a list of members of the CSPAN "Members of Congress" list.

Prints to stdout.
"""


import tweepy
import os
import sys

T = tweepy.API(
    auth_handler=tweepy.auth.OAuthHandler(
        consumer_key=os.getenv("T_CONSUMER_KEY"),
        consumer_secret=os.getenv("T_CONSUMER_SECRET"),
    )
)


def main(owner: str, slug: str):
    congress_accts = []
    for page in tweepy.Cursor(
        T.list_members, owner_screen_name=owner, slug=slug
    ).pages():
        congress_accts.extend(page)

    print("\n".join([u.screen_name for u in congress_accts]))


if __name__ == "__main__":
    house = sys.argv[-2].lower()
    if house not in ["senate", "house"]:
        raise ValueError("Invoke with get-members.py [senate|house] [R|D]")
    party = sys.argv[-1].lower()
    if party not in ["r", "d"]:
        raise ValueError("Invoke with get-members.py [senate|house] [R|D]")

    main(
        *{
            ("senate", "r"): ("SenateDems", "senaterepublicans"),
            ("senate", "d"): ("SenateDems", "senatedemocrats"),
            ("house", "d"): ("thedemocrats", "house-democrats"),
            ("house", "r"): ("housegop", "house-republicans")
        }[(house, party)]
    )

