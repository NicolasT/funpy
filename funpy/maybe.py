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

from .monad import Monad, NumericMonadMixin

class Maybe(Monad, NumericMonadMixin):
    __slots__ = tuple()

    return_ = lambda _, value: Just(value)
    fail = lambda *_: Nothing

    # TODO not implemented raising
    _stringify = None
    __str__ = lambda self: self._stringify(str)
    __repr__ = lambda self: self._stringify(repr)
    __unicode__ = lambda self: self._stringify(unicode)


class Nothing(Maybe):
    __slots__ = tuple()

    bind = lambda self, _: self
    __eq__ = lambda self, other: self is other

    _stringify = lambda *_: 'Nothing'

    __hash__ = lambda *_: 9873983764589L

Nothing = Nothing()


class Just(Maybe):
    __slots__ = ('_value', )

    def __init__(self, value):
        self._value = value

    def bind(self, fun):
        try:
            return fun(self._value)
        except Exception, exc:
            return self.fail(exc)

    def __eq__(self, other):
        if not isinstance(other, Maybe):
            return NotImplemented

        if other is Nothing:
            return False

        return self._value == other._value

    _stringify = lambda self, fun: 'Just(' + fun(self._value) + ')'

    __hash__ = lambda self: hash(self._value)
