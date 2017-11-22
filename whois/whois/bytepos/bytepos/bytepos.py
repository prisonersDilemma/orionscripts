#!/usr/bin/env python3.6


#import abc

class BytePosition:

    #__metaclass__ = abc.ABCMeta

    # Hide from subclasses.
    DIRECTIONS = { 'reverse': getattr(int, '__sub__'), 'forward': getattr(int, '__add__'), }

    # I don't think I can make this an abstraction because I need access to prv, cur, etc,
    # at least in order to print the object.

    #@abc.abstractmethod
    def __init__(self, fsize, bufsz, direction):

        if not isinstance(fsize, int):
            raise TypeError(f'{__class__.__name__}: expected int, got type {type(fsize)}')
        elif not isinstance(bufsz, int):
            raise TypeError(f'{__class__.__name__}: expected int, got type {type(bufsz)}')
        elif not direction in self.DIRECTIONS:
            raise AttributeError(f'{__class__} has no attribute {direction!s}')
        elif not fsize >= bufsz: #bufsz = fsize # read it all
            raise ValueError(f'{__class__.__name__}: fsize < bufsz')

        # Don't need to keep fsize as a property, but may be useful.
        self.fsize = fsize
        self.bufsz = bufsz

        # Type of incrementing (+/-) to do with respect to 'direction'.
        self.inc = self.DIRECTIONS[direction] # callable

        # self.inc.__name__ == '__add__' is effectively the same as comparing
        # direction == 'forward', but immutable (whereas, I may change the
        # values of the variables, e.g. 'backward' to 'reverse'). Likewise with
        # direction == 'backward' and self.inc.__name__ == '__sub__'

        # Maximum value to signal EOF.
        self.max = self.fsize if self.inc.__name__ == '__add__' else 0

        # Type of comparisons to make with respect to 'direction'.
        self.cmp = getattr(int, '__lt__') if self.inc.__name__ == '__add__' else getattr(int, '__gt__')

        # Dependent on direction.
        self.prv = self.fsize if self.inc.__name__ == '__sub__' else 0
        self.cur = self.fsize if self.inc.__name__ == '__sub__' else 0

        # Dependent on direction.
        self._nxt = self.inc(self.cur, self.bufsz) if self.cmp(self.inc(self.cur, self.bufsz), self.max) else self.max


    #@abc.abstractclassmethod # Print the subclass name.
    def __repr__(self):
        """Return a view of *prv*, *cur*, and *nxt* positions, and *bufsz*."""
        return f'{__class__.__name__}(prv={self.prv}, cur={self.cur}, nxt={self.nxt}, bufsz={self.bufsz})'

    def __str__(self):
        """Return the current position *cur* as str."""
        return str(self.cur)

    #@abc.abstractmethod
    def __iter__(self):
        """Yield the __next__ values."""
        return self

    #@abc.abstractmethod # print subclass name instead of BytePosition in StopIteration
    def __next__(self):
        """'Increment' positions relative to *bufsz*, with respect to
        *direction* till 'EOF'.

        Positions are yielded, in increments or decrements, corresponding to
        *direction*, of *bufsz* till *fsize* is consumed. If *fsize* is not
        evenly divisible by *bufsz*, the last yield will be the remainder.
        """
        self.prv = self.cur
        self.cur = self.nxt
        if self.prv is self.max:
            raise StopIteration(f'{__class__.__name__}: EOF reached')
        return self

    @property
    def nxt(self):
        """Dynamically return the next position."""
        return self._delta()

    #@abc.abstractmethod # Hide from subclasses. still available to subs
    def _delta(self):
        delta = self.inc(self.cur, self.bufsz)
        return delta if self.cmp(delta, self.max) else self.max



class RevBytePosition(BytePosition):
    """Return an object capable of calculating and tracking the current,
    previous, and next byte positions of a file size, for a given buffer
    size, as well as the next readable buffer size, *delta*, from its
    current position. All of this is applied in reverse (working from the
    'bottom' or 'end' of the file to the 'top' or 'beginning'."""

    def __init__(self, *args, **kwargs): # fsize, bufsz
        super(RevBytePosition, self).__init__(direction='reverse', *args, **kwargs)
        #__class__.__name__ =


class FwdBytePosition(BytePosition):
    def __init__(self, *args, **kwargs): # fsize, bufsz
        super(FwdBytePosition, self).__init__(direction='forward', *args, **kwargs)



#===============================================================================
# Notes:

# I'm trying to emulate the behavior of this class in an abstract class that
# can do "forward" and "backward".

# Do Reverse or Regular.

# 'Offset' instead of 'Position'?

# Could use same methods for forward & backward, by inverting the values of
# backward. e.g., instead of going from fsize to 0, go from 0 to fsize by -delta

# 'backward' -> sub -> gt max (0)
# 'forward'  -> add -> lt max (fsize)
#===============================================================================
