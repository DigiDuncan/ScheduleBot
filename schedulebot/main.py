
import os
import sys
from datetime import datetime
import logging
import digiformatter.styles

import discord
from discord.ext.commands import Bot

import discordn

from schedulebot import __version__
from schedulebot.conf import ConfLoadException, conf, load_conf
from schedulebot.lib import paths
from schedulebot.lib.logger import init_logging, BANNER, CMD, LOGIN
from schedulebot.lib.utils import truncate

init_logging()

discordn.patch()

logger = logging.getLogger("schedulebot")
initial_cogs = ["calendar"]
initial_extensions = []


def initConf():
    print("Initializing configuration file")
    try:
        conf.init()
        print(f"Configuration file initialized: {paths.confpath}")
    except FileExistsError as e:
        print(e)
        pass
    os.startfile(paths.confpath.parent)


def main():
    try:
        load_conf()
    except ConfLoadException:
        return

    launchtime = datetime.now()

    bot = Bot(command_prefix = conf.prefix)

    for extension in initial_extensions:
        bot.load_extension("schedulebot.extensions." + extension)
    for cog in initial_cogs:
        bot.load_extension("schedulebot.cogs." + cog)

    @bot.event
    async def on_first_ready():
        # Set the bots name to what's set in the config.
        try:
            await bot.user.edit(username = conf.name)
        except discord.errors.HTTPException:
            logger.warn("We can't change the username this much!")

        # Print the splash screen.
        # Obviously we need the banner printed in the terminal
        banner = ("ScheduleBot " + __version__)
        logger.log(BANNER, banner)
        logger.log(LOGIN, f"Logged in as: {bot.user.name} ({bot.user.id})\n------")

        # Add a special message to bot status if we are running in debug mode
        activity = discord.Game(name = "with the timeline")
        if sys.gettrace() is not None:
            activity = discord.Activity(type=discord.ActivityType.listening, name = "DEBUGGER 🔧")

        # More splash screen.
        await bot.change_presence(activity = activity)
        print(digiformatter.styles)
        logger.info(f"Prefix: {conf.prefix}")
        launchfinishtime = datetime.now()
        elapsed = launchfinishtime - launchtime
        logger.debug(f"ScheduleBot launched in {round((elapsed.total_seconds() * 1000), 3)} milliseconds.\n")

    @bot.event
    async def on_reconnect_ready():
        logger.error("ScheduleBot has been reconnected to Discord.")

    @bot.event
    async def on_command(ctx):
        guild = truncate(ctx.guild.name, 20) if (hasattr(ctx, "guild") and ctx.guild is not None) else "DM"
        logger.log(CMD, f"G {guild}, U {ctx.message.author.name}: {ctx.message.content}")

    @bot.event
    async def on_message(message):
        # F*** smart quotes.
        message.content = message.content.replace("“", "\"")
        message.content = message.content.replace("”", "\"")
        message.content = message.content.replace("’", "'")
        message.content = message.content.replace("‘", "'")

        await bot.process_commands(message)

    @bot.event
    async def on_message_edit(before, after):
        if before.content == after.content:
            return
        await bot.process_commands(after)

    def on_disconnect():
        logger.error("ScheduleBot has been disconnected from Discord!")

    if not conf.authtoken:
        logger.error("Authentication token not found!")
        return

    bot.run(conf.authtoken)
    on_disconnect()


if __name__ == "__main__":
    main()
