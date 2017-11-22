#!/usr/bin/env python3.6
"""Incrementally "walk" backwards through a file, reading "blocks" of bufsz,
yielding chunks of nlines."""
__date__ = '2017-11-20'
__version__ = (0,1,0)

from os import SEEK_END, SEEK_CUR, stat
from os.path import exists
#from bytepos import ReverseBytePosition

from logging import basicConfig, getLogger
basicConfig(filename='tail.log',
            level=10, # INFO; defines the root logging level
            format='%(message)s',
            #datefmt='%I:%M:%S%p',
            filemode='w') # Overwrite existing logs.
logger = getLogger(__name__)
logger.setLevel('DEBUG') # str -> int


class Tail:
    def __init__(self, fpath, nlines=10, bufsz=1024, encoding='utf-8', newline=b'\n'):
        assert (isinstance(bufsz, int) and
                isinstance(encoding, str) and
                isinstance(nlines, int) and
                exists(fpath))

        self.nlines = nlines
        self.encoding = encoding
        self.newline = newline
        self._stat = stat(fpath)
        self.stream = open(fpath, mode='rb')
        bufsz = bufsz if self._stat.st_size > bufsz else self._stat.st_size
        self.pos = ReverseBytePosition(self._stat.st_size, bufsz)
        self.buffer = b''

    def __repr__(self):
        """Return information on the current buffer and file position."""
        return 'Tail(ppos={}, cpos={}, npos={}, bufsz={}, buflen={})'.format(
                self.pos.prv, self.pos.cur, self.pos.nxt, self.pos.bufsz, len(self.buffer))

    def __str__(self):
        """Return the current buffer, decoded."""
        return self.buffer.decode(self.encoding)

    def __del__(self):
        """Have Python close the stream during garbage collection."""
        #logger.debug('Closing stream.')
        if not self.stream.closed:
            print('Closing stream.') # Happens 3x, regardless.
            self.stream.close()

    def __iter__(self):
        """Yield chunks of nlines till the file is consumed, whence the final
        chunk will be the remaining lines."""
        return self

    def __next__(self):
        """Return a chunk of nlines."""
        if self.buffer is None:
            logger.debug('Buffer is empty. Raising StopIteration.')
            raise StopIteration('Tail: buffer is empty')

        for pos in self.pos:
            logger.debug('%r', self)
            self.stream.seek(pos.cur)
            buf = self.stream.read(pos.delta()) + self.buffer

            if len(self.buffer) is 0:
                self.buffer = buf.rstrip(self.newline)
                input('\033[31;1mStripping a newline.\033[0m')
                logger.debug('Stripped a newline from the buffer.')
            else: self.buffer = buf

            #n = self.buffer.count(self.newline)
            #print(f'\033[31;1mNumber of newlines in buffer before chunk: {n}\033[0m')
            chunk = self.buffer.rsplit(self.newline, self.nlines)
            input(f'\033[31;1mLength of chunk: {len(chunk)}\033[0m')
            if len(chunk) != (self.nlines + 1):
            #if len(chunk) is not (self.nlines + 1):
                logger.debug('Chunk len (%s) is not nlines+1 (%s). Continuing.', len(chunk), self.nlines + 1)
                continue

            self.buffer, nlines = chunk[0], chunk[-self.nlines:]
            # This is actually faster than a listcomp!
            chunk = self.newline.join(nlines).decode(self.encoding).splitlines()
            #print(f'\033[31;1mLength of the chunk we are about to return: {len(chunk)}\033[0m')
            logger.debug('Returning chunk of len %s', len(chunk))
            return chunk

        # Somehow, a line is lost here. Does it possibly have anything to do with the line
        # we initially removed? Though this doesn't happen with the other file(s). And the line
        # is there beforehand. I need more tests with say a chunk that ends with a few blank lines.
        # I think those lines at the end of the uppermost chunk, which are nothing but newlines,
        # are getting merged together as empty string.

        #nlines = self.buffer.rsplit(self.newline, self.nlines)
        nlines = self.buffer.splitlines()
        logger.debug(f'Len of final nlines, before chunk: {len(nlines)}. See if a line is lost in the translation from this...')
        self.buffer = None
        chunk = self.newline.join(nlines).decode(self.encoding).splitlines()
        logger.debug(f'...to this: len of chunk {len(chunk)}')
        #print(f'\033[31;1mLength of the chunk we are about to return: {len(chunk)}\033[0m')
        #logger.debug('Returning chunk of len %s', len(chunk))
        return chunk
