import json
import os
import sys

import plexapi.myplex as myplex


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
print(instance.devices())
