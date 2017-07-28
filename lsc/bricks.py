"""
    @author ksdme
    Contains wrappers for protocol objects
"""

class Brick(object):
    """ "null" """
    pass

# -------------------------------------
# Document Identification Bricks
# -------------------------------------
# Refer to protocol.md#uri
class DocumentUri(Brick):
    """
        "str()"
    """

class TextDocumentIdentifier(Brick):
    """
        {
            "uri": "class(DocumentUri)"
        }
    """

# extends TextDocumentIdentifier
class VersionedTextDocumentIdentifier(Brick):
    """
        {
            "uri": "class(DocumentUri)",
            "version": "int()"
        }
    """

# -------------------------------------
# Error/Diagonstic Codes Handlers
# -------------------------------------
# protocol.md#diagnostic
class DiagnosticSeverity(Brick):
    """
        "int_range(1, 4)"
    """

# protocol.md#response-message
class ErrorCodes(Brick):
    """
        "or(eq(-32700),eq(-32600),eq(-32601),eq(-32602),eq(-32603),eq(-32099),eq(-32000),eq(-32002),eq(-32001),eq(-32800))"
    """

class ResponseError(Brick):
    """
        {
            "code":     "int()",
            "message":  "str()",
            "data":     "opt(class(ErrorCodes))"
        }
    """

# ------------------------------------- 
# Basic Bricks
# -------------------------------------
class Message(Brick):
    """
        {
            "jsonrpc": "str('2.0')"
        }
    """

# extends Message
class RequestMessage(Brick):
    """
        {
            "jsonrpc":  "str('2.0')",

            "id":       "or(int(), str())",
            "method":   "str()",
            "params":   "opt(any())"
        }
    """

# extends Message
class ResponseMessage(Brick):
    """
        {
            "jsonrpc": "str('2.0')",

            "id":       "or(int(), str(), null())",
            "result":   "opt(any())",
            "error":    "opt(class(ResponseError))"
        }
    """

# extends Message
class NotificationMessage(Brick):
    """
        {
            "method": "str()",
            "params": "opt(any())"
        }
    """

class CancelParams(Brick):
    """
        {
            "id": "or(int(), str())"
        }
    """

# -------------------------------------
# Bricks
# -------------------------------------
class Position(Brick):
    """
        {
            "line":     "pos(int())",
            "character":"pos(int())"
        }
    """

class Range(Brick):
    """
        {
            "start":    "class(Position)",
            "end":      "class(Position)"
        }
    """

class Location(Brick):
    """
        {
            "uri":   "class(DocumentUri)",
            "range": "class(Range)"
        }
    """

class Diagnostic(Brick):
    """
        {
            "range":    "class(Range)",
            "severity": "opt(class(DiagnosticSeverity))",
            "code":     "opt(or(int(), str()))",
            "source":   "opt(str())",
            "message":  "str()"
        }
    """

class Command(Brick):
    """
        {
            "title":        "str()",
            "command":      "str()",
            "arguments":    "opt(array())"
        }
    """

class TextEdit(Brick):
    """
        {
            "range": "class(Range)",
            "newText": "str()"
        }
    """

class TextDocumentEdit(Brick):
    """
        {
            "textDocument": "class(VersionedTextDocumentIdentifier)",
            "edits":        "array(class(TextEdit))"
        }
    """

class WorkspaceEdit(Brick):
    """
        {
            "changes": "opt(dict(class(DocumentUri), array(class(TextEdit))))",
            "documentChanges": "array(class(TextDocumentEdit))"
        }
    """

class TextDocumentItem(Brick):
    """
        {
            "uri":          "class(DocumentUri)",
            "languageId":   "str()",
            "version":      "int()",
            "text":         "str()"
        }
    """

class TextDocumentPositionParams(Brick):
    """
        {
            "textDocument": "class(TextDocumentIdentifier)",
            "position":     "class(Position)"
        }
    """

class DocumentFilter(Brick):
    """
        {
            "language": "opt(str())",
            "scheme":   "opt(str())",
            "pattern":  "opt(str())"
        }
    """

class DocumentSelector(Brick):
    """
        "array(class(DocumentFilter))"
    """
