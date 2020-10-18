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


account = PlexAccount()
instance = myplex.MyPlexAccount(account.user, account.password)
server = instance.resource(SERVER).connect()
show = server.library.section(LIBSECTION).get(SERIES)
outdir = os.path.join(starterdir, "out")
if not os.path.exists(outdir):
    os.mkdir(outdir)
episode = show.episodes()[0]
episode.download(outdir, keep_original_name=True)
