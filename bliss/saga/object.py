#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.runtime import _Runtime

class Object :
    '''Represents a SAGA object as defined in GFD.90'''
    __shared_state = {}
    __shared_state["runtime_initialized"] = False
    def __init__(self):
        '''Construct a new object'''
        self.__dict__ = self.__shared_state
        if not self.__dict__["runtime_initialized"]:
            # initialize runtime
            self._init_runtime()
            self.__dict__["runtime_initialized"] = True

    def _init_runtime(self):
        '''Registers available plugins and so on'''
        self.__dict__["runtime_instance"] = _Runtime()

    def _set_data(self, key, value):
        self.__dict__[key] = value

    def _get_data(self, key):
        return self.__dict__[key]

    def _register_job_service_object(self, obj):
        '''Register a job service object with the runtime'''

    def _register_job_job_object(self, obj):
        ''''Register a job object with the runtime'''
