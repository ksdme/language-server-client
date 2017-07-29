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
    """ Basic TestUnit """

    def test_protocol_raw_bricks(self):
        """
            Tests if each brick class has an associated
            STRUCT
        """
