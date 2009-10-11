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

import operator

class Monad(object):
    __slots__ = tuple()

    def bind(self, fun):
        raise NotImplementedError

    def return_(self, value):
        raise NotImplementedError

    def fail(self, exception):
        raise NotImplementedError


liftM = lambda fun: lambda m: m.bind(lambda x: m.return_(fun(x)))


unary_proxy = lambda fun: \
        lambda self: liftM(lambda x: fun(x))(self)
binary_proxy = lambda fun: \
        lambda self, other: liftM(lambda x: fun(x, other))(self)

class NumericMonadMixin:
    __add__ = binary_proxy(operator.add)
    __sub__ = binary_proxy(operator.sub)
    __mul__ = binary_proxy(operator.mul)
    __floordiv__ = binary_proxy(operator.floordiv)
    __mod__ = binary_proxy(operator.mod)
    __divmod__ = binary_proxy(lambda a, b: ((a - (a % b)) / b, a % b))
    __pow__ = binary_proxy(operator.pow)
    __lshift__ = binary_proxy(operator.lshift)
    __rshift__ = binary_proxy(operator.rshift)
    __and__ = binary_proxy(operator.and_)
    __xor__ = binary_proxy(operator.xor)
    __or__ = binary_proxy(operator.or_)

    __div__ = binary_proxy(operator.div)
    __truediv__ = binary_proxy(operator.truediv)

    __neg__ = unary_proxy(operator.neg)
    __pos__ = unary_proxy(operator.pos)
    __abs__ = unary_proxy(operator.abs)
    __invert__ = unary_proxy(operator.invert)

del unary_proxy, binary_proxy
