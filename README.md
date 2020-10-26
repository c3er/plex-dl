# Plex Downloader

A tool for batch downloading of Plex videos.

## Prerequisites

The tool is based on the "plexapi" library. To install this requirement:

```
pip install -r requirements.txt
```

Username and password for your Plex account is needed. This information has to be in a file "secrets.json":

```json
{
    "plexAccount": {
        "user": "<your e-mail address or Plex username>",
        "password": "<your password>"
    }
}
```

## Usage

The user interface is very minimalistic, if it's even exists. To perform a download, you have to set certain parameters in the source code of "plex.py". There is a section that looks like this:

```python
SERVER = "Some server"
SHOWS = [
    Show("Section 1", "Show 1"),
    Show("Section 1", "Show 2"),
    Show("Section 2", "Show 3"),
]
```

### `SERVER`

Name of a shared server. That's the small grey text under the share name.

### `SHOWS`

A list of `Show` objects. Each `Show` object expects two parameters:

- **Section:** exact title of the section contained in the share, e.g. "Series", "Movies"
- **Show name:** exact name of the show of interest
