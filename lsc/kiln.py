"""
    @author ksdme
    Contains basic units for building bricks
"""
Fail = "#@None@#"

# -------------------------------------
# Simple value based type checker
# -------------------------------------
def integer(val=None):
    """ Convert into int or ensure that it is an integer """

    if val is None:
        return lambda arg: arg if isinstance(arg, int) else Fail
    else:
        return lambda arg: int(val)

def string(val=None):
    """ Returns if str flag is none else lambda """

    if val is None:
        return lambda arg: arg if isinstance(arg, str) else Fail
    else:
        return lambda arg: str(val)

def null():
    """ Accepts None """
    return lambda val: None if val is None else Fail

def accept_any():
    """ It doesn't care, Accepts all """
    return lambda val: val

# -------------------------------------
# Extended type checkers
# -------------------------------------
def positive(arg):
    """ Accepts only positive """

    return lambda val: val if arg(val=val) >= 0 else Fail

def int_range(start, end):
    """ Ensure Integer Range """

    return lambda val: val if val >= start and val <= end else Fail

# -------------------------------------
# Collection type checkers
# -------------------------------------
def array(typ):
    """ Ahoy, An array! """

    def lhs(val):
        assert isinstance(val, list)

        for elem in val:
            if typ(val=elem) == Fail:
                return Fail

        return val

    return lhs

def dikt(keyTyp, valTyp):
    """ Checks if the passed array's type """

    def lhs(dykt):
        assert isinstance(dykt, dict)

        for key, val in dykt.iteritems():
            if not isinstance(key, keyTyp):
                if not isinstance(val, valTyp):
                    return Fail

        return dykt

    return lhs

# -------------------------------------
# Compound type checkers
# -------------------------------------
def bool_or(*args):
    """ Or """

    def internal(val):
        for elem in args:
            val = elem(val=val)
            if val is not Fail:
                return val

    return internal

def bool_eq(arg):
    """ Equals """

    return lambda val: val if arg == val else Fail

def opt(lhs, default=None):
    """ Optional, If lhs fails then default """

    return lambda val: lhs(val=val) or default

# -------------------------------------
# Simple class instance checker
# -------------------------------------
def klass(val=None):
    """ Ensures that the arg is a instance of a class """

    if val is None:
        return lambda arg: Fail
    else:
        return lambda arg: arg if isinstance(arg, val) else Fail
