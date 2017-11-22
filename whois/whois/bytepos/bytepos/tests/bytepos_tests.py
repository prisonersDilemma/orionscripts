#!/usr/bin/env python3.6

from unittest import TestCase


if __name__ == '__main__':
    pass

# This is what I set out to emulate in both directions as an abstraction.
#class ReverseBytePosition:
#    def __init__(self, fsize, bufsz):
#        if not fsize >= bufsz:
#            raise ValueError(f'ReverseAttributeError: fsize < bufsz')
#        self.bufsz = bufsz
#        self.prv = fsize
#        self.cur = fsize
#
#    def __repr__(self):
#        return f'ReverseBytePosition(prv={self.prv}, cur={self.cur}, nxt={self.nxt}, bufsz={self.bufsz})'
#
#    def __str__(self):
#        return str(self.cur)
#
#    @property
#    def nxt(self):
#        return self._delta()
#
#    def __iter__(self):
#        return self
#
#    def __next__(self):
#        self.prv = self.cur
#        self.cur = self.nxt
#        if self.prv is 0:
#            raise StopIteration
#        return self
#
#    def _delta(self):
#        """Return the size of the next readable buffer."""
#        delta = self.cur - self.bufsz
#        return delta if delta > 0 else 0

    # Samples
    # fsize | bufsz
    # 8751, 1024
    # 408, 64

    #rbp = ReverseBytePosition(408, 64)
    #bp = BytePosition(408,64,direction='backward')

    #for pos in rbp:
    #    print(f'{pos!r}')
    #print(f'After: {rbp!r}')

    #print(f'Before: {rbp!r}')
    #print(f'Before:        {bp!r}')

    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #next(rbp)
    #print(f'Next: {rbp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')


    #bp = BytePosition(408,64,direction='forward')
    #print(f'Before:        {bp!r}')
    #next(bp)
    #print(f'Next:        {bp!r}')
    #for pos in bp:
    #    print(f'{pos!r}')
    #print(f'After: {bp!r}')


    #rbp = RevBytePosition(408,64)
    #print(f'Before: {rbp!r}')
    #for pos in rbp:
    #    print(f'{pos!r}')
    #print(f'After: {rbp!r}')
