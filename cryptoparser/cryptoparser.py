#!/usr/bin/env python3.6

__date__ = '2017-10-19'
__version__ = (0,0,6)

# Standard Library.
import argparse # ArgumentParser
import logging
import os       # path.exists, path.expanduser, path.join, mkdir
import shutil   # rmtree
import sys      # stdout.write
import time

# Package modules.
try: # httplib2 dependency.
    import scanner
    missing_httplib2_error_message = False
except ModuleNotFoundError:
    missing_httplib2_error_message = \
        """\
        scanner: error: Missing module httplib2.
        Try entering `pip3.6 install httplib2` on the command-line,
        or visiting: https://pypi.python.org/pypi/httplib2/0.10.3
        in your browser.
        """

SCRIPTDIR = os.getcwd()
SCRIPTNAME = os.path.splitext(__file__)[0]
LOGNAME = SCRIPTNAME + '.log'
LOGFILE = os.path.join(SCRIPTDIR, LOGNAME)


# Regular-expressions.
#coinhivehash = r""".*CoinHive.Anonymous\(('|")(?P<hash>\w+)('|")\)"""
coinhivehash = r""".*CoinHive.Anonymous\('?"?(?P<hash>\w{,32})'?"?\)"""

def main():
    parser = argparse.ArgumentParser(
        prog='cryptoparser.py',
        description='Parse a HTML source for a pattern, provided a list of URLs from a file.')
    parser.add_argument('--http-only', action='store_true', help='only request to http://')
    parser.add_argument('--https-only', action='store_true', help='only request to https://')
    parser.add_argument('infile', metavar='PATH', help='path to text file containing URLs')
    parser.add_argument('-l', '--log-level', metavar='STR', dest='loglevel', default='INFO',
                        choices=['debug', 'DEBUG', 'info', 'INFO', 'warning', 'WARNING',
                                 'error', 'ERROR', 'critical', 'CRITICAL'],
                        help='set the logging level; turn on error messages')
    parser.add_argument('outfile', nargs='?', metavar='PATH',
                        default=os.path.join(SCRIPTDIR, SCRIPTNAME + '.csv'),
                        help='path to output destination; default is $CWD/cryptoparser.out')
    parser.add_argument('-p', '--pattern', metavar='STR', type=str, default=coinhivehash,
                        help='string or regex to search for')
    parser.add_argument('-q', '--quiet-mode', dest='quietmode', action='store_true',
                        help='do not print any output to stdout')
    parser.add_argument('-s', '--sleep', type=int, metavar='INT', default=None,
                        help='time in seconds to delay between targets')
    parser.add_argument('-t', '--timeout', type=int, metavar='INT', default=None,
                        help=('time in seconds to wait before giving up on a host;'
                              "default is Python's default"))
    args = parser.parse_args()

    start_time = time.time()

    if args.quietmode:
        args.loglevel = 'CRITICAL'
    LOGLEVEL = getattr(logging, args.loglevel.upper(), None)

    logging.basicConfig(
        filename=LOGFILE,
        level=LOGLEVEL,
        # logging module still uses old format style.
        format='%(levelname)s: %(asctime)s: %(message)s', #noqa
        datefmt='%Y-%m-%d-%H:%M:%S%p',
        filemode='w')

    logger = logging.getLogger(__name__) # '__main__'
    logger.debug(f'logging level: {logger.level}') #noqa # logging level set to 0

    # Passed to the Http instance object for storing temporary files.
    cache = os.path.join(SCRIPTDIR, 'scanner_http_cache')
    if not os.path.exists(cache):
        logger.info('No cache exists. Creating cache directory.')
        os.mkdir(cache)
    logger.info('Cache location: {}'.format(cache))

    if missing_httplib2_error_message:
        logger.critical('Missing dependency: {}. Exiting.'.format('httplib2'))
        sys.stderr.write(missing_httplib2_error_message)
        sys.exit(1)


    logger.info('Creating Scanner object.')
    logger.debug('Scanner object is being passed a pattern of: {}'.format(args.pattern))

    # Does the same as below.
    #opts = dict(**vars(args))
    #del opts['loglevel'], opts['quietmode']
    #opts['logger'] = logger
    #scan = scanner.Scanner(**opts)

    scan = scanner.Scanner(
        infile=args.infile,
        outfile=args.outfile,
        pattern=args.pattern,
        cache=cache,
        timeout=args.timeout,
        sleep=args.sleep,
        logger=logger,
        quietmode=args.quietmode,
        http_only=args.http_only,
        https_only=args.https_only)

    logger.info('Starting scan.')
    scan.run()

    try: # Dir/files could be in use.
        shutil.rmtree(cache) # Delete the cache+contents.
        logger.info('Cache has been cleaned up.')
    except Exception as error_removing_cache:
        logger.exception('Could not remove cache: {}'.format(error_removing_cache))

    end_time = time.time()
    time_delta = 'Finished in: {:.4}s'.format(end_time - start_time)

    logger.info(time_delta)
    if not args.quietmode:
        sys.stdout.write(f'{time_delta}\n') #noqa


if __name__ == '__main__':
    main()

    #"""Return a constant of logging level, given an int (0,6],
    #which bears an inverse correlation to the number of times the
    #flag was passed as an argument to the script, i.e.,
    #    0 -> CRITICAL (only)
    #    1 -> ERROR (only)
    #    2 -> WARNING (only)
    #    3 -> INFO (only)
    #    4 -> DEBUG (only)
    #    5 -> NOTSET (only)
    #"""



