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

import unittest

from funpy.maybe import Just, Nothing

class TestMonadDiv(unittest.TestCase):
    '''Test Maybe division, the most obvious example'''
    def test_correct(self):
        self.assertEquals(Just(10) / 2, Just(5))

    def test_zero(self):
        self.assertEquals(Just(10) / 0, Nothing)

    def test_multi_level(self):
        self.assertEquals(Just(10) / 5 / 2, Just(1))
        self.assertEquals(Just(10) / 2 / 0 / 2, Nothing)

    def test_nothing(self):
        self.assertEquals(Nothing / 5, Nothing)
        self.assertEquals(Nothing / 0, Nothing)


class TestSpecialFunctions(unittest.TestCase):
    def test_str(self):
        self.assertEquals(str(Just('test')), 'Just(test)')

    def test_repr(self):
        class T:
            def __repr__(self): return 'test'

        self.assertEquals(repr(Just(T())), 'Just(test)')

    def test_unicode(self):
        self.assertEquals(unicode(Just('abc')), u'Just(abc)')

    def test_nothing_str(self):
        self.assertEquals(str(Nothing), 'Nothing')
        self.assertEquals(repr(Nothing), 'Nothing')
        self.assertEquals(unicode(Nothing), u'Nothing')

    def test_just_eq(self):
        o = object()
        self.assertEquals(Just(o), Just(o))
        self.assertNotEquals(Just(o), Just(object))
        self.assertNotEquals(Just(o), o)
        self.assertNotEquals(Just(o), Nothing)

    def test_nothing_eq(self):
        self.assertEquals(Nothing, Nothing)
        self.assertNotEquals(Nothing, Just(object()))
        self.assertNotEquals(Nothing, object())

    def test_hash(self):
        o = object()
        self.assertEquals(hash(Just(o)), hash(o))


class TestNumericFunctions(unittest.TestCase):
    def test_add(self):
        self.assertEquals(Just(10) + 5, Just(15))
        self.assertEquals(Just(10) + Nothing, Nothing)
        self.assertEquals(Nothing + 10, Nothing)
        self.assertEquals(Nothing + Nothing, Nothing)
