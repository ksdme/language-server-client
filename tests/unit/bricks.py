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

class TestUnits(unittest.TestCase):
    """ Basic TestUnit """

    def test_protocol_raw_bricks(self):
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
