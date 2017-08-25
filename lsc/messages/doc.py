"""
    @author ksdme
    holds doc parameters
    protocol.md#position
"""
from sure.types import *
from sure.builder import TypedModel
from lsc.messages.abstract import DocumentUri

class Position(TypedModel):
	""" @typed

		zero based position of char
		indexes by line no and char offset
		protocol.md#position	
	""" 

	line = integer()
	character = integer()

class Range(TypedModel):
	""" @typed

		basically a selection of text
		protocol.md#range
	"""

	start = klass(Position)
	end = klass(Position)

class Location(TypedModel):
	""" @typed

		indicates a range selection
		in a document identified by DocUri
	"""

	uri = klass(DocumentUri)
	range = klass(Range)
