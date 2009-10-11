# funpy, a library for functional programming in Python
#
# Copyright (C) 2009 Nicolas Trangez  <eikke eikke com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1
# of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301  USA

'''Cons list implementation'''

import operator

swap_args = lambda fun: lambda a, b: fun(b, a) #pylint: disable-msg=C0103,E0601
swap_args.__doc__ = '''
Create a function which will call the original with swapped arguments

:param fun: function to call
:type fun: callable

:return: function which will call `fun` using swapped arguments
:rtype: callable
'''.strip()

const = lambda value: lambda *_: value #pylint: disable-msg=C0103,E0601
const.__doc__ = '''
Create a function which will always return the same value

:param value: value to return
:type value: object

:return: function which always returns `value`
:rtype: callable
'''.strip()

def not_implemented(*_):
    '''Raise a NotImplementedError'''
    raise NotImplementedError

def assert_not_reached(*_):
    '''Raise an exception when this code is reached'''
    raise Exception('This should not be reached')

class ConsCell(object): #pylint: disable-msg=R0903
    '''Base class for Cons cell implementations'''
    __slots__ = '_head', '_tail',

    def __init__(self, head, tail):
        '''Initialize a new cell

        :param head: value of head element
        :type head: object
        :param tail: tail element of cons list
        :type tail: ConsCell
        '''
        self._head = head
        self._tail = tail

    head = property(operator.attrgetter('_head'), doc='Head value')
    tail = property(operator.attrgetter('_tail'), doc='Tail cell')

    __nonzero__ = const(True)
    __lshift__ = lambda self, other: type(self)(other, self)

    _stringify = not_implemented
    #pylint: disable-msg=W0212
    __str__ = lambda self: self._stringify(str)
    __unicode__ = lambda self: self._stringify(unicode)
    __repr__ = lambda self: self._stringify(repr)
    #pylint: enable-msg=W0212

    __len__ = not_implemented
    __getitem__ = not_implemented
    __contains__ = not_implemented
    __iter__ = not_implemented
    __eq__ = not_implemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result

        return (not result)

    empty = property(const(False), doc='Cell is empty (Nil)')


class Nil(ConsCell): #pylint: disable-msg=R0903
    '''Base class for Nil cell types'''
    __slots__ = tuple()
    
    _CONS = property(assert_not_reached, doc='Cell constructor')

    __init__ = const(None)

    def __getitem__(self, _):
        raise IndexError

    head = property(assert_not_reached)
    tail = property(assert_not_reached)

    __nonzero__ = const(False)
    __len__ = const(0)
    __contains__ = const(False)

    __eq__ = lambda self, other: self.empty is getattr(other, 'empty', None)
    __hash__ = const(94598459345L)

    _stringify = const('Nil')

    __iter__ = lambda _: iter(tuple())

    #pylint: disable-msg=W0212
    __lshift__ = lambda self, other: self._CONS(other, self)
    #pylint: enable-msg=W0212

    empty = property(const(True), doc='Cell is empty (Nil)')


# Some utility functions
#pylint: disable-msg=C0103,E0601
from_iterable = lambda unit, zero: lambda iterable: reduce(swap_args(unit),
                                                     reversed(iterable), zero)
#pylint: enable-msg=C0103,E0601
from_iterable.__doc__ = '''
Helper to create a function which creates a Cons list from any iterable

:param unit: Unit function of Cons implementation
:type unit: ConsCell
:param zero: Nil cell value
:type zero: Nil

:return: function which creates a Cons list from an iterable
:rtype: callable
'''.strip()


# Iterative implementation
class IterativeConsCell(ConsCell): #pylint: disable-msg=R0903
    '''Cons list implementation using iterative algorithms'''
    def __len__(self):
        len_ = 1

        tail = self.tail
        while not tail.empty:
            len_ += 1
            tail = tail.tail

        return len_

    def __getitem__(self, key):
        if not isinstance(key, (int, long)):
            raise TypeError

        if key < 0:
            key = len(self) - abs(key)
            if key < 0:
                raise IndexError

        cell = self
        for _ in xrange(key):
            if cell.empty:
                raise IndexError

            cell = cell.tail

        if cell.empty:
            raise IndexError

        return cell.head

    def __contains__(self, item):
        cell = self

        while not cell.empty:
            if cell.head == item:
                return True

            cell = cell.tail

        return False

    def __iter__(self):
        cell = self
        while not cell.empty:
            yield cell.head
            cell = cell.tail

    def __eq__(self, other):
        if not hasattr(other, 'head') or not hasattr(other, 'tail'):
            return NotImplemented

        cell1 = self
        cell2 = other

        while not cell1.empty and not cell2.empty:
            if cell1.head != cell2.head:
                return False

            cell1 = cell1.tail
            cell2 = cell2.tail

            if cell1.empty != cell2.empty:
                return False

        return True

    def _stringify(self, fun):
        '''Create string-representation of the list'''
        def partim_generator():
            '''Create string-representation of one list item'''
            cell = self
            while not cell.empty:
                yield fun('cons(%s, ') % fun(cell.head)
                cell = cell.tail

            yield fun(cell)

        return fun('%s%s') % (''.join(partim_generator()), ')' * len(self))

    def __hash__(self):
        hash_ = 1

        cell = self
        while not cell.empty:
            hash_ = hash_ * 31 + hash(cell.head)
            cell = cell.tail

        hash_ = hash_ * 31 + hash(cell)
        return hash_

class IterativeNil(Nil): #pylint: disable-msg=R0903
    '''Nil value to construct iterative Cons lists'''
    _CONS = IterativeConsCell
IterativeNil = IterativeNil() #pylint: disable-msg=C0103

#pylint: disable-msg=C0103
iterative_from_iterable = from_iterable(IterativeConsCell, IterativeNil)
#pylint: enable-msg=C0103
iterative_from_iterable.__doc__ = \
        'Create an iterative Cons list from an iterable'


# Recursive implementation
class RecursiveConsCell(ConsCell): #pylint: disable-msg=R0903
    '''Cons list implementation using recursive algorithms'''
    def __len__(self):
        return len(self.tail) + 1

    def __getitem__(self, key):
        if not isinstance(key, (int, long)):
            raise TypeError

        if key < 0:
            key = len(self) - abs(key)
            if key < 0:
                raise IndexError

        return self.head if key == 0 else self.tail[key - 1]

    __contains__ = lambda self, item: (self.head == item) or (item in self.tail)

    def __iter__(self):
        yield self.head
        for item in iter(self.tail):
            yield item

    def __eq__(self, other):
        if not hasattr(other, 'head') or not hasattr(other, 'tail'):
            return NotImplemented

        return (self.head == other.head) and (self.tail == other.tail)

    _stringify = lambda self, fun: fun('cons(%s, %s)') % \
                                    (fun(self.head), fun(self.tail))

    __hash__ = lambda self: 31 * hash(self.tail) + hash(self.head)

class RecursiveNil(Nil): #pylint: disable-msg=R0903
    '''Nil value to construct recursive Cons lists'''
    _CONS = RecursiveConsCell
RecursiveNil = RecursiveNil() #pylint: disable-msg=C0103

#pylint: disable-msg=C0103
recursive_from_iterable = from_iterable(RecursiveConsCell, RecursiveNil)
#pylint: enable-msg=C0103
recursive_from_iterable.__doc__ = \
        'Create a recursive Cons list from an iterable'
