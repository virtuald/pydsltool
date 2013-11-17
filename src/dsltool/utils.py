
# 
# Camelcase from https://gist.github.com/jaytaylor/3660565
#

import re

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')
 
def camelToSnake(s):
    """
        Is it ironic that this function is written in camel case, yet it
        converts to snake case? hmm..
    """
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()

