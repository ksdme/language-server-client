import unittest, json
from lsc import bricks

class TestUnits(unittest.TestCase):

	def test_protocol_units(self):

		for l in dir(bricks):
			avail = getattr(bricks, l)
			if type(avail) == type:
				if issubclass(avail, bricks.Brick):
					try:
						json.loads(avail.__doc__)
					except Exception as e:
						self.assertTrue(False,
							"{}; {}".format(l, str(e)))

		self.assertTrue(True)
