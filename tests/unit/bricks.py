"""
    @author ksdme
    Tests lsc.bricks module, both in terms of
    of the raw definitions of the Bricks and
    also their compiled forms
"""

import unittest
from lsc import bricks

class Messages:
    """ Messages """

    STRUCT_MISSING = "Missing Structure Descriptor"

class TestBricks(unittest.TestCase):
    """ Basic TestUnit """

    def test_raw_bricks(self):
        """
            Tests if each brick class has an associated
            STRUCT. Its basic consistency test.
        """

        for elem in dir(bricks):
            prop = getattr(bricks, elem)
            if isinstance(prop, type):
                if issubclass(prop, bricks.Brick):
                    if not hasattr(prop, "STRUCT"):
                        if prop is not bricks.Brick:
                            message = "{}; {}".format(elem, Messages.STRUCT_MISSING)
                            self.assertTrue(False, message)

    def test_brick_objects(self):
        """ Monolithic Test """
        from lsc.bricks import RequestMessage
        from lsc.exceptions import ValueTypeError

        """
            Barebone Testing on a dict type holder
        """
        req = RequestMessage(("params", ""), id=10, method="info")

        self.assertEqual(req.get_value("id"), 10)
        self.assertEqual(req.get_value("method"), "info")

        req = RequestMessage(id=10, params="info")
        with self.assertRaises(ValueTypeError):
            req.set_value("method", 125.0, True)
