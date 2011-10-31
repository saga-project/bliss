#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.context import Context

class Session():
    '''Looesely defines a SAGA Session object as defined in GFD.90.'''

    def __init__(self):
        '''Construct a new Session.'''
        self._contexts = []

    def __del__(self):
        '''Destructor (tear-down the Session object).'''

    def get_session():
        '''Overloaded from saga.Object: just returns itself.'''

    def add_context(self, context):
        '''Add an (authentication) L{Context} to the session.'''
        self._contexts.append(context)

    def remove_context(self, context):
        '''Remove an (authentication) L{Context} to the session.'''
        self._contexts.remove(context)

    def list_contexts(self):
        '''Retrieve all Contexts attached to the session.'''
        return self._contexts
