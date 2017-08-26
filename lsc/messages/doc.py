"""
	@author ksdme
	contains messages that describe a text doc
"""
from sure.types import *
from sure.builder import TypedModel, TypedValue
from lsc.messages.params import Position
from lsc.messages.abstract import DocumentUri

class TextDocumentIdentifier(TypedModel):
	""" @typed

		Identifies a text document by uri
		protocol.md#textdocumentidentifier
	"""

	uri = klass(DocumentUri)

class TextDocumentItem(TypedModel):
	""" @typed

		helps transfer text docment from
		client to server
		protocol.md#textdocumentitem
	"""

	uri = klass(DocumentUri)
	languageId = string()
	version = integer()
	text = string()

class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
	""" @typed

		denotes a specific version of the given document
		protocol.md#versionedtextdocumentidentifier
	"""

	version = integer()

class TextDocumentPositionParams(TypedModel):
	""" @typed

		message used to pass text document
		and a position inside a doc
		protocol.md#textdocumentpositionparams
	"""

	textDocument = klass(TextDocumentIdentifier)
	position = klass(Position)

class DocumentFilter(TypedModel):
	""" @typed

		[NEW] used a filter for selecting files
		protocol.md#new-documentfilter
	"""

	language = optional(string())
	scheme = optional(string())
	pattern = optional(string())

class DocumentSelector(TypedValue):
	""" @typed

		A document selector is the combination of
		one or more document filters.
	"""

	selector = array(klass(DocumentFilter))
