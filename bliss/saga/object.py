#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import logging

from bliss.saga.exception  import Exception as SException
from bliss.saga.exception  import Error as SError
from bliss.runtime.runtime import Runtime

class Object :
    '''Loosely resembles a SAGA object as defined in GFD.90'''

    Url            = "saga.Url"
    '''saga.Url object type.'''
    Session        = "saga.Session"
    '''saga.Session object type.'''
    Context        = "saga.Context"
    '''saga.Context object type.'''
    Job            = "saga.job.Job"
    '''saga.job.Job object typ.e'''
    JobService     = "saga.job.Service"
    '''saga.job.Service object type.'''
    JobDescription = "saga.job.Description"
    '''saga.job.Description object type.'''

    __shared_state = {}
    __shared_state["runtime_initialized"] = False
    def __init__(self, objtype):
        '''Construct a new object'''
        #self.__dict__ = self.__shared_state
        if not self.__shared_state["runtime_initialized"]:
            # initialize runtime
            self._init_runtime()
            self.__shared_state["runtime_initialized"] = True

        self._plugin = None
        self._type = objtype
        self._logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')')
        self._session = None 

    def _init_runtime(self):
        '''Registers available plugins and so on'''
        if not self.__shared_state["runtime_initialized"]: 
            self.__shared_state["runtime_instance"] = Runtime()

    def _get_plugin(self):
        '''Bind an object to the runtime'''
        try:
            return self.__shared_state["runtime_instance"].get_plugin_for_url(self.url) 
        except Exception, ex:
            error = ("{!s}".format(str(ex)))
            raise SException(SError.NoSuccess, error)

    def _get_runtime_info(self):
        return self.plugin.get_runtime_info()

    def get_session(self):
        '''Return the object's session.'''
        if self._session is None:
            pass # return default session

    def get_type(self):
        '''Return the object type.'''
        return self._type

    def get_id(self):
        '''Return the object identifier.'''
        return repr(self) 

