"""
    @author ksdme
    Exceptions
"""

class RequiredParameter(Exception):
    """Required Paramter missing"""

class ParameterError(Exception):
    """Parameter Errors"""

    def __init__(self, msg):
        super(ParameterError, self).__init__(msg)

class ValueTypeError(Exception):
    """Value Error"""

    def __init__(self, msg):
        super(ValueTypeError, self).__init__(msg)
