#!/usr/bin/env python3.6

from os.path import basename, splitext
from sqlite3 import connect

def create_database(fpath):
    with connect(fpath) as conn:
        return


def conn_and_exec(**kwargs):
    conn = connect(kwargs.get('file'))   # Create & open Connection object
    c = conn.cursor()                            # Create a cursor object
    stmt = kwargs.get('stmt')
    vals = kwargs.get('vals', '')                # Empty string if not present
    c.execute(stmt, vals)                        # Execute the SQL statement
    conn.commit()                                # Saves changes.
    conn.close()                                 # Closes the connection

def create_table(dbpath, keys, name=None):
    name = name if name else gettablename(dbpath)
    cols = ' text, '.join(keys) + ' text'
    sql_stmt = 'CREATE TABLE IF NOT EXISTS ' + name + ' (' + cols + ')'
    conn_and_exec(file=dbpath, stmt=sql_stmt)

def insert_record(dbpath, values, name=None):
    name = name if name else gettablename(dbpath)
    n = len(values) # Get from table, or still could cause an error.
    sql_stmt = f' {name} '.join(['INSERT INTO',  'VALUES'])
    sql_stmt = ' '.join([sql_stmt, ('?,'*(n-1) + '?').join(['(', ')'])])
    #print(f'insert_record sql_stmt: {sql_stmt}')
    conn_and_exec(file=dbpath, stmt=sql_stmt, vals=values)

def gettablename(dbpath):
    return splitext(basename(dbpath))[0]

#if __name__ == '__main__':
#    dbpath = '/home/na/git/prisonersDilemma/orionscripts/whois/tests/samples-micro/micro.db'
#    name = 'micro'
#    keys = ['ip', 'asn', 'name', 'country']
#    create_table(dbpath, keys)
#    values = ''
#    insert_record(dbpath, values)
