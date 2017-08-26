"""
	@author ksdme
	holds all the misc data models
"""
from sure.types import *
from sure.builder import TypedModel

class Command(TypedModel):
	""" @typed

		Represents a command, depends on implementation
		protocol.md#command
	""" 

	title = string()
	command = string()
	arguments = optional(array(accept()))
