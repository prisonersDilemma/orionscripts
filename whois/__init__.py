#!/usr/bin/env python3.6

#from .nacat import join_msg, join_msg_from, nacat
#from .tail import Tail, tail, tfilter
#from .targets import gettargets, yesterdays, yesterdays_targets
#from .yyyymmdd import date, DateComp, getdates, str2ints, yesterday, yyyymmdd

from database import create_database, create_table, insert_record
from nacat import join_msg, join_msg_from, nacat
from tail import Tail, tail, tfilter
from targets import gettargets, yesterdays, yesterdays_targets
from yyyymmdd import date, DateComp, getdates, str2ints, yesterday, yyyymmdd


global __package__
__package__ = 'whois'
global __version__
__version__ = (0,0,1)
