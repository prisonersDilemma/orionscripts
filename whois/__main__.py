#!/usr/bin/env python3.6

__date__ = '2017-11-15'
__package__ = 'whois'
__version__ = (0,0,1)

from os.path import exists, expanduser, join
from re import sub
from sys import stdout, stderr, exit

from __init__ import *
import config # Will execute the script during import.
#from config import *

#===============================================================================
# Finish processing the args and opts, and create any necessary files.

# Parse the config file: '.whois.conf'. Remove the commented lines.
with open(config.CONFIGFILE, mode='r') as conf:
    CONFIGS = conf.read().splitlines()
CONFIGS = [line for line in CONFIGS if not line.lstrip().startswith('#')]
CONFIGS = vars(config.set_option.parse_args(CONFIGS)) # ArgumentParser obj -> dict.
del CONFIGS['func'] # set-option

# Explicitly exclude None values, and sanitize any values that may be quoted.
CONFIGS = {k:v.strip('"\'') for k,v in CONFIGS.items() if v is not None}
config.ARGS.update(CONFIGS)

# Parse command-line args.
args = config.parser.parse_args()

# Explicitly exclude None values.
config.ARGS.update({k:v for k,v in vars(args).items() if v is not None})
try:
    del config.ARGS['func'] # set-option
    # Run set_option() here. We get the KeyError, only when set-option cmd is
    # not present/used.
except KeyError:
    pass

# Create the Namespace.
opts = config.Options(config.ARGS)


# Update the logging-level (if necessary). #config.getLevelName()
level = config.LOGLEVELS.get(opts.logging_level)
if level and (level != config.logger.level):
    config.logger.setLevel(level)
    config.logger.info(f'logger: updated logging_level to {opts.logging_level!s} '
                       f'({config.logger.level})')

# Indent each option=value when writing to the log, to make it easier to read.
logopts = ''.join((_.join(['  ', '\n']) for _ in str(opts).splitlines())).rstrip('\n') # strip the last newline.
config.logger.debug(f'`{__package__}` running with options:\n{logopts}')
#===============================================================================


# Assemble targets dict from the Splunk log.
trgts = gettargets(opts.log_file, opts.date)
config.logger.info(f'trgts found: {len(trgts)}')


# Assemble targets query from the dict and call nacat.
output = nacat(opts.hostname, opts.port, join_msg(*trgts))
config.logger.debug(f'`nacat` returned with an output string of len: {len(output)}')


# Ignore the first line in the output, which is a header. Not all lines
# will have all elements. Parse the lines. Normalize the data elements.
# Remove duplicates automatically done by dict.update). Add them to trgts.
output_lines = output.splitlines()
header_line  = output_lines[0]
config.logger.info(f'presumed header line in the output from `nacat`: {header_line}')

for line in output_lines[1:]: # Skip the first line; the header.
    try:
        asn, ipaddr, name_cntry = line.split('|')
        asn = asn.strip()
        ipaddr = ipaddr.strip()
        name_cntry = name_cntry.strip()
        #name_cntry = sub(r'(, |,)', ' - ', name_cntry) # squeeze?
        try:
            name, cntry = name_cntry.rsplit(',', 1)
            name = sub(r'(, |,)', ' - ', name)
        except ValueError:
            config.logger.warning(f'Exception raised parsing `nacat` output for '
                           'secondary values "name", "cntry":\n{line}\n'
                           'Resorting to defaults.')
            name = name_cntry if name_cntry else ''
            cntry = ''

        trgts[ipaddr].update({'ASN': f'AS{asn}', 'name': name, 'country': cntry}) # 'country': cntry})

    except ValueError:
        config.logger.warning(f'Exception raised parsing `nacat` output for primary '
                       'values "asn", "ipaddr", "name_cntry":\n{line}\n'
                       'This item will not be updated in the database.')


# Daily List. Data is changed daily.
# Format data. Append to csv.
# No header, with following format: name - country,ASN,ipaddr,timestamp
config.logger.info(f'Writing to daily list file: {opts.list_file}')
with open(opts.list_file, mode='w') as f:
    for trgt in trgts:
        line = ','.join((
                         trgts[trgt]['name'],
                         trgts[trgt]['country'],
                         trgts[trgt]['ASN'],
                         trgt,
                         trgts[trgt]['timestamp']))
        config.logger.debug(f'Writing to daily list file: {line}')
        f.write(f'{line}\n')


# If no '.db' extension, append.
opts.database_file = opts.database_file if opts.database_file.endswith('.db') else ''.join([opts.database_file, '.db'])
if not exists(opts.database_file):
    create_database(opts.database_file)
    config.logger.info(f'database: {opts.database_file} created.')

    # Only create the table if we have data, and make KEYS dynamic, gotten from
    # the data.
    KEYS = ['ASN', 'IPADDR', 'NAME', 'COUNTRY', 'TIMESTAMP']
    # Create a table (and the database), only if they do not exist.
    create_table(opts.database_file, KEYS, opts.table_name)
    config.logger.info(f'table {opts.table_name} created if it does not exist.')


# Compose and insert the records (rows) into the database table.
config.logger.info(f'inserting {len(trgts)} records into table: {opts.table_name}')
for trgt in trgts:
    VALUES = (trgts[trgt]['ASN'],
              trgt,
              trgts[trgt]['name'],
              trgts[trgt]['country'],
              trgts[trgt]['timestamp'])
    config.logger.debug(f'inserting values: {VALUES}')
    insert_record(opts.database_file, VALUES, opts.table_name)

#===============================================================================
# "MASTER list"
# Add to master list/database: append to the csv file:  name - cntry,asn,ip,timestamp
# These are the columns in the master list. Remember, it's comma-separated.
# So this first part is one column and this column is separated by dashes.
# ....................
# ASN / Name / Country,ASN,IP Address ,Date First Seen,ASN Lookup,IP Address Lookup,Country
#with open(MASTER, mode='a') as m:
#    m.write()
#===============================================================================
