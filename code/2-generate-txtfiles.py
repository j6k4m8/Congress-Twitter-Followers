import datetime

OUT_PATH = "../data/members/"

with open("./followers.twint.data", 'r') as fh:
    lines = fh.readlines()

for line in lines:
    rep, followers = line.split(": ")
    followers = followers.split(',')
    with open(f"{OUT_PATH}/{rep}.txt", 'w') as fh:
        fh.write(f"# updated: {now.isoformat()}\n")
        fh.write(f"# count: {len(followers)}\n")
        fh.write("\n".join(sorted(followers)))

