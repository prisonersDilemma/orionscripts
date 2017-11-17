#!/usr/bin/env python3.6

__date__ = '2017-11-14'
__version__ = (0,0,1)

"""
Get yesterday's date with the yesterday function, choose a date with the
yyyymmdd function, or filter strings for a date pattern of the form dddd-dd-dd.

Also available is a DateComp class, which converts a datestamp to an object
with year, month, and day attributes with integer values, and a convenience
function str2ints, which, given a datestamp string, returns a DateComp
instance.
"""

from datetime import datetime
from re import compile

# date pattern, of the form 'dddd-dd-dd', where 'd' is a digit.
date = compile(r'(?P<date>(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}))').search


# Force any changes to the values to be the right type, within the right range.
# Add aliases for year/month/day as y,m,d
class DateComp:
    """Create a DateComp object, which, given a string of the form
    yyyy-mm-dd, converts it to ints as attributes of the corresponding values.
    """
    def __init__(self, dstring):
        d = dstring.split('-')
        self.y = int(d[0])
        self.m = int(d[1])
        self.d = int(d[2])


    def __repr__(self):
        return 'DateComp(year={}, month={}, day={})'.format(self.year, self.month, self.day)

    def __str__(self):
        return f'{self.year}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)}'


    @property
    def year(self):
        return self.y
    @property
    def month(self):
        return self.m
    @property
    def day(self):
        return self.d


    # Could convert other to DateComp if its a suitably formatted string.
    # I don't need to assert anywhere else. The other comparisons depend on this.

    def __gt__(self, other):
        assert isinstance(other, DateComp)
        if self.y > other.y:
            return True
        elif self.y < other.y:
            return False
        elif self.m > other.m: # year == year; month?
            return True
        elif self.m < other.m:
            return False
        return self.d > other.d # month == month; day?

    def __eq__(self, other):
        assert isinstance(other, DateComp)
        return (self.y == other.y) and (self.m == other.m) and (self.d == other.d)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return not (self.__gt__(other) or self.__eq__(other))

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)


        # 14 < 14 == True
        # 14 > 14 == False

        # 15 == 14
        # 15 < 14 ? False
        # 15 > 14 ? True
        # not False and not True
        # False and True
        # False

        # 14 == 14
        # 14 < 14 ? False
        # 14 > 14 ? False
        # not False and not False
        # True and True
        # True





def yesterday():
    """Return a string of yesterday's date in YYYY-MM-DD format."""
    date_obj = datetime.now()
    return '{}-{}-{}'.format(date_obj.year, date_obj.month, date_obj.day - 1)


def yyyymmdd(**kwargs):
    """Return a date string given any kwargs *yyyy*, *mm*, *dd* or current.

    Example: Today's date is 2017-11-13

    >>> yyyymmdd(mm=09)
    '2017-09-13'
    >>> yyyymmdd(dd="9")
    '2017-11-09'
    >>> yyyymmdd(dd=1, mm=12)
    '2017-12-01'
    """
    date_obj = datetime.now()
    year = str(kwargs.get('yyyy', date_obj.year))
    month = str(kwargs.get('mm', date_obj.month)).zfill(2)
    day = str(kwargs.get('dd', date_obj.day)).zfill(2)
    return '{}-{}-{}'.format(year, month, day)


def getdates(*args):
    """Yield a str value of 'date' pattern dddd-dd-dd or None for all args."""
    for arg in args:
        match = date(arg)
        if match:
            yield match.group('date')


def str2ints(dstring):
    """Return an object with year, month, and day attributes as ints given a date string."""
    return DateComp(dstring)
