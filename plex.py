import datetime
import json
import os
import re
import sys

import plexapi.myplex as myplex
import plexapi.video


class Show:
    def __init__(self, section, name, skip=0, ignore=0):
        self.section = section
        self.name = name
        self.skip = skip
        self.ignore = ignore

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


class Duration:
    def __init__(self, timedelta):
        self.hours, seconds = divmod(int(timedelta.total_seconds() + 0.5), 3600)
        self.minutes, self.seconds = divmod(seconds, 60)

    def __str__(self):
        return f"{self.hours:02}h{self.minutes:02}m{self.seconds:02}s"


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


def timestr(time):
    return f"{time.year}.{time.month:02}.{time.day:02} {time.hour:02}:{time.minute:02}:{time.second:02}"


def download(movie, outpath):
    try:
        filename = extract_filename(movie)
        path = os.path.join(outpath, filename)
        if os.path.exists(path):
            log(f'"{filename}" exists already; skipping')
        else:
            now = datetime.datetime.now

            starttime = now()
            log(timestr(starttime), filename, sep="\t", end="\t")
            movie.download(outpath, keep_original_name=True)

            finished_time = now()
            log(timestr(finished_time), Duration(finished_time - starttime), sep="\t")
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
                episodes = plexshow.episodes()[show.skip:]
                ignore = show.ignore
                if ignore > 0:
                    episodes = episodes[:-ignore]
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
