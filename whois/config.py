#!/usr/bin/env python3.6

__date__ = '2017-11-16'
__package__ = 'whois' # Can I define this globally, along with __version__?

#===============================================================================
# DEFAULTS
# set[-option] cmd writes the options/values to the config file, making changes
# "permanent". Command-line args have the highest precedence (so they get
# applied last), and override any defaults or config file settings:
# defaults > config file > command-line args
#
# Add an option to display all defaults, or, optionally, of a [given] option?
#===============================================================================
from argparse import (ArgumentParser, RawDescriptionHelpFormatter,)
from datetime import datetime
from logging import basicConfig, getLevelName, getLogger
from os import getcwd, mkdir
from os.path import exists, expanduser, splitext
from yyyymmdd import yesterday
#===============================================================================
# Define some base variables.
CONFIGDIR = f'{getcwd()}/.whois'
CONFIGFILE = f'{CONFIGDIR}/{__package__}.conf'
LOGNAME = f'{__package__}.log'
LOGFILE = f'{CONFIGDIR}/{LOGNAME}'
LOGLEVELS = { 'DEBUG':10, 'INFO':20, 'WARNING':30, 'ERROR':40, 'CRITICAL':50 }
LOG_LEVEL = LOGLEVELS['DEBUG'] # Use set-option to change, and restart.
SCRIPTHOME = getcwd()
SCRIPTNAME = splitext(__file__)[0]
USERHOME = expanduser('~')
#===============================================================================
# Is it our first time running?
if not exists(CONFIGDIR):
    mkdir(CONFIGDIR)
#===============================================================================
# Configure the logger.
# A second logger is necessary to write to stdout (stream).
basicConfig(filename=LOGFILE,
            level=LOG_LEVEL, # defines the root logging level
            format='%(levelname)s: %(asctime)s: %(message)s',
            datefmt='%Y-%m-%d-%H:%M:%S%p',
            filemode='a')
logger = getLogger(__package__) # __name__?
logger.setLevel(LOG_LEVEL)
logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
logger.debug(f'logger: Initialized logging_level to: {getLevelName(logger.level)} '
             f'({logger.level})')
#===============================================================================
if not exists(CONFIGFILE):
    with open(CONFIGFILE, mode='x') as conf:
        conf.write('# Configuration file for whois. Created: {:%F %I:%M%p}\n'
                                                        .format(datetime.now()))
#===============================================================================
# Change DEFAULTS with 'set-option', which will rewrite the file in-place.

# Take out anything that's hardcoded and too specific. It can be put in whois.conf.
USERDIR = USERHOME
DEFAULTS = {
    'date'          : yesterday(),
    'hostname'      : 'whois.cymru.com',
    'list_file'     : f'{USERDIR}/daily-list.csv',
    'log_file'      : f'{USERDIR}/target.log', # For demo. Needs changing.
    'port'          : 43,
    'bufsz'         : 2048,
    'config_file'   : f'{CONFIGFILE}',
    'database_file' : f'{USERDIR}/whois.db',
    'logging_file'  : f'{CONFIGDIR}/whois.log',
    'logging_level' : f'INFO',
    'nlines'        : 100,
    'table_name'    : 'master',
}
#===============================================================================
class Options:
    """Return a Namespace object, provided a mapping sequence."""
    def __init__(self, mapseq):
        self._setattrs(mapseq)

    def __repr__(self):
        """Return a view into the namespace."""
        return 'Options({})'.format(
               ', '.join(('='.join([str(k),str(v)]) for k,v in self.__dict__.items())))

    def __str__(self):
        """Return a string of one option=value per line."""
        return '{}'.format(
               '\n'.join(('='.join([str(k),str(v)]) for k,v in self.__dict__.items())))

    def __iadd__(self, other):
        setattr(self, other[0], other[1])
        return self

    def _setattrs(self, mapseq):
        """Set the attributes of the Namespace, given a mapping sequence."""
        if isinstance(mapseq, dict):
            for k,v in mapseq.items():
                setattr(self, k,v)
        else:
            for k,v in mapseq:
                setattr(self, k,v)
#===============================================================================
def set_option(*args):
    """Write the change to the config file."""
    #print('set_option called with args: {}'.format('|'.join(args)))
    #with open(CONFIGFILE mode='a') as conf:
    ##Assemble args appropriately: options are prefixed with --, and - word seps
    ##are _.
    #    conf.write()
#===============================================================================
ARGS = DEFAULTS.copy() # Don't need two dicts, but may be useful while testing.
#===============================================================================
parser = ArgumentParser(
    prog='whois',
    description="""\
    \033[32;1mBuild a database based on whois queries of targets.\033[0m""",
    epilog="""\
    Filter a log for a given date. Run whois queries.
    Parse the output, to produce a daily list, and
    aggregate the cumalative results into a database.""",
    formatter_class=RawDescriptionHelpFormatter,
    #add_help=False,
    usage="""
    %(prog)s [--help|[--date][--hostname][--list-file][--log-file][--port]]
    %(prog)s set[-option] [--OPTION]""")


parser.add_argument('--date', metavar='YYYY-MM-DD',
    help='Filter\033[32;1mlog-file\033[0m for the given date.')
parser.add_argument('--hostname', metavar='URL',
    help='Send the whois query to the given host.')
parser.add_argument('--list-file', metavar='PATH',
    help='Write the current results to the given path.')
parser.add_argument('--log-file', metavar='PATH',
    help='Filter for \033[32;1mdate\033[0m at the given path.')
parser.add_argument('--port', type=int, metavar='INT',
    help='Use the given port when connecting to \033[32;1mhostname\033[0m.')

# Display the name like this: 'set[-option]'
subparsers = parser.add_subparsers(dest='cmd', title='subcommands', metavar='command',
    help='Execute a subcommand.')

set_option = subparsers.add_parser('set-option', aliases=['set'],
    #add_help=False,
    # Gets parents' args, too. But add_help=False needs to be set, and they share a help.
    #parents=[parser],
    # Ends up concatenated with parser's usage.
    #usage='%(prog)s set[-option] --OPTION ...[[--OPTION]...[--OPTION]]',
    help='Make changes permanent by writing them to the configuration file.')
set_option.set_defaults(func=set_option)

set_option.add_argument('--buffer-size', type=int, metavar='INT', dest='bufsz',
    help='Size in bytes (power of 2) to read when tailing \033[32;1mlog-file\033[0m.')
set_option.add_argument('--config-file', metavar='PATH',
    help="Change the location of  whois' permanent configurations.")
set_option.add_argument('--database-file', metavar='PATH',
    help='Set the path and name of the database.')
set_option.add_argument('--date', metavar='YYYY-MM-DD',
    help='Filter \033[32;1mlog-file\033[0m for the given date.')
set_option.add_argument('--hostname', metavar='URL',
    help='Send the whois query to the given host.')
set_option.add_argument('--list-file', metavar='PATH',
    help='Write the current results to the given path.')
set_option.add_argument('--log-file', metavar='PATH',
    help='Filter for \033[32;1mdate\033[0m at the given path.')
set_option.add_argument('--logging-file', metavar='PATH',
    help="Change the location of whois' log.")
set_option.add_argument('--logging-level', metavar='STR',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help="Set the level at which whois' will write to its log.")
set_option.add_argument('--port', type=int, metavar='INT',
    help='Use the given port when connecting to \033[32;1mhostname\033[0m')
set_option.add_argument('--table-name', metavar='NAME',
    help='Create the table of the given name in the \033[32;1mdatabase-file\033[0m.')
set_option.add_argument('--tail-nlines', type=int, metavar='INT', dest='nlines',
    help='Set how many lines to parse from \033[32;1mlog-file\033[0m at once.')
#===============================================================================
