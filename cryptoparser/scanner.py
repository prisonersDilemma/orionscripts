#!/usr/bin/env python3.6

import re
import sys
import time

try:
    import httplib2 # Http
except ModuleNotFoundError: #noqa
    pass


class Scanner:

    # Base domainname, removed of any protocol/schema.
    domain = re.compile(r'https?://(?P<addr>[^/]+(/?|$))').search

    def __init__(self, infile, outfile, pattern, cache=None,
                 timeout=None, sleep=None, logger=None, **kwargs):
        """
        infile & outfile are paths
        cache is path to dir
        pattern is a string/regex
        timeout & sleep are ints
        logger is logger obj
        kwargs = http_only=False, https_only=False,
        """
        self.cache = cache
        self.http_only = kwargs.get('http_only') # Should default to false from argparse.
        self.https_only = kwargs.get('https_only') # Should default to false from argparse.
        self.infile = infile
        self.logger = logger
        self.outfile = outfile
        self.pattern = pattern
        self.quietmode = kwargs.get('quietmode')
        self.logger.debug('scanner: during instantiation: pattern: {}'.format(self.pattern))
        self._regex = None
        self.sleep = sleep
        self.timeout = timeout

        #List of protocols we will prepend to every domain/IP and make a request to.
        self.schemas = ['http', 'https']
        if self.http_only:
            self.schemas.remove('https')
        elif self.https_only:
            self.schemas.remove('http')
        if self.logger:
            self.initLog()


    def initLog(self):
        self.logger.debug(
            'New Scanner instance initialized with the following attributes:\n'
            'cache: {}\n'
            'http_only: {}\n'
            'https_only: {}\n'
            'infile: {}\n'
            'logger: {}\n'
            'outfile: {}\n'
            'pattern: {}\n'
            'regex: {}\n'
            'schemas: {}\n'
            'sleep: {}\n'
            'timeout: {}'
            .format(self.cache, self.http_only, self.https_only, self.infile,
                    self.logger.name, self.outfile, self.pattern, self.regex,
                    self.schemas, self.sleep, self.timeout))

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, pattern):
        self._regex = pattern

    # Probably should've just combined this with the regex.setter.
    def compileregex(self):
        self.regex = re.compile(r'{}'.format(self.pattern))
        self.logger.debug('compiled regex: {}'.format(self.regex))
        self.regex = self.regex.search

    def qualifyurl(self, domainname):
        """Return a generator, which is an iterable of *thedomainname* prefixed with
        http:// and https://.
        """
        self.logger.debug('qualifying url.')
        self.logger.debug('qualifyurl: schemas used: {}'.format(self.schemas))
        return ('://'.join((schema,domainname)) for schema in self.schemas)

    def splitdomain(self, url): # Maybe this is better as spliturl?
        """Return the parsed domain-name from a fully qualified URL.

        Example: https://badpackets.net -> badpackets.net

        If the domain-name can't be parsed from the URL, because URL is not
        fully qualified (is not preceded with the protocol, e.g., http://
        or https://), then the URL is returned as-is.
        """
        try:
            domain = self.domain(url).group('addr')
            schema = url.split(domain)[0].rstrip('://')
            self.logger.debug('splitdomain: schema: {}, domain: {}'.format(schema, domain))
            return [schema, domain]
        except AttributeError:
            self.logger.debug('Error parsing domain from url in splitdomain. Returning url: {}.'.format(url))
            return [url]

    def parsecontent(self, content):
        """Return a string if the pattern: CoinHive.Anonymous('HASH');
        is found embedded in *content*, the HTML page source.
        Example:
            CoinHive.Anonymous('oZFH0SLOx5v0DuQug1dqDykUWYnfbEgq');
        ->  oZFH0SLOx5v0DuQug1dqDykUWYnfbEgq
        Returns None if either the pattern: CoinHive.Anonymous('')
        is not found, or the string inside consists of non-alphanumeric
        characters.
        """
        # Leads to an error when there is no content returned, but a connection
        # is able to be made, e.g., a decoding error.
        #self.logger.debug('parsecontent: content snippet:\n{}'.format(content[:100]))
        try:
            # Changed, since I got it working. Could pose a problem. Had to
            # accomodate coinhivehash, and I'm too tired too inspect further.
            match = ''.join(self.regex(content).groups())
            self.logger.debug('parsecontent: regex returned: {}, of type: {}'.format(match, type(match)))
            if match:
                self.logger.debug('parsecontent: successfully parserd a match: {}'.format(match))
            return match
        # Catching TypeError, in case content is None, because getsource timed out.
        except (AttributeError, TypeError):
            self.logger.exception('parsecontent: the regex did not match.')

    # Should I be creating a new Http instance for every URI, and for
    # every schema?
    def getsource(self, url):
        """Return the HTML source code as string from a host at *url*.

        Make a GET requst using httplib2's Http class's request method.
        Convert the binary to string, in utf-8 format. The request method
        demands a "fully qualified url". Thus, if the url is not fully
        qualified, then the http protocol will be used.

        *cache* is an optional argument to a directory path, with a default
        value of '~/Desktop/http_cache'.

        # Should be qualified already now.
        #if not url.startswith('http'): url = ''.join(['http://', url])

        # If None, Python's default is used. See help(httplib2.Http)

        Now returns a tuple of status code (if a request could be made),
        content (if any).
        """
        try:
            h = httplib2.Http(cache=self.cache,
                              timeout=self.timeout,
                              disable_ssl_certificate_validation=True)
            response, content = h.request(url)
            statuscode = response.status
            try:
                content = content.decode('utf-8') if content.decode('utf-8') else None
            except UnicodeDecodeError as decode_err:
                content = None
                self.logger.exception('Cannot decode content at url: {}'
                                 .format(url))
            self.logger.info('target url: {}, received http status code: {}'
                             .format(url, response.status))
            if statuscode is 200:
                return statuscode, content
            elif statuscode is not 200:
                return statuscode, ''
        #(ConnectionRefusedError, TimeoutError): #noqa Socket still in use?.
        except Exception:
            # Automatically prints the traceback on a newline.
            self.logger.exception('Exception raised in getsource:')
            return -1, ''

    def scan(self, url):
        self.logger.debug('current url: {}'.format(url))
        thedomain = self.splitdomain(url)[-1]
        self.logger.debug('current domain: {}'.format(thedomain))
        for n,qualifiedurl in enumerate(self.qualifyurl(thedomain)):
            self.logger.debug('qualified url (#{}): {}'.format(n, qualifiedurl))
            decodedsource = self.getsource(qualifiedurl)
            statuscode, decodedsource = decodedsource[0], decodedsource[1]
            #self.logger.info('decoded source: {}'.format(decodedsource))
            if statuscode is 200: # We were able to make the request.
                pattern_found = self.parsecontent(decodedsource)
                pattern_found = pattern_found if pattern_found else 0 # None if not found (regex AttributeError).
                # Have to return for https & http if not exclusively one or the other.
                return qualifiedurl, pattern_found
            else: # returned either statuscode or -1
                pattern_found = -1 # Could return statuscode.
        return qualifiedurl, pattern_found

    def run(self):
        # Now this can be threaded, but the workers will have to acquire locks on outfile.
        self.compileregex() #compile & set the regex.
        with open(self.infile) as infile, open(self.outfile, 'a') as outfile:
            self.logger.debug('infile:{}, outfile:{}'.format(self.infile, self.outfile))
            for url in (url.strip() for url in list(infile)):
                # output is a tuple of domain, pattern_found
                # pattern_found is 0 if successful request was made, or -1
                #self.splitdomain()
                qualifiedurl, pattern_found = self.scan(url)
                schema, domain = self.splitdomain(qualifiedurl)
                if pattern_found is not 0 and pattern_found is not -1:
                    self.logger.debug('run: pattern_found is not 0 and not -1.')
                    self.logger.debug('run: pattern_found is: {}'.format(pattern_found))
                    output = '{},{},{}'.format(domain,pattern_found,schema)
                    if not self.quietmode:
                        sys.stdout.write(output + '\n')
                else:
                    self.logger.debug('run: pattern_found is 0 or -1: {}'.format(pattern_found))
                    output = '{},{}'.format(domain,pattern_found)
                #log to stdout & logfile if logger
                self.logger.info('result: {}'.format(output))
                outfile.write(output + '\n')
                if self.sleep:
                    time.sleep(self.sleep)
