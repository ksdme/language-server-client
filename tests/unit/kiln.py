"""
    @author ksdme
    Tests the basic kiln module functions
"""
import unittest
from lsc.kiln import *

class TestKiln(unittest.TestCase):
    """
        Basic Kiln Module Tests
        This is not a monolithic test because the
        order of execution doesn't really matter!
    """

    def test_kiln_integer(self):
        """ integer() """

        # integer() as a filter
        lamda = integer()

        self.assertEqual(lamda(val=2), 2)
        self.assertEqual(lamda(val=2.5), Fail)
        self.assertEqual(lamda(val="C"), Fail)

        with self.assertRaises(TypeError):
            lamda()

        # integer() as constant converter
        self.assertEqual(integer("2")(), 2)
        self.assertEqual(integer("-2")(), -2)
        self.assertEqual(integer("2.0")(), 2)

    def test_kiln_string(self):
        """ string() """

        # string() as a filter
        lamda = string()

        self.assertEqual(lamda(val=2), Fail)
        self.assertEqual(lamda(val="hey"), "hey")

        with self.assertRaises(TypeError):
            lamda()

        # string() as constant converter
        self.assertEqual(string(2)(), "2")
        self.assertEqual(string("0.2")(), "0.2")

    def test_kiln_null(self):
        """ null() """

        # null() as a filter
        lamda = null()

        self.assertEqual(lamda(None), None)
        self.assertEqual(lamda("Some"), None)

    def test_kiln_accept_any(self):
        """ accept_any() """

        lamda = accept_any()

        self.assertEqual(lamda(None), None)
        self.assertEqual(lamda("hey"), "hey")
        self.assertEqual(lamda([0, 0]), [0, 0])

    def test_kiln_positive(self):
        """ positive() """

        # positive() as simple filter
        lamda = positive()

        self.assertEqual(lamda(4.5), 4.5)
        self.assertEqual(lamda(-4.5), Fail)

        # positive() as composite filter
        lamda = positive(integer())

        self.assertEqual(lamda(5), 5)
        self.assertEqual(lamda(-5), Fail)
        self.assertEqual(lamda(-5.5), Fail)

    def test_kiln_int_range(self):
        """ int_range() """

        # int_range() as simple filter
        lamda = int_range(0, 50)

        self.assertEqual(lamda(25), 25)
        self.assertEqual(lamda("H"), Fail)
        self.assertEqual(lamda(-25), Fail)

        # int_range() as composite filter
        lamda = int_range(0, 50, positive())

        self.assertEqual(lamda(25), 25)
        self.assertEqual(lamda(25.2), Fail)
        self.assertEqual(lamda("hey"), Fail)

    def test_kiln_array(self):
        """ array() """

        # array of simple type
        lamda = array(integer())

        self.assertEqual(lamda(range(10)), range(10))
        self.assertEqual(lamda(["A", "B", 0]), Fail)

        # array of compound data types
        lamda = array(positive(integer()))

        self.assertEqual(lamda([0, -1]), Fail)
        self.assertEqual(lamda([0, 1, 2]), [0, 1, 2])

        # array of compound data types
        lamda = array(array(positive()))

        self.assertEqual(lamda([]), [])
        self.assertEqual(lamda([2]), Fail)
        self.assertEqual(lamda([[-1, 2]]), Fail)
        self.assertEqual(lamda([[2], [1]]), [[2], [1]])

    def test_kiln_dikt(self):
        """ dikt() """

        # statically typed dict's
        lamda = dikt(string(), integer())

        self.assertEqual(lamda({1: 1, 2: 2}), Fail)
        self.assertEqual(lamda({"1": 1, "2": 2}), {"1": 1, "2": 2})

        # composite typed dict's
        lamda = dikt(string(), positive(integer()))

        self.assertEqual(lamda({"1": 1, "2": 2}), {"1": 1, "2": 2})
        self.assertEqual(lamda({"1": -1}), Fail)

    def test_kiln_bool_or(self):
        """ bool_or() """

        lamda = bool_or(integer(), string())

        self.assertEqual(lamda("hey"), "hey")
        self.assertEqual(lamda(12345), 12345)
        self.assertEqual(lamda(123.45), Fail)

    def test_kiln_bool_and(self):
        """ bool_and() """

        lamda = bool_and(integer(), positive())

        self.assertEqual(lamda(5), 5)
        self.assertEqual(lamda(""), Fail)
        self.assertEqual(lamda(5.5), Fail)

    def test_kiln_bool_eq(self):
        """ bool_eq() """

        lamda = bool_eq(2, integer("2"))
        self.assertEqual(lamda(), 2)

        lamda = bool_or(bool_eq(1), bool_eq(-1))
        self.assertEqual(lamda(-1), -1)

    def test_kiln_opt(self):
        """ opt() """

        lamda = opt(integer(), null())
        
        self.assertEqual(lamda(5), 5)
        self.assertEqual(lamda("")(""), None)

    def test_kiln_klass(self):
        """ klass() """

        class TestClass:
            """ Test Class """
            pass

        lamda = klass(TestClass)
        val = TestClass()

        self.assertEqual(lamda(val), val)
        self.assertEqual(lamda(123), Fail)
