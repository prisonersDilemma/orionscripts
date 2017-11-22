#!/usr/bin/env python3.6

from . import database
from . import nacat
from . import targets

# Not sure if this will work if the packages aren't all installed separately.
import bytepos
import tables
import tail
import yyyymmdd

global PKGPATH # Not even sure how global works.
PKGPATH = __path__[0]
