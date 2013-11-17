
#
# py.test based tests
#

import dsltool
from inspect import cleandoc

import pytest

#
# DSL Objects
#


class AddDsl(object):
    
    _items = []
    
    @property 
    def items(self):
        return dsltool.add_to_list(self._items)
    
    @items.setter
    def items(self, value):
        self._items = value
        

class ChildDsl(object):
    child_var = None

class ListOfDsl(object):
    var = None
    
    def __init__(self):
        self.child_dsl = dsltool.list_of(ChildDsl)

#
# Test add_to_list
#

def test_addto_0():
    dsl_contents = cleandoc('''
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, AddDsl)
    assert result._items == []

def test_addto_1():
    dsl_contents = cleandoc('''
        items += 1
        items += 2 
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, AddDsl)
    assert result._items == [1,2]
    
#
# Test list_of
#

def test_listof_0():
    dsl_contents = cleandoc('''
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ListOfDsl)
    assert result.child_dsl == []

def test_listof_1a():
    dsl_contents = cleandoc('''
        with ChildDsl:
            pass
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ListOfDsl)
    assert len(result.child_dsl) == 1
    assert type(result.child_dsl[0]) is ChildDsl
    
def test_listof_1b():
    dsl_contents = cleandoc('''
        with ChildDsl():
            pass
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ListOfDsl)
    assert len(result.child_dsl) == 1
    assert type(result.child_dsl[0]) is ChildDsl

def test_listof_1c():
    dsl_contents = cleandoc('''
        with ChildDsl():
            child_var = 1
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ListOfDsl)
    assert len(result.child_dsl) == 1
    assert type(result.child_dsl[0]) is ChildDsl
    assert result.child_dsl[0].child_var == 1

def test_listof_2a():
    dsl_contents = cleandoc('''
        with ChildDsl:
            child_var = 0
        with ChildDsl:
            child_var = 1
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ListOfDsl)
    assert len(result.child_dsl) == 2
    for i, child in enumerate(result.child_dsl):
        assert type(child) is ChildDsl
        assert child.child_var == i

def test_listof_2b():
    dsl_contents = cleandoc('''
        with ChildDsl:
            child_var = 0
        with ChildDsl:
            child_var = 1
        with ChildDsl:
            child_var = 2
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ListOfDsl)
    assert len(result.child_dsl) == 3
    for i, child in enumerate(result.child_dsl):
        assert type(child) is ChildDsl
        assert child.child_var == i

def test_listof_2c():
    dsl_contents = cleandoc('''
        with ChildDsl():
            child_var = 0
        with ChildDsl():
            child_var = 1
        with ChildDsl():
            child_var = 2
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ListOfDsl)
    assert len(result.child_dsl) == 3
    for i, child in enumerate(result.child_dsl):
        assert type(child) is ChildDsl
        assert child.child_var == i


