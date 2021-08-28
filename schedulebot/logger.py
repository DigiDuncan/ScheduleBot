import logging

from digiformatter import logger as digilogger

from schedulebot.lib.loglevels import CMD


def init_logging():
    logging.basicConfig(level=CMD)
    dfhandler = digilogger.DigiFormatterHandler()
    dfhandler.setLevel(CMD)

    logger = logging.getLogger("schedulebot")
    logger.setLevel(CMD)
    logger.handlers = []
    logger.propagate = False
    logger.addHandler(dfhandler)

    discordlogger = logging.getLogger("discord")
    discordlogger.setLevel(logging.WARN)
    discordlogger.handlers = []
    discordlogger.propagate = False
    discordlogger.addHandler(dfhandler)
