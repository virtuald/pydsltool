
#
# py.test based tests
#

import dsltool
from inspect import cleandoc

#
# DSL Objects
#


class ChildDsl(object):
    child_var = None

class ListOfDsl(object):
    var = None
    
    def __init__(self):
        self.child_dsl = dsltool.list_of(ChildDsl)
        
class ItemListDsl(object):
    def __init__(self):
        self.items = dsltool.helpers.ItemList()
    
#
# Test item_list_property
#

def test_item_list_0():
    dsl_contents = cleandoc('''
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ItemListDsl)
    assert result.items == []

def test_item_list_1():
    dsl_contents = cleandoc('''
        items += 1
        items += 2 
    ''')
    
    result = dsltool.parse_dsl(dsl_contents, ItemListDsl)
    assert result.items == [1,2]

    
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


