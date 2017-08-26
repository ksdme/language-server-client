"""
	@author ksdme
	handles the messages that signal edits
	on the text files
"""
from sure.types import *
from sure.builder import TypedModel
from lsc.messages.params import Range
from lsc.messages.doc import VersionedTextDocumentIdentifier

class TextEdit(TypedModel):
	""" @typed

		textual edit applicable to a text document
		protocol.md#textedit
	"""

	range = klass(Range)
	newText = string()

class TextDocumentEdit(TypedModel):
	""" @typed

		[NEW] textual changes on a single text document
		protocol.md#new-textdocumentedit
	"""

	textDocument = klass(VersionedTextDocumentIdentifier)
	edits = array(klass(TextEdit))

class WorkspaceEdit(TypedModel):
	""" @typed

		represents changes made in a given workspace
		protocol.md#workspaceedit
	"""

	changes = optional(dictionary(
						string(),
						array(klass(TextEdit))))

	documentChanges = optional(array(TextDocumentEdit))
