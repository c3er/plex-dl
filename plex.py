import json
import os
import sys

import plexapi.myplex as myplex


SERVER = "Some server"
LIBSECTION = "Some section"
SERIES = "Some series"


starterdir = os.path.dirname(os.path.realpath(sys.argv[0]))


class PlexAccount:
    def __init__(self):
        with open(os.path.join(starterdir, "secrets.json"), encoding="utf8") as f:
            data = json.load(f)
        cred = data["plexAccount"]

        self.user = cred["user"]
        self.password = cred["password"]


def extract_filename(episode):
    return episode.locations[0].split("/")[-1]


account = PlexAccount()
instance = myplex.MyPlexAccount(account.user, account.password)
server = instance.resource(SERVER).connect()
show = server.library.section(LIBSECTION).get(SERIES)

outdir = os.path.join(starterdir, "out")
if not os.path.exists(outdir):
    os.mkdir(outdir)

for episode in show.episodes():
    filename = extract_filename(episode)
    if os.path.exists(os.path.join(outdir, filename)):
        print(f'"{filename}" exists already; skipping')
    else:
        print(f'Download "{filename}"')
        episode.download(outdir, keep_original_name=True)

print("All episodes downloaded")
