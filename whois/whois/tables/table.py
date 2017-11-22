#!/usr/bin/env python3.6
"""
Functions for printing columns, rows, and tables.
"""

def ceildiv(x,y):
    """Return the ceiling of x / y. Useful for calculating columns in a table."""
    return -(-x//y)

def longest(lst):
    """Return the length of the longest item in a list."""
    return max((len(i) for i in lst))

def strs(lst):
    return [str(i) for i in lst]

def column(lst):
    """Return a column as a string given a list of items."""
    lst = strs(lst)
    return '\n'.join((i.rjust(longest(lst)) for i in lst))


# ints will need to be converted to stry, in order to apply str methods!
def as_row(lst, widths=None, sep=' ', n=4, align='r'):
    """Given a list, returns a formatted row.

    If widths are provided, they are used for the justification instead of
    the len of each item. By default right justification is used, and sep
    is a space and n is 4, and each column is separated by sep * n.

    The greater of the len of lst or widths will determine the number of
    columns. If widths is None (default), there will be a column for
    every item in lst.

    Any unique string can be given for align.
    """
    sep *= n
    lst = strs(lst)
    alignments = ['center', 'ljust', 'rjust']
    widths = widths if widths else [len(_) for _ in lst]
    align = [_ for _ in alignments if _.startswith(align[0])][0]
    return sep.join(map(lambda x: getattr(x[0], align)(x[1]) ,zip(lst,widths)))


def table(matrix, headers=False):
    """Given a list of lists, each sublist representing a column,
    return a formatted table."""
    rows = []
    col_widths = [longest(col) for col in matrix]
    get_row = lambda m: [_.pop() for _ in m] # bottom up
    while True:
        try: rows.append(as_row(get_row(matrix), widths=col_widths))
        except IndexError:
            break # We are done (at least with that col).

    if headers:
        div = '-' * longest(rows)
        rows.insert(-1, div) # table is inverted; insert the divider
    return '\n'.join(reversed(rows))


if __name__ == '__main__':
    # column tests.
    #s = "An example of how to print a nice, formatted column."
    #print(column(s.split()))
    #print(column(list(range(5))))

    # as_row tests.
    #lst = ['one', 'two', 'three']
    #lst = list(range(5))
    #widths=[3, 3, 3, 3, 3]
    #print(as_row(lst, widths, align='center'))

    # table tests.
    c0 = ['OS', 'Linux', 'Unix', 'crApple', 'doz']
    c1 = ['Rating', 'best', 'great', 'shit', 'worse']
    c2 = ['Cost', 'free', 'proprietary', 'worse than rape','rape']
    print(table([c0, c1, c2], headers=True))
