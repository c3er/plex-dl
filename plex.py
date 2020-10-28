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


def download(movie, outpath):
    try:
        filename = extract_filename(movie)
        path = os.path.join(outpath, filename)
        if os.path.exists(path):
            log(f'"{filename}" exists already; skipping')
        else:
            log(f'Download "{filename}"...', end="\t")
            movie.download(outpath, keep_original_name=True)
            log("Ready")
    except KeyboardInterrupt:
        os.remove(path)
        raise


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
                log(f'Downloading {len(episodes)} episodes of "{show.name}"...')

                showpath = os.path.join(outpath, show.filename)
                mkdir(showpath)

                for episode in episodes:
                    download(episode, showpath)
                log("All episodes downloaded")
            elif isinstance(plexshow, plexapi.video.Movie):
                download(plexshow, outpath)
            else:
                error(f"Not supported: {type(plexshow)}")
    except KeyboardInterrupt:
        log("Interrupted")


if __name__ == "__main__":
    main()
