"""
    @author ksdme
    Contains wrappers for protocol objects
"""
from lsc.kiln import *
from lsc.exceptions import *

class Brick(object):
    """ "null" """
    UNDEFINED = "#@!UNDEFINED!@#"

    def __init__(self, *args, **kargs):
        self.klass = self.__class__
        self._struct = self.klass.STRUCT
        self._val_struct = {}

        self.set_up_struct(self.struct, self._val_struct)

        # set the initials
        for pair in args:
            if not isinstance(pair, tuple):
                raise ValueError("*args need to be (key, val)")

        for key, val in list(kargs.iteritems())+list(args):
            self.set_value(key, val)

    def validate_struct(self, struct=None):
        """ Validate Struct Type """
        if struct is None:
            struct = self.struct

        return isinstance(struct, dict) or callable(struct)

    def set_up_struct(self, struct, context=None, root=True):
        """
            Setup struct and alias functions,
            Context for root stays 'self'
        """
        assert isinstance(struct, dict)

        if root is True:
            self._val_struct = {}
            context = self._val_struct

        for key, val in struct.iteritems():
            if isinstance(val, dict):
                context[key] = {}
                self.set_up_struct(val, context[key], False)
            else:
                context[key] = Brick.UNDEFINED

    def set_value(self, key, val, throw=False, only_check=False):
        """
            This method here sets the value of a given parameter of a
            STRUCT while making sure that it does suffice the requirements
            only_check: Doesn't assign values to the struct, only checks them
                        for type safety and does what throws implies
        """
        value_type_error = ValueTypeError("Value doesn't meet condition ({})".format(key))

        try:
            beans = key.split(".")
            pointer_val = self._val_struct
            pointer_str = self.struct
            for bean in beans[:-1]:
                pointer_val = pointer_val[bean]
                pointer_str = pointer_str[bean]

            """
                Happens only when a dict is being built
                rather than its individual components, 
                this ensures that the entire dictionary
                being assigned is consistent with the type
                declarations and only then does the job,
                If it doesn't then no assignments are made
            """
            if isinstance(val, dict):
                if isinstance(pointer_str[beans[-1]], dict):
                    flag = True
                    for lkey, lval in val.iteritems():
                        nkey = "{}.{}".format(key, lkey)
                        flag = flag and self.set_value(nkey, lval, False, True)

                    if flag is False:
                        if not throw:
                            return False
                        else:
                            raise value_type_error
                    else:
                        for lkey, lval in val.iteritems():
                            nkey = "{}.{}".format(key, lkey)
                            flag = flag and self.set_value(nkey, lval, throw)

                        return True

            # Happens when a value needs to be set after
            # being verified by the Kiln functions
            callble = pointer_str[beans[-1]]
            assert callable(callble)

            if callble(val) is not Fail:
                if not only_check:
                    pointer_val[beans[-1]] = val
                return True
            else:
                if not throw:
                    return False
                else:
                    raise value_type_error

        except KeyError:
            raise ParameterError("No such parameter found ({})".format(key))

        except ValueTypeError as value_error:
            raise ValueTypeError(value_error.message)

    def get_value(self, key):
        """
            Get the value of some field,
            Returns UNDEFINED too, Check using the
            reference Brick Class provides.
        """
        try:
            beans = key.split(".")
            pointer_val = self._val_struct
            for bean in beans[:-1]:
                pointer_val = pointer_val[bean]

            return pointer_val[beans[-1]]

        except:
            msg = "No such parameter found ({})".format(key)
            raise ParameterError(msg)

    struct = property(lambda self: self._struct)

# -------------------------------------
# Document Identification Bricks
# -------------------------------------
# Refer to protocol.md#uri
class DocumentUri(Brick):
    """ Represents Document, Simply a Path String """

    STRUCT = string()

class TextDocumentIdentifier(Brick):
    """ Simply Extends DocumentUri for TextDoc """

    STRUCT = {
        "uri": klass(DocumentUri)
    }

# extends TextDocumentIdentifier
class VersionedTextDocumentIdentifier(Brick):
    """
       Extends TextDocIden to include Version int,
       It should ideally be incremented on each edit
    """

    STRUCT = {
        "uri": klass(DocumentUri),
        "version": integer()
    }

# -------------------------------------
# Error/Diagonstic Codes Handlers
# -------------------------------------
# protocol.md#diagnostic
class DiagnosticSeverity(Brick):
    """
        "int_range(1, 4)"
    """

    STRUCT = int_range(1, 4)

# protocol.md#response-message
class ErrorCodes(Brick):
    """
        You know how it is, errors are bound to
        happen and then we have error codes
    """

    STRUCT = bool_or(
        bool_eq(-32700),
        bool_eq(-32600),
        bool_eq(-32601),
        bool_eq(-32602),
        bool_eq(-32603),
        bool_eq(-32099),
        bool_eq(-32000),
        bool_eq(-32002),
        bool_eq(-32001),
        bool_eq(-32800))

class ResponseError(Brick):
    """ General Response Error """

    STRUCT = {
        "code": integer(),
        "message": string(),
        "data": opt(klass(ErrorCodes))
    }

# -------------------------------------
# Basic Bricks
# -------------------------------------
class Message(Brick):
    """ General Message """

    STRUCT = {
        "jsonrpc": str("2.0")
    }

# extends Message
class RequestMessage(Brick):
    """ Request Messages """

    STRUCT = {
        "jsonrpc": str("2.0"),

        "id": bool_or(integer(), string()),
        "method": string(),
        "params": opt(accept_any())
    }

# extends Message
class ResponseMessage(Brick):
    """ Response Message """

    STRUCT = {
        "jsonrpc": str("2.0"),

        "id": bool_or(integer(), string(), null()),
        "result": opt(accept_any()),
        "error": opt(klass(ResponseError))
    }

# extends Message
class NotificationMessage(Brick):
    """ Notification Message """

    STRUCT = {
        "method": string(),
        "params": opt(accept_any())
    }

class CancelParams(Brick):
    """ Cancel Notification """

    STRUCT = {
        "id": bool_or(integer(), string())
    }

# -------------------------------------
# Bricks
# -------------------------------------
class Position(Brick):
    """
        Position of a character in a document
        by its line number and character offset
        Inclusive, Zero based index
    """

    STRUCT = {
        "line": positive(integer()),
        "character": positive(integer())
    }

class Range(Brick):
    """
        Represents Selection range in a text document,
        By Start Position and End Position
    """

    STRUCT = {
        "start": klass(Position),
        "end": klass(Position)
    }

class Location(Brick):
    """
       Location of a Range in a document by DocumentUri
    """

    STRUCT = {
        "uri": klass(DocumentUri),
        "range": klass(Range)
    }

class Diagnostic(Brick):
    """
        Diagnostic Message issued by the Server,
        Optionally Code
    """

    STRUCT = {
        "range": klass(Range),
        "severity": opt(klass(DiagnosticSeverity)),
        "code": opt(bool_or(integer(), string())),
        "source": opt(string()),
        "message": string()
    }

class Command(Brick):
    """ Command Message """

    STRUCT = {
        "title": string(),
        "command": string(),
        "arguments": opt(array(accept_any()))
    }

class TextEdit(Brick):
    """ A TextEdit Message """

    STRUCT = {
        "range": klass(Range),
        "newText": string()
    }

class TextDocumentEdit(Brick):
    """
        Its a collection of edits on a given document
        by Version identified Document Uri,

        Execution-wise text edits should be applied from the bottom
        to the top of the text document. Overlapping text edits are
        not supported.
    """

    STRUCT = {
        "textDocument": klass(VersionedTextDocumentIdentifier),
        "edits": array(klass(TextEdit))
    }

class WorkspaceEdit(Brick):
    """
        A Collection of TextDocumentEdits in a workspace
    """

    STRUCT = {
        "changes": opt(dikt(klass(DocumentUri), array(klass(TextEdit)))),
        "documentChanges": array(klass(TextDocumentEdit))
    }

class TextDocumentItem(Brick):
    """ Message to transfer TextDoc Content to Server """

    STRUCT = {
        "uri": klass(DocumentUri),
        "languageId": string(),
        "version": integer(),
        "text": string()
    }

class TextDocumentPositionParams(Brick):
    """ A TextDocumentItem with Position of some Text """

    STRUCT = {
        "textDocument": klass(TextDocumentIdentifier),
        "position": klass(Position)
    }

class DocumentFilter(Brick):
    """ Filters Documents Using This Message """

    STRUCT = {
        "language": opt(string()),
        "scheme": opt(string()),
        "pattern": opt(string())
    }

class DocumentSelector(Brick):
    """ Collection of Filters """

    STRUCT = array(klass(DocumentFilter))
