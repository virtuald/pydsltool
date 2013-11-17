
#
# TODO: Other useful operations
#



class add_to_list(object):
    '''
        Useful for implementing the += operation in your DSL. 
        
        DSL Implementation Object Usage:
        
            class Foo(object):
                
                _items = []
                
                @property
                def items(self):
                    return dsltool.add_to_list(self._items)
                
                @add.setter
                def items(self, value):
                    self._items = value
                
        DSL End User Usage:
        
            with Foo:
                add += 'item'
        
    '''
    
    def __init__(self, lst):
        self.lst = lst
        
    def __iadd__(self, item):
        self.lst.append(item)
        return self.lst
    
    
class list_of(list):
    '''
        When seen in a DSL Implementation Object, this allows the 'with'
        statement to occur multiple times, and each time a new object will
        be appended to the list.
        
        @warning Don't use it like this, or you will get odd errors:
        
            class Foo:
                bar = dsltool.list_of(Bar)
                
        Instead, prefer this:
        
            class Foo:
                def __init__(self):
                    self.bar = dsltool.list_of(Bar)
    '''
    
    def __init__(self, cls):
        list.__init__(self)
        self._original_cls = cls
