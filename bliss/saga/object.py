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

        self.logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')') 


    def _init_runtime(self):
        '''Registers available plugins and so on'''
        self.__dict__["runtime_instance"] = _Runtime()

    def _set_data(self, key, value):
        self.__dict__[key] = value

    def _get_data(self, key):
        return self.__dict__[key]

    def _bind_object(self):
        '''Bind an object to the runtime'''
        try:
            self.__dict__["runtime_instance"].find_plugin_for_url(self.url) 
        except Exception, ex:
            error = ("Can't instantiate {!s} object because: {!r}.".format(self.__class__.__name__, str(ex)))
            self.logger.error(error)
            raise exception.Exception(exception.Error.NoSuccess, error)
        
