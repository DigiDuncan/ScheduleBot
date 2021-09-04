from discord.ext import commands

# from pony import orm
from digical import Time, TimeRange, Schedule
# from schedulebot.lib import db
from schedulebot.lib.utils import sentence_join


class Player:
    def __init__(self, pid: int, schedule: Schedule = None, timezone: int = -5):
        self.pid = pid
        if schedule is None:
            schedule = Schedule()
        self.schedule = schedule
        self.timezone = timezone


players: dict[int, Player] = {}  # "database"

days = {
    "sun": 0,
    "mon": 1,
    "tue": 2,
    "wed": 3,
    "thu": 4,
    "fri": 5,
    "sat": 6
}


def get_saved_player(pid):
    if pid not in players:
        players[pid] = Player(pid)
    return players[pid]


def get_player(pid):
    return players.get(pid, Player(pid))


class CalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, sd: str, sh: int, sm: int, ed: str, eh: int, em: int):
        """
        Add a block of time to your schedule.
        """
        player = get_saved_player(ctx.author.id)
        sched = player.schedule
        sd = days[sd.lower()]
        ed = days[ed.lower()]
        sched.add(
            TimeRange(
                Time.from_dhm(sd, sh, sm),
                Time.from_dhm(ed, eh, em)
            ) - (60 * player.timezone)
        )

    @commands.command()
    async def remove(self, ctx, sd: str, sh: int, sm: int, ed: str, eh: int, em: int):
        """
        Remove a block of time to your schedule.
        """
        player = get_saved_player(ctx.author.id)
        sched = player.schedule
        ed = days[ed.lower()]
        sched.discard(
            TimeRange(
                Time.from_dhm(sd, sh, sm),
                Time.from_dhm(ed, eh, em)
            ) - (60 * player.timezone)
        )

    @commands.command()
    async def clear(self, ctx):
        """
        Empty your schedule.
        """
        player = get_saved_player(ctx.author.id)
        player.schedule = Schedule()

    @commands.command(
        usage = "<users...>"
    )
    async def schedule(self, ctx):
        """
        Find a schedule.
        """
        player = get_player(ctx.author.id)
        players = [(get_player(u.id), u) for u in ctx.message.mentions]
        bad_players = [(p, u) for p, u in players if len(p.schedule) == 0]
        if bad_players:
            await ctx.send(f"{sentence_join([u.display_name for p, u in bad_players], oxford = True)} do not have schedules.")
            return
        schedules = [p.schedule for p, u in players]
        first_schedule = schedules.pop()
        good_schedule = first_schedule.intersection(*schedules) + player.timezone
        await ctx.send(good_schedule)

    @commands.command()
    async def timezone(self, ctx, tz: int):
        """
        Set your timezone.
        """
        player = get_saved_player(ctx.author.id)
        player.timezone = tz


def setup(bot):
    bot.add_cog(CalendarCog(bot))
