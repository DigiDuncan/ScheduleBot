import importlib.resources as pkg_resources
from pathlib import Path

import appdirs

def getDataDir():
    appname = "Agendroid"
    appauthor = "DigiDuncan"
    datadir = Path(appdirs.user_data_dir(appname, appauthor))
    return datadir


# File paths
datadir = getDataDir()
confpath = datadir / "decbot.conf"
tempdir = datadir / "temp"
