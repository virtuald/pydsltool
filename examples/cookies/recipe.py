#!/usr/bin/env python

import os.path
import sys
import dsltool


#
# When the DSL is executed, the methods and attributes of these objects
# are called
#

class Ingredients(object):
    
    def __init__(self):
        self._items = []
    
    @property
    def add(self):
        '''
            Uses a utility that gives the DSL a syntax to add to a list:
            
                with Ingredients:
                    add += 'item'
                    ...
            
        '''
        return dsltool.add_to_list(self._items)
    
    @add.setter
    def add(self, value):
        self._items = value


class Steps(object):
    '''Example of how to record whatever the user throws at you'''
        
    def __init__(self):
        self._steps = []
    
    def __getattr__(self, name):
        return lambda *args: self._steps.append([name] + list(args))


class Instructions(object):
    preheat_oven = None
    
    #
    # When the DSL is executed, attributes that have a class object assigned 
    # to them are used by the DSL in 'with' statements. The attribute
    # must be a snake cased version of the class name.  
    #
    
    ingredients = Ingredients
    steps = Steps
    
    def __init__(self, name):
        self.name = name
        

class Recipe(object):
    '''This is the base object, so the DSL code is interpreted with this
       object's methods/attributes as its context'''
    
    author = None
    level = None
    
    def __init__(self):
        self.instructions = dsltool.list_of(Instructions)

# 
# Main
#

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        filename = os.path.join(os.path.dirname(__file__), 'cookies.pydsl')
    else:
        filename = sys.argv[1]
    
    recipe = dsltool.parse_dsl_file(filename, Recipe()) 

    # display the parsed recipe
    print 'Author: %s' % recipe.author
    print 'Level : %s' % recipe.level
    
    for instructions in recipe.instructions:
        print 'Instructions for %s:' % instructions.name
        print '  Preheat oven: %s' % instructions.preheat_oven
        print '  Ingredients:'
        
        if instructions.ingredients is not None:
            for quantity, ingredient in instructions.ingredients._items:
                print '    %s %s' % (quantity, ingredient)
    
        print '  Steps:'
        if instructions.steps is not None:
            for step in instructions.steps._steps:
                print '    %s' % ' '.join(step)
    
    
