"""Helper functions around the standard library's ``datetime`` module."""

import datetime


def convert_day_to_int(day=None):
    """Get an 8-digit int for the provided *day*::

        >>> from ustudioapi.utils import date
        >>> date.convert_day_to_int(datetime.datetime(year=2010, month=1, day=2))
        20100102

    If *day* is not passed then the current date is used::

        >>> date.convert_day_to_int()
        20111212

    """
    if not day:
        day = datetime.date.today()
    string = '%04d%02d%02d' % (day.year, day.month, day.day)
    return int(string)


def make_timestamp():
    """Return a timestamp int in the form YYYYMMDDHHMMSS."""
    day = datetime.datetime.today()
    string = u"%04d%02d%02d%02d%02d%02d" % (
        day.year, day.month, day.day, day.hour, day.minute, day.second)
    return string
