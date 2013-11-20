
#
# TODO: Other useful operations
#


class ItemList(list):
    '''
        A list that allows adding items to it via the += operator.
                
        DSL Implementation Object Usage:
        
            class Foo(object):
                def __init__(self):
                    self.items = ItemList()
                
        DSL usage:
        
            with Foo:
                items += 'item1'
                items += 'item2
                
        Result:
        
            foo.items == ['item1', 'item2']
    '''
    def __iadd__(self, item):
        self.append(item)
        return self
    
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
