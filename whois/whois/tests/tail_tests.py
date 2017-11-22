#!/usr/bin/env python3.6

__date__ = '2017-11-14'
__version__ = (0,0,1)


from unittest import TestCase

import whois


# Path to a simple test file to tail: 11 lines long
fpath = '/home/na/git/prisonersDilemma/orionscripts/whois/tests/samples-micro/tail-simple'


class TailTester(TestCase):


    def test_Tail_iter(self):
        # tailing 2 at a time
        test_chunks = [c for c in whois.Tail(fpath, nlines=2, bufsz=128)]
        ctrl_chunks = ['line ten\nline eleven\n', 'line eight\nline nine\n',
                       'line six\nline seven\n', 'line four\nline five\n',
                       'line two\nline three\n', 'line one\n']
        self.assertEqual(test_chunks, ctrl_chunks)


    def test_Tail_next(self):
        tail = whois.Tail(fpath, nlines=2, bufsz=128)

        last_two = 'line ten\nline eleven\n'
        self.assertEqual(next(tail), last_two)

        next_two_1 = 'line eight\nline nine\n'
        self.assertEqual(next(tail), next_two_1)

        next_two_2 = 'line six\nline seven\n'
        self.assertEqual(next(tail), next_two_2)

        next_two_3 = 'line four\nline five\n'
        self.assertEqual(next(tail), next_two_3)

        next_two_4 = 'line two\nline three\n'
        self.assertEqual(next(tail), next_two_4)

        last_one = 'line one\n'
        self.assertEqual(next(tail), last_one)


    def test_Tail_StopIteration(self):
        with self.assertRaises(StopIteration) as cm:
            tail = whois.Tail(fpath, nlines=2, bufsz=128)
            for i in range(7):
                next(tail) # Should be exhausted after 6 iterations.
        the_exception = cm.exception


    def test_Tail_more_lines_than_exist(self):
        # Only 11 lines in file, requesting the last 100, so all the lines
        # will be returned at once as a string.
        test_chunks = [c for c in whois.Tail(fpath, nlines=100, bufsz=128)]
        ctrl_chunks = [('line one\nline two\nline three\nline four\nline five\n'
                        'line six\nline seven\nline eight\nline nine\nline ten\n'
                        'line eleven\n')]
        self.assertEqual(test_chunks, ctrl_chunks)


    # test that I can request more lines than the bufsz can handle

    #def test_tail_gen(self):
    #    for lines in tail(logfile, nlines=2):
    #        print(lines, end='')

    #def test_tail_gen_next(self):
    #print(next(tail(logfile, nlines=2)), end='')

    #import date
    #def myfilterfunc(chunk):
    #    matches = []
    #    for line in chunk.splitlines():
    #        try:
    #            if date.DATE(line).group('date') == date.yyyymmdd(dd='10'):
    #                matches.append(line)
    #        except AttributeError:
    #            pass
    #    return matches

    ## Ends up returning everything in a list.
    #print('Filtering for 2017-11-10.')
    #for match in tfilter(fpath=logfile, nlines=20 func=myfilterfunc):
    #    print(match)


if __name__ == '__main__':
    TailTester()
    # $ python3.6 -m unittest tests.tail_tests.py
