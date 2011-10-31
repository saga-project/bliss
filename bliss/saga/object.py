#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import logging
import bliss.saga
import bliss.runtime

class Object(object) :
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

    __slots__ = ("_plugin", "type", "_logger", "session")

    def __init__(self, objtype, session=None):
        '''Construct a new object'''
 
        if not self.__shared_state["runtime_initialized"]:
            # initialize runtime
            self._init_runtime()
            self.__shared_state["default_session"] = bliss.saga.Session()
            self.__shared_state["runtime_initialized"] = True

        self._plugin = None
        self.type = objtype
        self._logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')')
 
        if session is not None:
            self.session = session
        else:
            self.session = self.__shared_state["default_session"]

    def _init_runtime(self):
        '''Registers available plugins and so on'''
        if not self.__shared_state["runtime_initialized"]: 
            self.__shared_state["runtime_instance"] = bliss.runtime.Runtime()

    def _get_plugin(self):
        '''Bind an object to the runtime'''
        try:
            return self.__shared_state["runtime_instance"].get_plugin_for_url(self.url) 
        except Exception, ex:
            error = ("%s" % (str(ex)))
            raise SException(SError.NoSuccess, error)

    def _get_runtime_info(self):
        return self.plugin.get_runtime_info()

    def get_session(self):
        '''Legacy method: return the object's session.'''
        if self.session is None:
            pass # return default session
        else:
           return self.session

    def get_type(self):
        '''Legacy method: return the object type.'''
        return self.type

    def get_id(self):
        '''Legacy method: Return the object identifier.'''
        return repr(self) 
