#!/usr/bin/env python3.6

# Passed tests on: 2017-11-15 08:55:02AM

__date__ = '2017-11-15'
__version__ = (0,0,1)

"""
Tail a csv logfile for entries falling on a specific date. Return a
dictionary whose keys are the IP addresses found on the given date, and values
are dictionaries with a timestamp key and value.
"""

import tail
import yyyymmdd


def gettargets(logfile, trgtdate, nlines=100):
    """Return a dict of the targets matching a given *date* in *logfile*.
    The dict's keys are the IP addresses corresponding to the *date*
    argument, and the values are dicts, with a single key consisting of
    the associated timestamp.
    """
    trgts = {}
    trgtdatecomp = yyyymmdd.DateComp(trgtdate)
    finished = False
    #nchunks = 0 # How many chunks we've processed.

    for chunk in tail.Tail(fpath=logfile, nlines=nlines, bufsz=2048):
        #nchunks += 1
        for line in chunk.splitlines():

            # Good place to log exceptions? There should be a date in every
            # line, except the header (first line). In practice, should only
            # happen at the header. Otherwise, the header may raise an error
            # when we call group().
            dateptrns = yyyymmdd.date(line) # re.match object

            if not dateptrns:
                finished = True
            else:
                currdatecomp = yyyymmdd.DateComp(dateptrns.group('date'))
                if trgtdatecomp == currdatecomp:
                    ipaddr, tmstmp = line.split(',')
                    ipaddr, tmstmp = ipaddr.strip('"'), tmstmp.rstrip().strip('"')
                    trgts[ipaddr] = {'timestamp': tmstmp}

                # We've gone too far, and have reached dates before trgtdate.
                # Finish processing the lines in the current chunk and return.
                elif trgtdatecomp > currdatecomp:
                    finished = True

        # Once we've finished the current chunk of lines.
        if finished:
            break

    return trgts


def yesterdays_targets(logfile):
    """Return the targets from *logfile* that fall within yesterday's date."""
    return gettargets(logfile, trgtdate=yyyymmdd.yesterday())

# Alias.
yesterdays = yesterdays_targets


#if __name__ == '__main__':
#    log = '/home/na/git/prisonersDilemma/orionscripts/whois/tests/samples-micro/splunk-export.csv'
#
#    # 2 matches
#    #d = '2017-11-10'
#    #print(f'Target date: {d}') # OK when bufsz is >=2048
#    #for k,v in gettargets(log, d).items():
#    #    print(k,v)
#
#    # 8 matches
#    print(f'Target date: {yyyymmdd.yesterday()}')
#    for k,v in yesterdays_targets(log).items():
#        print(k,v)
