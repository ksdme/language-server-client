"""
	@author ksdme
	diagonistics messages
	I see this module merging back into some other
	logical unit in near future, anyway
"""
from sure.types import *
from sure.builder import TypedModel
from lsc.messages.params import Range

class Diagnostic(TypedModel):
	""" @typed

		Represents a diagnostic message
		protocol.md#diagnostic
	"""

	range = klass(Range)
	severity = optional(integer())
	
	code = optional(bool_or(
				integer(),
				string()))

	source = optional(string())
	message = string()

class DiagnosticSeverity(object):
	"""
		diagnostic severities
	"""

	Error = 1
	Warning = 2
	Information = 3
	Hint = 4
