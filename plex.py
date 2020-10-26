import json
import os
import sys

import plexapi.myplex as myplex


SERVER = "Some server"
LIBSECTION = "Some section"
SHOW = "Some series"


starterdir = os.path.dirname(os.path.realpath(sys.argv[0]))


def log(*args, sep=" ", end="\n"):
    print(*args, sep=sep, end=end)
    sys.stdout.flush()


def extract_filename(episode):
    return episode.locations[0].split("/")[-1]


def main():
    with open(os.path.join(starterdir, "secrets.json"), encoding="utf8") as f:
        data = json.load(f)
    credentials = data["plexAccount"]

    episodes = (myplex.MyPlexAccount(credentials["user"], credentials["password"])
        .resource(SERVER)
        .connect()
        .library
        .section(LIBSECTION)
        .get(SHOW)
        .episodes())

    log(f'Downloading {len(episodes)} episodes of "{SHOW}"...')

    outdir = os.path.join(starterdir, "out")
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    try:
        for episode in episodes:
            filename = extract_filename(episode)
            if os.path.exists(os.path.join(outdir, filename)):
                log(f'"{filename}" exists already; skipping')
            else:
                log(f'Download "{filename}"...', end="\t")
                episode.download(outdir, keep_original_name=True)
                log("Ready")
        log("All episodes downloaded")
    except KeyboardInterrupt:
        log("Interrupted")


if __name__ == "__main__":
    main()
