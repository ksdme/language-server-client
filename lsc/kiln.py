"""
    @author ksdme
    Contains basic units for building bricks
"""
Fail = "#@None@#"

# -------------------------------------
# Utilities
# -------------------------------------
def isFail(val):
    return val is Fail

def fail(val):
    return Fail

# -------------------------------------
# Simple value based type checker
# -------------------------------------
def integer(pre=None):
    """ Convert into int or ensure that it is an integer """

    if pre is None:
        return lambda val: val if isinstance(val, int) and not isFail(val) else Fail
    else:
        return lambda val=None: int(float(pre))

def string(pre=None):
    """ Returns if str flag is none else lambda """

    if pre is None:
        return lambda val: val if isinstance(val, str) and not isFail(val) else Fail
    else:
        return lambda val=None: str(pre)

def null():
    """ Accepts None """
    return lambda val: None

def accept_any():
    """ It doesn't care, Accepts all """
    return lambda val: val

# -------------------------------------
# Extended type checkers
# -------------------------------------
def positive(arg=None):
    """ Accepts only positive """

    if arg is None:
        return lambda val: val if val >= 0 and not isFail(val) else Fail
    else:
        return lambda val: positive()(arg(val=val))

def int_range(start, end, arg=None):
    """ Ensure Integer Range """

    if arg is None:
        return lambda val: val if start <= val <= end and integer()(val) != Fail else Fail
    else:
        return lambda val: int_range(start, end)(arg(val=val))

# -------------------------------------
# Collection type checkers
# -------------------------------------
def array(typ):
    """ Ahoy, An array! """

    def lhs(val):
        if not isinstance(val, list):
            return Fail

        for elem in val:
            if typ(val=elem) is Fail:
                return Fail

        return val

    return lhs

def dikt(keyTyp, valTyp):
    """ Checks if the passed array's type """

    def lhs(val):
        if not isinstance(val, dict):
            return Fail

        for key, itm in val.iteritems():
            if isFail(keyTyp(key)) or isFail(valTyp(itm)):
                return Fail

        return val

    return lhs

# -------------------------------------
# Compound type checkers
# -------------------------------------
def bool_or(*args):
    """ Or """

    def internal(val):
        for elem in args:
            out = elem(val=val)
            if out is not Fail:
                return val

        return Fail

    return internal

def bool_and(*args):
    """ Or """

    def internal(val):
        for elem in args:
            out = elem(val=val)
            if out is Fail:
                return Fail

        return val

    return internal

def bool_eq(equals, arg=None):
    """ Equals """

    if arg is None:
        return lambda val: val if equals is val else Fail
    else:
        return lambda val=None: bool_eq(equals)(arg(val=val))

def opt(arg, default=fail):
    """ Optional, If lhs fails then default """

    def lhs(val):
        out = arg(val=val)
        if not isFail(out):
            return out
        else:
            return default

    return lhs

# -------------------------------------
# Simple class instance checker
# -------------------------------------
def klass(pre=None):
    """ Ensures that the arg is a instance of a class """

    if pre is None:
        return lambda val=None: Fail
    else:
        return lambda val: val if isinstance(val, pre) and not isFail(val) else Fail
