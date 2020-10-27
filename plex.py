import json
import os
import re
import sys

import plexapi.myplex as myplex
import plexapi.video


class Show:
    def __init__(self, section, name):
        self.section = section
        self.name = name

    @property
    def filename(self):
        return re.sub(r"[<>:\"/\\|\?\*]", "", self.name)


STARTERDIR = os.path.dirname(os.path.realpath(sys.argv[0]))

SERVER = "Some server"
SHOWS = [
    Show("Section 1", "Show 1"),
    Show("Section 1", "Show 2"),
    Show("Section 2", "Show 3"),
]


def log(*args, sep=" ", end="\n", file=sys.stdout):
    print(*args, sep=sep, end=end, file=file, flush=True)


def error(msg):
    log(msg, file=sys.stderr)
    sys.exit(1)


def extract_filename(episode):
    return episode.locations[0].split("/")[-1]


def mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def main():
    with open(os.path.join(STARTERDIR, "secrets.json"), encoding="utf8") as f:
        data = json.load(f)
    credentials = data["plexAccount"]

    connection = (myplex.MyPlexAccount(credentials["user"], credentials["password"])
        .resource(SERVER)
        .connect()
        .library)

    outpath = os.path.join(STARTERDIR, "out")
    mkdir(outpath)

    try:
        for show in SHOWS:
            plexshow = (connection
                .section(show.section)
                .get(show.name))
            if isinstance(plexshow, plexapi.video.Show):
                episodes = plexshow.episodes()
            elif isinstance(plexshow, plexapi.video.Movie):
                episodes = [plexshow]
            else:
                error(f"Not supported: {type(plexshow)}")

            showpath = os.path.join(outpath, show.filename)
            mkdir(showpath)

            log(f'Downloading {len(episodes)} episodes of "{show.name}"...')

            for episode in episodes:
                filename = extract_filename(episode)
                path = os.path.join(showpath, filename)
                if os.path.exists(path):
                    log(f'"{filename}" exists already; skipping')
                else:
                    log(f'Download "{filename}"...', end="\t")
                    episode.download(showpath, keep_original_name=True)
                    log("Ready")
            log("All episodes downloaded")
    except KeyboardInterrupt:
        log("Interrupted")
        os.remove(path)


if __name__ == "__main__":
    main()
