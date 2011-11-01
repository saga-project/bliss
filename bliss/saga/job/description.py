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

    __slots__ = {'_executable', '_arguments', '_environment', '_project',
                  '_output', '_error', '_queue'}

    def __init__(self):
        '''Constructor.'''
        Object.__init__(self, Object.JobDescription)

        self._executable = None
        self._arguments = None
        self._environment = None
        self._project = None
        self._output = None
        self._error = None
        self._queue = None 

    def __del__(self):
        '''Destructor'''

    ######################################################################
    ## Property: executable
    def executable():
        doc = "The job executable."
        def fget(self):
            return self._executable
        def fset(self, val):
            self._executable = val
        def fdel(self, val):
            self._executable = None
        return locals()
    executable = property(**executable())
      
    ######################################################################
    ## Property: arguments
    def arguments():
        doc = "The arguments to pass to the job executable."
        def fget(self):
            return self._arguments
        def fset(self, val):
            self._arguments = val
        def fdel(self, val):
            self._arguments = None
        return locals()
    arguments = property(**arguments())

    ######################################################################
    ## Property: environment
    def environment():
        doc = "The environment variables to set in the job's execution context."
        def fget(self):
            return self._environment
        def fset(self, val):
            self._environment = val
        def fdel(self, val):
            self._environment = None
        return locals()
    environment = property(**environment())


    ######################################################################
    ## Property: output
    def output():
        doc = "The file in which the job\'s stdout stream will be captured."
        def fget(self):
            return self._output
        def fset(self, val):
            self._output = val
        def fdel(self, val):
            self._output = None
        return locals()
    output = property(**output())

    ######################################################################
    ## Property: error
    def error():
        doc = "The file in which the job\'s stderr stream will be captured."
        def fget(self):
            return self._error
        def fset(self, val):
            self._error = val
        def fdel(self, val):
            self._error = None
        return locals()
    error = property(**error())

