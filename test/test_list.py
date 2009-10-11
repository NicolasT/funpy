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

'''Tests for Cons lists'''

import new
import unittest
import operator

from funpy.cons import ConsCell
from funpy.cons import IterativeConsCell, IterativeNil, iterative_from_iterable
from funpy.cons import RecursiveConsCell, RecursiveNil, recursive_from_iterable

class TestIterative:
    '''Base class for tests testing the iterative Cons implementation'''
    zero = IterativeNil
    unit = IterativeConsCell

    from_iterable = staticmethod(iterative_from_iterable)

class TestRecursive:
    '''Base class for tests testing the recursive Cons implementation'''
    zero = RecursiveNil
    unit = RecursiveConsCell

    from_iterable = staticmethod(recursive_from_iterable)


def case(test):
    '''Create iterative and recursive tests from a given case

    :param test: testcase implementation
    :type test: `unittest.TestCase`

    :return: iterative and recursive testcases
    :rtype: (class, class)
    '''
    types = (
        ('Iterative', TestIterative, ),
        ('Recursive', TestRecursive, ),
    )
    suffix = test.__name__[len('Test'):]

    return [new.classobj('Test%s%s' % (type_, suffix),
                         (test, unittest.TestCase, base, ),
                         dict())
            for (type_, base) in types]


class TestNil:
    '''Test the Nil object'''
    def test_length(self):
        '''Assert length of Nil is 0'''
        self.assertEquals(len(self.zero), 0)

    def test_zero(self):
        '''Assert Nil is False'''
        self.assertFalse(self.zero)

    def test_tolist(self):
        '''Assert list(Nil) equals []'''
        self.assertEquals(list(self.zero), [])

    def test_totuple(self):
        '''Assert tuple(Nil) equals ()'''
        self.assertEquals(tuple(self.zero), tuple())

    def test_equality(self):
        '''Assert Nil is equal to itself and not to a non-Nil object'''
        self.assertEquals(self.zero, self.zero)
        self.assertNotEquals(self.zero, object())

    def test_index(self):
        '''Assert Nil can't be indexed'''
        self.assertRaises(IndexError, lambda: self.zero[0])
        self.assertRaises(IndexError, lambda: self.zero[1])

TestIterativeNil, TestRecursiveNil = case(TestNil)
del TestNil


class TestCons:
    '''Test Cons lists'''
    def test_creation(self):
        '''Make sure a cons list can be created'''
        list_ = self.unit(3, self.unit(2, self.unit(1, self.zero)))
        return list_

    def test_length(self):
        '''Assert the length of a cons list can be calculated correctly'''
        list_ = self.test_creation()
        self.assertEquals(len(list_), 3)

    def test_nonzero(self):
        '''Assert a cons list is nonzero'''
        self.assertTrue(self.test_creation())

    def test_tolist(self):
        '''Assert a cons list can be turned into a correct list'''
        list_ = self.test_creation()
        self.assertEquals(list(list_), [3, 2, 1])

    def test_totuple(self):
        '''Assert a cons list can be turned into a correct tuple'''
        list_ = self.test_creation()
        self.assertEquals(tuple(list_), (3, 2, 1, ))

    def test_iterator(self):
        '''Assert a cons list can be iterated correctly'''
        list_ = self.test_creation()

        iterator = iter(list_)
        result = list()

        for value in iterator:
            result.append(value)

        self.assertEquals(result, [3, 2, 1])

    def test_str(self):
        '''Assert a cons list can be stringified into the expected format'''
        list_ = self.test_creation()

        self.assertEquals(str(list_), 'cons(3, cons(2, cons(1, Nil)))')

    def test_equality(self):
        '''Assert equality testing on cons lists works as expected'''
        self.assertEquals(self.test_creation(), self.test_creation())

        self.assertNotEquals(self.unit(1, self.unit(3, self.zero)),
                             self.unit(2, self.unit(4, self.zero)))

        self.assertNotEquals(
            self.unit(1, self.unit(2, self.unit(3, self.zero))),
            self.unit(1, self.unit(2, self.zero)))

        self.assertNotEquals(
            self.unit(1, self.unit(2, self.zero)),
            self.unit(1, self.unit(2, self.unit(3, self.zero))))

    def test_hash(self):
        '''Assert a consistent hash value of a cons list can be calculated'''
        list1 = self.test_creation()
        list2 = self.test_creation()

        self.assertEquals(hash(list1), hash(list2))

        self.assertNotEquals(hash(list1), hash(self.zero))

    def test_shift(self):
        '''Assert a cons list can be created using '<<\''''
        list1 = self.test_creation()
        list2 = self.zero << 1 << 2 << 3

        self.assertEquals(list1, list2)
        self.assertEquals(list(list2), [3, 2, 1])

    def test_ilshift(self):
        '''Assert a cons list can be extended using '<<=\''''
        list1 = self.test_creation()

        list2 = self.zero
        for i in xrange(1, 4):
            list2 <<= i

        self.assertEquals(list1, list2)

    def test_index(self):
        '''Assert an item can be extracted from a cons list using indexing'''
        list_ = self.test_creation()

        self.assertEquals(list_[0], 3)
        self.assertEquals(list_[-3], 3)
        self.assertEquals(list_[1], 2)
        self.assertEquals(list_[-2], 2)
        self.assertEquals(list_[2], 1)
        self.assertEquals(list_[-1], 1)
        self.assertRaises(IndexError, lambda: list_[3])
        self.assertRaises(IndexError, lambda: list_[4])
        self.assertRaises(IndexError, lambda: list_[-4])

    def test_index_type(self):
        '''Assert only numeric indices can be used on cons lists'''
        list_ = self.test_creation()

        self.assertRaises(TypeError, lambda: list_[object()])

    def test_contains(self):
        '''Assert the 'in' operator works on cons lists'''
        list_ = self.test_creation()
        self.assert_(1 in list_)
        self.assert_(2 in list_)
        self.assert_(3 in list_)
        self.assert_(0 not in list_)
        self.assert_(4 not in list_)

    def test_not_equal(self):
        '''Assert inequality checking of cons lists works as expected'''
        list_ = self.test_creation()

        self.assertNotEqual(list_, [3, 2, 1])
        self.assert_(list_ != [3, 2, 1])

        self.assert_(self.unit(1, self.unit(2, self.zero)) != \
                     self.unit(1, self.zero))

TestIterativeCons, TestRecursiveCons = case(TestCons)
del TestCons


class TestFromIterable:
    '''Test cons list generation from iterables'''
    def test_from_list(self):
        '''Assert a cons list can be created from a list'''
        list1 = [1, 2, 3, 4, 3, 2, 1]
        list2 = self.unit(1, self.unit(2, self.unit(3, self.unit(4, self.unit(3,
                             self.unit(2, self.unit(1, self.zero)))))))

        self.assertEquals(self.from_iterable(list1), list2)

    def test_equality(self):
        '''Assert 2 cons lists created from an iterable are equal'''
        list1 = [1, 2, 3, 4, 5, 6, 4, 2]

        self.assertEquals(self.from_iterable(list1), self.from_iterable(list1))

    def test_inverse(self):
        '''Assert list . from_iterable results in an equal list'''
        list1 = [1, 3, 5, 7, 9, 8, 6, 4, 2]
        list2 = self.from_iterable(list1)
        list3 = list(list2)

        self.assertEquals(list1, list3)

TestIterativeFromIterable, TestRecursiveFromIterable = case(TestFromIterable)
del TestFromIterable


class TestBuiltins:
    def setUp(self):
        self.list_ = self.unit(1, self.unit(2, self.unit(3, self.unit(4,
                               self.unit(5, self.zero)))))

    def test_reduce(self):
        '''Assert reduce works as expected on cons lists'''
        self.assertEquals(reduce(operator.add, self.list_), sum(xrange(1, 6)))

    def test_map(self):
        '''Assert map works as expected on cons lists'''
        fun = lambda iterable: map(lambda a: a * 2, iterable)
        self.assertEquals(fun(self.list_), fun(xrange(1, 6)))

    def test_filter(self):
        '''Assert filter works as expected on cons lists'''
        fun = lambda iterable: filter(lambda p: p % 2 == 0, iterable)
        self.assertEquals(fun(self.list_), fun(xrange(1, 6)))

TestIterativeBuiltins, TestRecursiveBuiltins = case(TestBuiltins)
del TestBuiltins


class TestMixedTypes(unittest.TestCase):
    '''Test equality checking between iterative and recursive cons lists'''
    def test_equality(self):
        '''Assert iterative and recursive cons lists are equal'''
        list1 = range(100)
        list2 = iterative_from_iterable(list1)
        list3 = recursive_from_iterable(list1)

        self.assertEquals(list2, list3)
        self.assertEquals(list3, list2)

        self.assertEquals(list2, iterative_from_iterable(list3))
        self.assertEquals(list3, recursive_from_iterable(list2))

        self.assertEquals(list2, recursive_from_iterable(list2))
        self.assertEquals(list3, iterative_from_iterable(list3))


# This fives us 100% coverage (for now), so why not...
class VoidTest(unittest.TestCase):
    '''Extra testcases'''
    def test_conscell_len(self):
        '''Test ConsCell.__len__ raises a NotImplementedError'''
        self.assertRaises(NotImplementedError,
                          lambda: len(ConsCell(None, None)))


if __name__ == '__main__':
    unittest.main()
