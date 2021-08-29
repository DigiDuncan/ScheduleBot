from discord.ext import commands


class CalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duck(self, ctx, where: str):
        await ctx.send("Where?")


def setup(bot):
    bot.add_cog(CalendarCog(bot))
