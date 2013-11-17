
#
# py.test based tests
#

import dsltool
from inspect import cleandoc

import pytest

#
# DSL Objects
#

class GrandchildDsl(object):
    grandchild_var = None

class ChildDsl(object):
    child_var = None
    grandchild_dsl = GrandchildDsl

class BaseDsl(object):
    var = None
    
    child_dsl = ChildDsl


#
# Test nested with statements
#


def test_with_0a0():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl:
            child_var = 4
            with GrandchildDsl:
                grandchild_var = 5
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == 3
    assert result.child_dsl.child_var == 4
    assert result.child_dsl.grandchild_dsl.grandchild_var == 5
    
def test_with_0a1():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl as c:
            c.child_var = 4
            with GrandchildDsl as g:
                g.grandchild_var = 5
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == 3
    assert result.child_dsl.child_var == 4
    assert result.child_dsl.grandchild_dsl.grandchild_var == 5
    
def test_with_0b0():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl():
            child_var = 4
            with GrandchildDsl():
                grandchild_var = 5
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == 3
    assert result.child_dsl.child_var == 4
    assert result.child_dsl.grandchild_dsl.grandchild_var == 5
    
def test_with_0b1():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl() as c:
            c.child_var = 4
            with GrandchildDsl() as g:
                g.grandchild_var = 5
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == 3
    assert result.child_dsl.child_var == 4
    assert result.child_dsl.grandchild_dsl.grandchild_var == 5    

#
# Test missing with statements
#

def test_with_1a():
    dsl_contents = cleandoc('''
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == None
    assert result.child_dsl is None

def test_with_1b():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl:
            pass
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == 3
    assert result.child_dsl.child_var is None
    assert result.child_dsl.grandchild_dsl is None

def test_with_1c0():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl:
            child_var = 4
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == 3
    assert result.child_dsl.child_var == 4
    assert result.child_dsl.grandchild_dsl is None
    
def test_with_1c1():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl as c:
            c.child_var = 4
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, BaseDsl)
    assert result.var == 3
    assert result.child_dsl.child_var == 4
    assert result.child_dsl.grandchild_dsl is None
    
#
# Test multiple with statements
#

def test_with_2a():
    dsl_contents = cleandoc('''
        var = 3
        with ChildDsl:
            child_var = 4
        with ChildDsl:
            child_var = 5
    ''')
    
    with pytest.raises(AttributeError):
        dsltool.parse_dsl(dsl_contents, BaseDsl)
    
#
# Test missing classes
#

def test_with_3a():
    dsl_contents = cleandoc('''
        var = 3
        with MissingClass:
            var = 4
    ''')
    
    with pytest.raises(NameError):
        dsltool.parse_dsl(dsl_contents, BaseDsl)
    
