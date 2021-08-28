from pathlib import Path

import appdirs


def getDataDir():
    appname = "schedulebot"
    appauthor = "DigiDuncan"
    datadir = Path(appdirs.user_data_dir(appname, appauthor))
    return datadir


# File paths
datadir = getDataDir()
confpath = datadir / "schedulebot.conf"
tempdir = datadir / "temp"
