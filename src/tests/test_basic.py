
#
# py.test based tests
#

import dsltool
from inspect import cleandoc

#
# DSL Objects
#

class BasicDsl(object):
    var = None
    other_var = None


class BasicPropertyDsl(object):
    
    def __init__(self):
        self._var = None
        self.other_var = None
    
    @property
    def var(self):
        return self._var
        
    @var.setter
    def var(self, val):
        self._var = val

#
# Tests
#

def test_basic_0():
    dsl_contents = cleandoc('''
        
    ''')
    
    result1 = dsltool.parse_dsl(dsl_contents, BasicDsl)
    assert result1.var == None
    
    result2 = dsltool.parse_dsl(dsl_contents, BasicPropertyDsl)
    assert result2.var == None

def test_basic_1():
    dsl_contents = cleandoc('''
        var = 3
    ''')
    
    result1 = dsltool.parse_dsl(dsl_contents, BasicDsl)
    assert result1.var == 3
    
    result2 = dsltool.parse_dsl(dsl_contents, BasicPropertyDsl)
    assert result2.var == 3
    
def test_basic_2():
    dsl_contents = cleandoc('''
        var = 3
        other = 4
    ''')
    
    result1 = dsltool.parse_dsl(dsl_contents, BasicDsl)
    assert result1.var == 3
    
    result2 = dsltool.parse_dsl(dsl_contents, BasicPropertyDsl)
    assert result2.var == 3
    
    
def test_basic_3():
    dsl_contents = cleandoc('''
        class Foo(object):
            def get_3(self):
                return 3
        
        foo = Foo()
        var = foo.get_3()
    ''')
    
    result1 = dsltool.parse_dsl(dsl_contents, BasicDsl)
    assert result1.var == 3
    
    result2 = dsltool.parse_dsl(dsl_contents, BasicPropertyDsl)
    assert result2.var == 3
    
def test_basic_4():
    dsl_contents = cleandoc('''
        var = 3
        other_var = var
    ''')
    
    result1 = dsltool.parse_dsl(dsl_contents, BasicDsl)
    assert result1.var == 3
    assert result1.other_var == 3
    
    result2 = dsltool.parse_dsl(dsl_contents, BasicPropertyDsl)
    assert result2.other_var == 3
    