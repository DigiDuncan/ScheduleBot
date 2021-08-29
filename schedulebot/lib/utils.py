from typing import Iterable, Optional, Tuple, TypeVar, Union

re_num = r"\d+\.?\d*"

T = TypeVar("T")


def clamp(minVal: T, val: T, maxVal: T) -> T:
    """Clamp a `val` to be no lower than `minVal`, and no higher than `maxVal`."""
    return max(minVal, min(maxVal, val))


def prettyTimeDelta(totalSeconds: Union[int, float], millisecondAccuracy: bool = False, roundeventually: bool = False) -> str:
    """Get a human readable string representing an amount of time passed."""
    MILLISECONDS_PER_YEAR = 86400 * 365 * 1000
    MILLISECONDS_PER_DAY = 86400 * 1000
    MILLISECONDS_PER_HOUR = 3600 * 1000
    MILLISECONDS_PER_MINUTE = 60 * 1000
    MILLISECONDS_PER_SECOND = 1000

    inputms = milliseconds = int(totalSeconds * 1000)
    years, milliseconds = divmod(milliseconds, MILLISECONDS_PER_YEAR)
    days, milliseconds = divmod(milliseconds, MILLISECONDS_PER_DAY)
    hours, milliseconds = divmod(milliseconds, MILLISECONDS_PER_HOUR)
    minutes, milliseconds = divmod(milliseconds, MILLISECONDS_PER_MINUTE)
    seconds, milliseconds = divmod(milliseconds, MILLISECONDS_PER_SECOND)

    s = ""
    if not roundeventually or inputms <= MILLISECONDS_PER_DAY:
        if inputms >= MILLISECONDS_PER_YEAR:
            s += f"{years:,d} year{'s' if years != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_DAY:
            s += f"{days:,d} day{'s' if days != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_HOUR:
            s += f"{hours:,d} hour{'s' if hours != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_MINUTE:
            s += f"{minutes:,d} minute{'s' if minutes != 1 else ''}, "
        if millisecondAccuracy:
            s += f"{seconds:,d}.{milliseconds:03d} second{'' if seconds == 1 and milliseconds == 0 else 's'}"
        else:
            s += f"{seconds:,d} second{'s' if seconds != 1 else ''}"
    elif inputms >= MILLISECONDS_PER_YEAR:
        if inputms >= MILLISECONDS_PER_YEAR:
            s += f"{years:,d} year{'s' if years != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_DAY:
            s += f"{days:,d} day{'s' if days != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_HOUR:
            s += f"{hours:,d} hour{'s' if hours != 1 else ''}"
    elif inputms >= MILLISECONDS_PER_DAY:
        if inputms >= MILLISECONDS_PER_YEAR:
            s += f"{years:,d} year{'s' if years != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_DAY:
            s += f"{days:,d} day{'s' if days != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_HOUR:
            s += f"{hours:,d} hour{'s' if hours != 1 else ''}, "
        if inputms >= MILLISECONDS_PER_MINUTE:
            s += f"{minutes:,d} minute{'s' if minutes != 1 else ''}"

    return s


A = TypeVar("A")
B = TypeVar("B")


def minmax(first: A, second: B) -> Union[Tuple[A, B], Tuple[B, A]]:
    """Return a tuple where item 0 is the smaller value, and item 1 is the larger value."""
    small, big = first, second
    if small > big:
        small, big = big, small
    return small, big


def sentence_join(items: Iterable[str], *, joiner: Optional[str] = None, oxford: bool = False) -> str:
    """Join a list of strings like a sentence.

    >>> sentence_join(['red', 'green', 'blue'])
    'red, green and blue'

    Optionally, a different joiner can be provided.
    """
    if not items:
        return ""

    if joiner is None:
        joiner = "and"

    ox = ""
    if oxford:
        ox = ","

    # Do this in case we received something like a generator, that needs to be wrapped in a list
    items = list(items)

    if len(items) == 1:
        return items[0]

    return f"{', '.join(items[:-1])}{ox} {joiner} {items[-1]}"


def truncate(s: str, amount: int) -> str:
    """Return a string that is no longer than the amount specified."""
    if len(s) > amount:
        return s[:amount - 3] + "..."
    return s
