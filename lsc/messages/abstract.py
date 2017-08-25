"""
    @author ksdme
    an abstract message,
    as defined by the lsp protocol protocol.md#abstract-message
"""
from sure.types import *
from sure.builder import TypedModel, TypedValue

class Message(TypedModel):
    """ @typed
        
        Abstract Message
        protocol.md#abstract-message
    """

    jsonrpc = const("2.0")

class RequestMessage(Message):
    """ @typed
        
        Request Message,
        Request message used to describe request from client/server
        protocol.md#requestmessage
    """

    id = bool_or(
            integer(),
            string())

    method = string()

    params = optional(accept())

class ResponseError(Message):
    """ @typed

        Represents the error that occoured
        protocol.md#response-message
    """

    code = integer()
    message = string()
    data = optional(accept())

class ResponseMessage(Message):
    """ @typed

        Response Message,
        protocol.md#response-message
    """

    id = bool_or(
            integer(),
            string(),
            null())
    result = optional(accept())
    error = optional(klass(ResponseError))

class NotificationMessage(Message):
    """ @typed

        Notification Message,
        protocol.md#notification-message
    """

    method = string()
    params = optional(accept())

class CancelParams(Message):
    """ @typed

        Cancel Params
        used to cancel request
    """

    id = bool_or(
            integer(),
            string())

class DocumentUri(TypedValue):
    """ @typed

        DocumentUri,
        String
    """

    uri = string().length(1)
