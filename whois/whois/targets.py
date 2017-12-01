#!/usr/bin/env python3.6
"""
Tail a csv logfile for entries falling on a specific date. Return a
dictionary whose keys are the IP addresses found on the given date, and values
are dictionaries with a timestamp key and value.
"""
__date__ = '2017-11-15'
__version__ = (0,1,0)


from logging import getLogger

import tail
import yyyymmdd

#===============================================================================
logger = getLogger(__name__)
logger.setLevel('DEBUG') # str -> int
#===============================================================================

def gettargets(logfile, trgtdate, nlines, bufsz, newline):
    """Return a dict of the targets matching a given *date* in *logfile*.
    The dict's keys are the IP addresses corresponding to the *date*
    argument, and the values are dicts, with a single key consisting of
    the associated timestamp.
    """
    trgts = {}
    trgtdatecomp = yyyymmdd.DateComp(trgtdate)
    finished = False
    nchunks = 0 # How many chunks we've processed.

    for chunk in tail.Tail(fpath=logfile, nlines=nlines, bufsz=bufsz, newline=newline):

        nchunks += 1
        logger.debug('chunk %s returned from Tail, with %s lines.', nchunks, len(chunk))

        for line in chunk:

            # Good place to log exceptions? There should be a date in every
            # line, except the header (first line). In practice, should only
            # happen at the header. Otherwise, the header may raise an error
            # when we call group().

            dateptrns = yyyymmdd.date(line) # re.match object

            # We must finish the chunk before we can return. The lines in each
            # chunk are in order, but the chunks are in reverse order.
            # Therefore, the first time we come to an older date, may or may
            # not be its first occurrence. In other words, there may be a
            # variable number of lines still to go, in the current chunk, which
            # may be of the target date.

            if not dateptrns:
                #logger.debug('Exiting loops in gettargets. No date pattern found in line:\n'
                #         '%s', line)
                finished = True

            else:
                currdatecomp = yyyymmdd.DateComp(dateptrns.group('date'))
                if trgtdatecomp == currdatecomp:
                    ipaddr, tmstmp = line.split(',')
                    ipaddr, tmstmp = ipaddr.strip('"'), tmstmp.rstrip().strip('"')
                    trgts[ipaddr] = {'timestamp': tmstmp}


                # This should be reversed. If trgtdate > currdate, it is a NEWER date.

                # We've gone too far, and have reached dates before trgtdate.
                # Finish processing the lines in the current chunk and return.
                elif trgtdatecomp < currdatecomp:
                    logger.debug('Reached an older date (%s) than the target date (%s).',
                                currdatecomp, trgtdatecomp)
                    logger.debug('Exiting loops after current chunk is finished.')
                    finished = True

        # Once we've finished the current chunk of lines.
        if finished:
            break

    #logger.debug('Returning %s targets.', len(trgts))
    return trgts


def yesterdays_targets(logfile):
    """Return the targets from *logfile* that fall within yesterday's date."""
    return gettargets(logfile, trgtdate=yyyymmdd.yesterday())

# Alias.
yesterdays = yesterdays_targets



@tail.tail._filter
def gentargets(trgtdate, **kwargs):
    trgtdatecomp = yyyymmdd.DateComp(trgtdate)
    for line in kwargs.get('lines'):
        dateptrns = yyyymmdd.date(line) # re.match object
        try:
        #if not dateptrns: raise StopIteration
            currdatecomp = yyyymmdd.DateComp(dateptrns.group('date'))
            if trgtdatecomp == currdatecomp:
                ipaddr, tmstmp = line.split(',')
                ipaddr, tmstmp = ipaddr.strip('"'), tmstmp.rstrip().strip('"')
                #targets[ipaddr] = {'timestamp': tmstmp}
                yield {ipaddr: {'timestamp': tmstmp}}
            #elif trgtdatecomp < currdatecomp:
                #logger.debug('Reached an older date (%s) than the target date (%s).', currdatecomp, trgtdatecomp)
                #logger.debug('Exiting loops after current chunk is finished.')
                #raise StopIteration
        except AttributeError: # no date.
            pass # return? raise StopIteration?


trgts = {}
# Why don't these work?
#trgts = {dct for gen in gettargets('2017-11-14') for dct in gen}
#trgts.update(dct for gen in gettargets('2017-11-14') for dct in gen)
# But this does.
for gen in gettargets('2017-11-14'):
    for dct in gen:
        trgts.update(dct)
#print(trgts)



#===============================================================================
# Changelog:
# 0.0.1 -- small fix for trgtdatecomp vs currdatecomp to less than.
# 0.0.2 -- Added generator which uses a new filter function from tail.
