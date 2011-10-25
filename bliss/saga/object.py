#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import logging
from bliss.saga import exception
from bliss.runtime import _Runtime

class Object :
    '''Loosely resembles a SAGA object as defined in GFD.90'''

    type_saga_job_job         = "saga.job.Job"
    type_saga_job_service     = "saga.job.Service"
    type_saga_job_description = "saga.job.Description"

    __shared_state = {}
    __shared_state["runtime_initialized"] = False
    def __init__(self, objtype):
        '''Construct a new object'''
        #self.__dict__ = self.__shared_state
        if not self.__shared_state["runtime_initialized"]:
            # initialize runtime
            self._init_runtime()
            self.__shared_state["runtime_initialized"] = True

        self.plugin = None
        self.type = objtype
        self.logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')') 

    def _init_runtime(self):
        '''Registers available plugins and so on'''
        if not self.__shared_state["runtime_initialized"]: 
            self.__shared_state["runtime_instance"] = _Runtime()

    def _get_plugin(self):
        '''Bind an object to the runtime'''
        try:
            return self.__shared_state["runtime_instance"].get_plugin_for_url(self.url) 
        except Exception, ex:
            error = ("{!s}".format(str(ex)))
            raise exception.Exception(exception.Error.NoSuccess, error)

    def _get_runtime_info(self):
        return self.plugin.get_runtime_info()
        
