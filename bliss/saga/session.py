#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object as SAGAObject

class Session(SAGAObject):
    '''Looesely defines a SAGA Session object as defined in GFD.90.'''

    def __init__(self, urlstring=''):
        '''Construct a new Session.'''
        SAGAObject.__init__(self, SAGAObject.Session)

    def __del__(self):
        '''Destructuror - tear-down the Session object.'''
