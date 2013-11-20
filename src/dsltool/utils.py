
# 
# Camelcase from https://gist.github.com/jaytaylor/3660565
#

import re
from functools import wraps
import warnings

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')
 
def camelToSnake(s):
    """
        Is it ironic that this function is written in camel case, yet it
        converts to snake case? hmm..
    """
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn("deprecated", DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper
