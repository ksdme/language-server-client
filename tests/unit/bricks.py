"""
    @author ksdme
    Tests lsc.bricks module, both in terms of
    of the raw definitions of the Bricks and
    also their compiled forms
"""

import json
import unittest

from lsc import bricks

class TestUnits(unittest.TestCase):
    """ TestUnit """

    def test_protocol_units(self):
        """
            Tests all Brick classes provided
            by lsc.bricks if their doc strings
            are json loadbale
        """

        for attrbute in dir(bricks):
            avail = getattr(bricks, attrbute)
            if isinstance(avail, type):
                if issubclass(avail, bricks.Brick):
                    try:
                        json.loads(avail.__doc__)
                    except Exception as err:
                        self.assertTrue(False,
                                        "{}; {}".format(attrbute, str(err)))
