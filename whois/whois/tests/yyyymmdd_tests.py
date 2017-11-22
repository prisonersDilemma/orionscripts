#!/usr/bin/env python3.6

# Passed: 2017-11-15 06:40:57AM

from datetime import datetime
from unittest import TestCase

import whois

# These are variable! so I can't hardcode them, or the values I'm testing
# against will change every day, and the tests will fail. So, rather than
# rewriting them for every test, I've put them here.

today_obj = datetime.now()
# The values for the current year, month, and day as ints.
year, month, day = today_obj.year, today_obj.month, today_obj.day

def set_date(**kwargs):
    """Return a YYYY-MM-DD formatted string of year, month, and day.
    By default, year, month, and day are today, but any of them can be
    changed, passed as keyword args, as ints or string."""
    year = kwargs.get('year') if kwargs.get('year') else today_obj.year
    month = kwargs.get('month') if kwargs.get('month') else today_obj.month
    day = kwargs.get('day') if kwargs.get('day') else today_obj.day
    return '-'.join((str(_).zfill(2) for _ in (year,month,day)))


class YYYYMMDDTest(TestCase):

    def test_yesterday(self):
        self.assertEqual(whois.yesterday(), set_date(day=day-1))
        self.assertNotEqual(whois.yesterday(), set_date())


    def test_yyyymmdd(self):
        # mm as int w/o leading 0
        self.assertEqual(whois.yyyymmdd(mm=1), set_date(month=1))

        # dd as str
        self.assertEqual(whois.yyyymmdd(dd='31'), set_date(day=31))

        # mm as str w/o leading 0
        self.assertEqual(whois.yyyymmdd(mm='9'), set_date(month=9))

        # mm and dd as single digit ints
        self.assertEqual(whois.yyyymmdd(mm=1, dd=1),
                         set_date(month=1, day=1))

        # mm and dd as int and str, single digit and zfill respectively
        self.assertEqual(whois.yyyymmdd(mm=7, dd='08'),
                         set_date(month=7, day=8)) # Python doesn't recognize 07 & 08

        # mm, dd, and yyyy as str & int types in various order
        self.assertEqual(whois.yyyymmdd(dd='14', yyyy=1981, mm='7'),
                         set_date(year=1981,month=7,day=14))

        # token NotEqual
        self.assertNotEqual(whois.yyyymmdd(yyyy=2017,mm=1,dd=1), 2017-1-1)


    def test_getdates(self):
        # 9 lines, 5 contain dates (all the same) in:
        # tests/samples-micro/lines-with-dates
        with open('/home/na/git/prisonersDilemma/orionscripts/whois/tests/samples-micro/lines-with-dates', mode='r') as f:
            lines = list(f)

        _getdates = [d for d in whois.getdates(*lines)]
        _testcase = [ "2017-02-18", "2017-02-18", "2017-02-18", "2017-02-18", "2017-02-18", ]

        self.assertEqual(_getdates, _testcase)


    def test_str2ints(self):
        d = whois.str2ints('2017-11-14')
        self.assertEqual(d.year, 2017)
        self.assertEqual(d.month, 11)
        self.assertEqual(d.day, 14)
        self.assertNotEqual(d.day, '14')
        self.assertTrue(isinstance(d, whois.DateComp))


    def test_DateComp_comparators(self):
        d1 = whois.DateComp('2017-11-15')
        d2 = whois.DateComp('2017-11-14')
        d3 = whois.DateComp('2017-11-14')
        d4 = '2017-11-15' # Test exception

        self.assertTrue(d1 > d2)
        self.assertFalse(d2 > d1)

        self.assertTrue(d2 < d1)
        self.assertFalse(d1 < d2)

        self.assertTrue(d2 == d3)
        self.assertFalse(d1 == d2)

        self.assertTrue(d1 != d2)

        self.assertTrue(d1 >= d2)
        self.assertFalse(d2 >= d1)

        self.assertTrue(d2 <= d1)
        self.assertFalse(d1 <= d2)

        self.assertTrue(d2 <= d3)
        self.assertFalse(d1 <= d3)

        self.assertFalse(d1 <= d2)
        self.assertFalse(d1 <= d3)

        # Comparing a non DateComp object.
        with self.assertRaises(AssertionError) as cm:
            d1 == d4
        the_exception = cm.exception

        with self.assertRaises(AssertionError) as cm:
            d1 > d4
        the_exception = cm.exception

        with self.assertRaises(AssertionError) as cm:
            d1 < d4
        the_exception = cm.exception

        with self.assertRaises(AssertionError) as cm:
            d1 >= d4
        the_exception = cm.exception

        with self.assertRaises(AssertionError) as cm:
            d1 <= d4
        the_exception = cm.exception


if __name__ == '__main__':
    YYYYMMDDTest()

    # $ cd whois
    # $ python3.6 -m unittest tests.yyyymmdd_tests
    #                         ^package ^module
