#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object
from bliss.saga.url import Url


class Description(Object):
    '''Loosely represents a SAGA job description as defined in GFD.90'''
    def __init__(self):
        Object.__init__(self, Object.type_saga_job_description)

        self.executable  = ""
        self.arguments    = []
        self.environment  = {}

    @property
    def executable(self):
        '''The job's executable.'''

        def fget(self):
            return self.executable

        def fset(self, executable):
            self.executable = executable

    @property
    def arguments(self):
        '''The job's executable arguments.'''

        def fget(self):
            return self.arguments

        def fset(self, arguments):
            self.arguments = arguments 

    @property
    def environment(self):
        '''Environment variables to be set in the job's execution context.'''

        def fget(self):
            return self.environment

        def fset(self, arguments):
            self.environment = environment 


