from pony import orm

from schedulebot.lib.paths import dbpath
from schedulebot.lib.strint import StrInt

db = orm.Database()


class Player(db.Entity):
    userid = orm.PrimaryKey(StrInt)
    timezone = orm.Optional(int, default=0)
    time_ranges = orm.Set("TimeRange")


class TimeRange(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    start = orm.Required(int)
    end = orm.Required(int)
    player = orm.Required(Player)


def init():
    db.bind(provider="sqlite", filename=str(dbpath), create_db=True)
    StrInt.init(db)
    db.generate_mapping(create_tables=True)
