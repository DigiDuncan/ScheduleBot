import discord
from discord.ext import commands

from pony import orm
from schedulebot.lib import db


class TestCalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addplayer(self, ctx, who: discord.Member):
        added = False
        with orm.db_session:
            try:
                player = db.Player[who.id]
            except orm.ObjectNotFound:
                player = None

            if not player:
                player = db.Player(userid=who.id)
                added = True

        if added:
            resp = str(player.to_dict())
        else:
            resp = "Player already added"

        await ctx.send(resp)

    @commands.command()
    async def rmplayer(self, ctx, who: discord.Member):
        deleted = False
        with orm.db_session:
            try:
                db.Player[who.id].delete()
                deleted = True
            except orm.ObjectNotFound:
                pass

        if deleted:
            resp = "Player deleted"
        else:
            resp = "No player found"

        await ctx.send(resp)

    @commands.command()
    async def ls(self, ctx):
        with orm.db_session:
            players = db.Player.select()
            resp = (
                "\n".join(str(p.to_dict()) for p in players)
                if players else "No players found"
            )
        await ctx.send(resp)


def setup(bot):
    bot.add_cog(TestCalendarCog(bot))
