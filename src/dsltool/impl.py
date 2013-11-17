
import inspect

from helpers import list_of
from utils import camelToSnake


class DslExecError(Exception):
    pass

class WithProxy(object):
    '''
        There's probably a better way of doing this.
        
        The __getattribute__ function makes it so we can't actually
        perform accesses on our own object, thus why there are all the
        double underscore function calls to object. :) 
        
        This supports the following:
        
            with Foo:
            with Foo as f:
            with Foo():
            with Foo() as f:
            
        But really, you shouldn't be using Foo() as f, as avoiding that
        is the whole point of this DSL stuff... ;)
    '''
    
    def __init__(self, on_construction, on_exit):
        object.__setattr__(self, 'on_construction', on_construction)
        object.__setattr__(self, 'on_exit', on_exit)
    
    def __call__(self, *args, **kwargs):
        '''This is called at 'with Foo()' '''
        on_construction = object.__getattribute__(self, 'on_construction')
        if on_construction is None:
            return getattr(object.__getattribute__(self, 'constructed_obj'), '__call__')(*args, **kwargs)

        constructed_obj = on_construction(*args, **kwargs)
        object.__setattr__(self, 'constructed_obj', constructed_obj)
        object.__setattr__(self, 'on_construction', None)
            
        return self
    
    #
    # without these 'with Foo() as f:' won't work correctly.
    # 
    
    def __getattribute__(self, name):
        return getattr(object.__getattribute__(self, 'constructed_obj'), name)
    
    def __setattr__(self, name, value):
        return setattr(object.__getattribute__(self, 'constructed_obj'), name, value)
    
    def __enter__(self):
        
        # if this is set, the with statement was called
        # without parens. Which is ok, just do the default.

        on_construction = object.__getattribute__(self, 'on_construction')
        if on_construction is not None:            
            constructed_obj = on_construction()
            object.__setattr__(self, 'constructed_obj', constructed_obj)
            object.__setattr__(self, 'on_construction', None)
            
        return self
    
    def __exit__(self, type, value, traceback):
        object.__setattr__(self, 'constructed_obj', None)
        object.__getattribute__(self, 'on_exit')(None)
    

class GlobalsObjectProxy(dict):
    '''
        Used as the 'globals' for an executed DSL file. This is where most
        of the black magic is. 
    '''
        
    def __init__(self, wrapped_obj, filename):
        
        # populate initial dict
        if filename is not None:
            dict.__setitem__(self, '__file__', filename)
        
        self.obj_stack = [wrapped_obj]
        self._pop_stack()
        self._last_push = '<internal error>'
        
    def _pop_stack(self):
        self.wrapped_obj = self.obj_stack.pop()
    
    def _push_stack(self):
        self._last_push = self.wrapped_obj.__class__.__name__
        self.obj_stack.append(self.wrapped_obj)
        self.wrapped_obj = None

    def _check_for_invalid_usage(self):
        if self.wrapped_obj is None:
            raise DslExecError("DSL object name was referenced outside of a 'with' statement (likely was: '%s')" % self._last_push)
            
    def _clean_up_instance(self, inst=None):
        # TODO: refactor
        # TODO: this may be buggy, need to test on properties
        pop_stack = False
        if inst == None:
            pop_stack = True
            inst = self.wrapped_obj
            
        for attr in dir(inst):
            if attr.startswith('_'):
                continue
            
            if inspect.isclass(getattr(inst, attr)):
                setattr(inst, attr, None)
                
        if pop_stack:
            self._pop_stack()
        
            
    def __getitem__(self, k):
        
        #
        # TODO: could have something parse the object before
        # execution, and single out valid/invalid keys, so we
        # would just look in that dict. That way the DSL user couldn't
        # do silly things like overwrite attributes we're looking to
        # use for 'with' statements
        #
        
        self._check_for_invalid_usage()
        
        if hasattr(self.wrapped_obj, k):
            return getattr(self.wrapped_obj, k)
        
        # check for the attribute in snake case. if it exists, 
        # then we are probably using a with statement.
        # 
        # TODO: this can cause subtle bugs, pre-parsing the object
        #       would allow us to catch those
        #
        
        sk = camelToSnake(k)
        
        if hasattr(self.wrapped_obj, sk):
            
            cls = v = getattr(self.wrapped_obj, sk)
            
            # handle properties correctly
            if isinstance(v, property):
                v = getattr(self.wrapped_obj, sk)
            
            attr_is_list = False
            if isinstance(v, list_of):
                attr_is_list = True
                cls = v._original_cls
            
            elif not inspect.isclass(v):
                raise AttributeError("'%s' object has no attribute '%s'" % (self.wrapped_obj.__class__.__name__, k))
            
            # the DSL is asking for a class, return a proxy for the with
            # statement. If they are using list_of, then we append the
            # new instance to the list
            
            # prevent user from calling 'with' twice if they didn't use list_of 
            if not attr_is_list and not inspect.isclass(getattr(self.wrapped_obj, sk)):
                raise AttributeError("'with' statement for '%s' can only be used once per '%s' instance" % (k, self.wrapped_obj.__class__.__name__))
            
            old_object = self.wrapped_obj
            
            # We can't create the child object until the constructor is
            # called, so the WithProxy does that via this function 
            
            def on_construction(*args, **kwargs):
                # if the object is passed an incorrect amount of
                # parameters, you get weird error messages here
                self.wrapped_obj = cls(*args, **kwargs)
                if attr_is_list:
                    getattr(old_object, sk).append(self.wrapped_obj)
                else:
                    setattr(old_object, sk, self.wrapped_obj)
                
                return self.wrapped_obj
            
            self._push_stack()
            return WithProxy(on_construction, self._clean_up_instance)
        
        # return default globals
        return dict.__getitem__(self, k)
            
    
    def __setitem__(self, k, v):
        self._check_for_invalid_usage()
        
        if hasattr(self.wrapped_obj, k):
            setattr(self.wrapped_obj, k, v)
        else:
            dict.__setitem__(self, k, v)
        


def parse_dsl_file(filename, obj):
    '''
        Given a file of code formatted in the DSL that corresponds to the 
        given object, parse the content and store it in the object.
    
        :param filename:  File to read from
        :param cls: Class or object
    '''
    
    with open(filename, 'r') as fp:
        return parse_dsl(fp.read(), obj, filename)


def parse_dsl(string, obj, filename=None):
    '''
        Given a bit of code formatted in the DSL that corresponds to the 
        given object, parse the content and store it in the object.
    
        :param string: String of python code to interpret
        :param cls: Class or object
    '''
    
    if inspect.isclass(obj):
        obj = obj()
    
    # create a wrapper around the object
    dsl_globals = GlobalsObjectProxy(obj, filename)
    
    if filename is None:
        filename = '<string>'
    
    code = compile(string, filename, 'exec')
    
    # TODO: memory leaks warned about in http://lucumr.pocoo.org/2011/2/1/exec-in-python/
    exec code in dsl_globals
    
    # Fix up objects that aren't used
    # -> there's probably a better way to do this
    dsl_globals._clean_up_instance(obj)
    
    # TODO: add 'required' elements to the DSL
       
    return obj
    