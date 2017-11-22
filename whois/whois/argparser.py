#!/usr/bin/env python3.6
"""
Parse command-line arguments, and options in configuration file(s).
"""
__date__ = '2017-11-16'

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
from logging import getLogger
from re import sub
from os import getcwd, mkdir
from os.path import abspath, basename, exists, expanduser, join, splitext

from . import PKGPATH

from . import yyyymmdd

# Module-level logger.
logger = getLogger(__name__)


class Options:
    """Return a Namespace object, provided a mapping sequence."""
    def __init__(self, mapseq):
        self._setattrs(mapseq)

    def __repr__(self):
        """Return a view into the namespace."""
        return 'Options({})'.format(', '.join(('='.join([str(k),str(v)]) \
                                            for k,v in self.__dict__.items())))

    def __str__(self):
        """Return a string of one option=value per line."""
        return '{}'.format('\n'.join(('='.join([str(k),str(v)]) \
                                            for k,v in self.__dict__.items())))

    def __len__(self):
        return len(self.__dict__)

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



def set_option(opt_tuple, fpath):
    """Write the change to the user config file."""
    #print('set_option called with args: {}'.format('|'.join(args)))
    #with open(const.CONFIGFILE, mode='a') as conf:
    #    #Assemble args appropriately: options are prefixed with --, and - word seps are _.
    #    opt, arg = opt_tuple
    #    opt = sub(r'_', '-', opt)
    #    optline = '='.join((opt, arg))
    #    conf.write(f'{optline}\n')
    print('you have called set_option')


parser = ArgumentParser(
    prog='whois',
    description="""\
    \033[32;1mBuild a database based on whois queries of targets.\033[0m""",
    epilog="""\
    Filter a log for a given date. Run whois queries
    on a remote host. Parse the output. Produce a
    daily list (csv), and create and aggregate the
    results into a simple database.""",
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
parser.add_argument('--port', metavar='INT',
    help='Use the given port when connecting to \033[32;1mhostname\033[0m.')


# Display the name like this: 'set[-option]'
subparsers = parser.add_subparsers(dest='cmd', title='subcommands', metavar='command',
    help='Execute a subcommand.')


# Gets parents' args, too. But add_help=False needs to be set, and they share a help.
set_option = subparsers.add_parser('set-option', aliases=['set'],
    add_help=False,
    parents=[parser],
    help='Make changes permanent by writing them to the configuration file.')
set_option.set_defaults(func=set_option)

set_option.add_argument('--buffer-size', metavar='INT', dest='bufsz',
    help='Size in bytes (power of 2) to read when tailing \033[32;1mlog-file\033[0m.')
set_option.add_argument('--config-file', metavar='PATH',
    help="Change the location of  whois' permanent configurations.")
set_option.add_argument('--database-file', metavar='PATH',
    help='Set the path and name of the database.')
set_option.add_argument('--logging-file', metavar='PATH',
    help="Change the location of whois' log.")
set_option.add_argument('--logging-level', metavar='STR',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help="Set the level at which whois' will write to its log.")
set_option.add_argument('--table-name', metavar='NAME',
    help='Create the table of the given name in the \033[32;1mdatabase-file\033[0m.')
set_option.add_argument('--tail-nlines', metavar='INT', dest='nlines',
    help='Set how many lines to parse from \033[32;1mlog-file\033[0m at once.')
set_option.add_argument('--user-dir', metavar='PATH',
    help='Set the path where `whois` writes its file.')


#===============================================================================
# CONSTANTS
#===============================================================================
# Create the files and directories we need in order to run.

WHOISHOME = join(PKGPATH, '.whois')
if not exists(WHOISHOME):
    mkdir(WHOISHOME)

CONF = join(WHOISHOME, 'whois.conf')
LOG = join(WHOISHOME, 'whois.log')

header = f"# Configuration file for `whois', generated on {yyyymmdd.timedatestamp()}\n"
#header= '# Configuration file for whois. Created: {:%F %I:%M%p}\n'.format(datetime.now())
if not exists(CONF):
    with open(CONF, mode='a') as conf:
        conf.write(header)

if not exists(LOG):
    with open(LOG, mode='a') as log:
        conf.write(header)

#===============================================================================
# Parse configs & args.
#===============================================================================

with open(CONF, mode='r') as conf:
    CONFIGS = conf.read()

# Remove the commented lines.
CONFIGS = [ln for ln in CONFIGS.splitlines() if not ln.lstrip().startswith('#')]


# ArgumentParser obj -> dict.
CONFIGS = vars(set_option.parse_args(CONFIGS))
#print(CONFIGS)

# Execute func here, or ignore it by checking the types of all the attrs.
# Otherwise, we'll get an error when sanitizing the strings.
del CONFIGS['func'] # set-option sub-command
#print(CONFIGS)

# Explicitly exclude None values, the defaults, which will "overwrite" the
# succeeding values (that may be given on the command-line). Sanitize any
# quoted values in the config, since there is ambiguity in whether string
# values can and should be quoted there (they shouldn't, but on the CLI they
# often are). We will convert integer types later during function calls.

CONFIGS = {k:v.strip('"\'') for k,v in CONFIGS.items() if v is not None}
CONFIGS.update(CONFIGS)
#print(CONFIGS)


# Parse command-line args.
args = parser.parse_args()

#if args.cmd:
# Call set-option or init-config


# Explicitly exclude None values (or they'll override DEFAULTS & CONFIGS).
CONFIGS.update({k:v for k,v in vars(args).items() if v is not None})


# Remove the ArgumentParser object from the Namespace. Run set_option()
# here. We get the KeyError, only when set-option cmd is not present/used.
try: del CONFIGS['func'] # set-option
except KeyError:
    pass


# Create the Namespace.
opts = Options(CONFIGS)


# Convert some strings that are supposed to be ints.
opts.port = int(opts.port)
opts.bufsz = int(opts.bufsz)
opts.nlines = int(opts.nlines)

#===============================================================================
# Notes:
#
# This doesn't work. Why?
#for i in [opts.port, opts.bufsz, opts.nlines]:
#    try:
#        i = int(i)
#        print(f'Successfully converted {i} to int')
#    except ValueError:
#        print(f'{i} raised an exception')
#        pass
#print(type(opts.port))
#print(type(opts.bufsz))
#print(type(opts.nlines))
#===============================================================================
# TODO
# * Use tables to print Options str & repr.
#===============================================================================
