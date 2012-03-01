#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.context_impl import Context

class Session(object):
    '''Looesely defines a SAGA Session object as defined in GFD.90.'''

    #__slots__ = {'_contexts'}

    ######################################################################
    ## 
    def __init__(self):
        '''Constructor.
        '''
        self._contexts = []
        '''Authentication / security contexts registered with the Session.'''

    ######################################################################
    ## 
    def __del__(self):
        '''Destructor.
        '''
        pass

    ######################################################################
    ## 
    def __str__(self):
        '''String represenation.
        '''
        return "Registered contexts: % s" % (str(self.contexts))

    ######################################################################
    ## Property: type
    def contexts():
        doc = "Authentication contexts registered with the Session."
        def fget(self):
            return self._contexts
        def fset(self, val):
            self._contexts = val
        #def fdel(self, val):
        #    self._contexts.remove(val)
        return locals()
    contexts = property(**contexts())

    ######################################################################
    ## 
    def add_context(self, context):
        '''Legacy GFD.90 method: add a security L{Context} to the session.

           It is encouraged to use the L{contexts} property instead. 
        '''
        self._contexts.append(context)

    ######################################################################
    ## 
    def remove_context(self, context):
        '''Legacy GFD.90 method: remove a security L{Context} from the session.

           It is encouraged to use the L{contexts} property instead.
        '''
        self._contexts.remove(context)

    ######################################################################
    ## 
    def list_contexts(self):
        '''Legacy GFD.90 method: retrieve all L{Context} objects attached to the session.


           It is encouraged to use the L{contexts} property instead.
        '''
        return self._contexts
