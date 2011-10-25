#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

_api_type_saga_job = "saga.job"
_api_type_saga_file = "saga.file"

import logging
from bliss.saga import exception

class _PluginBase:
    '''Abstract base class for all plugins'''
    
    def __init__(self, name):
        '''Class constructor'''
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')') 
    
    @classmethod
    def supported_schemas(self):
        '''Return a list of all url schemas supported by this plugin'''
        raise Exception("Requires implementation!")
        
    @classmethod
    def supported_api(self):
        '''Return the api package this plugin supports'''
        raise Exception("Requires implementation!")
        
    @classmethod
    def plugin_name(self):
        '''Return the name of this plugin'''
        raise Exception("Requires implementation!")
        
    @classmethod
    def sanity_check(self):
        '''Called upon registring. If an excpetion is thrown, plugin will be disabled.'''
        raise Exception("Requires implementation!")

    def get_runtime_info(self):
        '''This method is used to reveal some runtime information for this plugin'''
        raise exception.Exception(NotImplemented, "{!s}: get_runtime_info() is not supported by this plugin".format(repr(self))) 

