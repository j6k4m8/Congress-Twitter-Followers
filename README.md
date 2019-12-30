# Congress-Twitter-Followers

This repository lists the followers (and associated metadata) for the accounts following congressional voting members.

## Map

| Path | Description |
|----------|------|
| `/data/member/[Name].txt` | A list of screen-name followers for the `@[Name]` Twitter account |
| `/data/users/[Name].json` | A JSON representation of the metadata for the `@[Name]` Twitter account |
| `/data/users/users.tsv` | A somewhat-up-to-date TSV of the data stored in the users/JSON files |

| Path | Description |
|------|-------------|
| `/code/make-tsv.py` | Convert the individual JSON files into one standalone TSV (a copy of which lives at `/data/users.tsv`) |
