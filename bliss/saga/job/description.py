#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object
from bliss.saga.attributes import AttributeInterface
from bliss.saga.url import Url


class Description(Object, AttributeInterface):
    '''Loosely represents a SAGA job description as defined in GFD.90'''
    def __init__(self):
        '''Constructor - create an empty job description.'''
        Object.__init__(self, Object.JobDescription)
        AttributeInterface.__init__(self)

        self._attributes['Arguments']    = {'value':[], 'type':'V', 'access':'RW'} 
        self._attributes['Environment']  = {'value':{}, 'type':'V', 'access':'RW'}
        self._attributes['Project']      = {'value':[], 'type':'V', 'access':'RW'}

        self._attributes['Executable']   = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['Output']       = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['Error']        = {'value':"", 'type':'S', 'access':'RW'}
        self._attributes['Queue']        = {'value':"", 'type':'S', 'access':'RW'}






