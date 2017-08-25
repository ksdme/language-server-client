"""
	@author ksdme
	test doc classes of lsc messages
"""
from unittest import TestCase
from lsc.messages.doc import *

class TestDocMessages(TestCase):
	""" tests doc """

	def test_position_class(self):
		""" position class """

		position = Position()
		position.character = 20
		position.line = 25

		position = Position(line=25, character=50)
		self.assertEqual(position(), {
			"character": 50,
			"line": 25 })

	def test_range_class(self):
		""" tests range model """

		range = Range()
		range.start = Position(
			character=20,
			line=10)

		range.end = Position(
			character=35,
			line=20)

		self.assertEqual(range(), {
			"start": {
				"character": 20,
				"line": 10
			},
			
			"end": {
				"character": 35,
				"line": 20
			}
		})

	def test_location_class(self):
		""" tests location class """

		location = Location()
		location.uri = DocumentUri("http://google.com")
		location.range = Range(
				start = Position(character=20, line=5),
				end = Position(character=35, line=6)
			)
