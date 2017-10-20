#!/usr/bin/env python3.6

__date__ = '2017-10-19'
__version__ = (0,0,4)

# Standard Library.
import argparse # ArgumentParser
import os       # path.exists, path.expanduser, path.join, mkdir
import re       # compile, VERBOSE
import shutil   # rmtree
import sys      # stdout.write
import time     # sleep

# Third-party.
try: import httplib2 # Http
except ModuleNotFoundError: #noqa
    sys.stderr.write(
        """\
        cryptoparser: error: Missing module httplib2.
        Try entering `pip3.6 install httplib2` on the command-line,
        or visiting: https://pypi.python.org/pypi/httplib2/0.10.3
        in your browser.
        """)
    sys.exit(1)


# Regular-expressions.
domainstring = re.compile(r'https?://(?P<addr>.*$)').search
coinhivehash = re.compile(
    r""".*CoinHive.Anonymous    # Anything preceeding the literal method call.
        \(                      # Opening paren.
        ('|")                   # Not everyone will have used single quoted strings.
        (?P<hash>\w+)           # The target: an alphanumeric string.
        ('|")                   # Closing quote.
        \)                      # Closing paren.
    """,re.VERBOSE).search


def getsource(url, cache='~/Desktop/http_cache', timeout=None):
    """Return the HTML source code as string from a host at *url*.

    Make a GET requst using httplib2's Http class's request method.
    Convert the binary to string, in utf-8 format. The request method
    demands a "fully qualified url". Thus, if the url is not fully
    qualified, then the http protocol will be used.

    *cache* is an optional argument to a directory path, with a default
    value of '~/Desktop/http_cache'.
    """
    # Should be qualified already now.
    #if not url.startswith('http'): url = ''.join(['http://', url])
    try:
        response, content = httplib2.Http(cache, timeout).request(url.strip())
        return content.decode('utf-8')
    except (ConnectionRefusedError, TimeoutError): #noqa Socket still in use?.
        return

def parsecontent(content):
    """Return a string if the pattern: CoinHive.Anonymous('HASH');
    is found embedded in *content*, the HTML page source.
    Example:
        CoinHive.Anonymous('oZFH0SLOx5v0DuQug1dqDykUWYnfbEgq');
    ->  oZFH0SLOx5v0DuQug1dqDykUWYnfbEgq
    Returns None if either the pattern: CoinHive.Anonymous('')
    is not found, or the string inside consists of non-alphanumeric
    characters.
    """
    try: return coinhivehash(content).group('hash')
    # Catching TypeError, in case content is None, because getsource
    # timed out.
    except (AttributeError, TypeError):
        return

def splitdomain(url):
    """Return the parsed domain-name from a fully qualified URL.

    Example: https://badpackets.net -> badpackets.net

    If the domain-name can't be parsed from the URL, because URL is not
    fully qualified (is not preceded with the protocol, e.g., http://
    or https://), then the URL is returned as-is.
    """
    try: return domainstring(url).group('addr')
    except AttributeError: return url

def qualifyurl(domainname):
    return ('://'.join((schema,domainname)) for schema in ('http', 'https'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='', description='')
    parser.add_argument('infile', help='path to text file containing URLs')
    parser.add_argument('outfile', nargs='?', default=os.path.join(os.path.expanduser('~'), 'Desktop/outfile'),
                        help='path to output destination (default: ~/Desktop/outfile)')
    parser.add_argument('-s', '--slep', type=int, metavar='TIME', default=0,
                        help='time in seconds to delay between each target')
    parser.add_argument('-t', '--timeout', type=int, metavar='TIME', default=None,
                        help='time in seconds to wait before giving up on a host')
    parser.add_argument('-q', '--quiet-mode', dest='quietmode', action='store_true',
                        help='do not print output to stdout')
    args = parser.parse_args()


    # Passed to the Http instance object for storing temporary files.
    cache = os.path.expanduser('~/Desktop/http_cache')
    if not os.path.exists(cache): os.mkdir(cache)
    with open(args.infile) as infile, open(args.outfile, 'a') as outfile:
        for url in [url.strip() for url in list(infile)]:
            thedomain = splitdomain(url)
            for qualifiedurl in qualifyurl(thedomain):
                # thehash is None if getsource caught an exception.
                thehash = parsecontent(getsource(qualifiedurl, cache, args.timeout))
            thehash = thehash if thehash else 0 # None if not found.
            output = '{},{}\n'.format(thedomain,thehash)
            if not args.quietmode: sys.stdout.write(output)
            outfile.write(output)
            time.sleep(args.sleep)
    shutil.rmtree(cache) # Delete the cache+contents.
    if not args.quietmode: sys.stdout.write('Done.\n')
