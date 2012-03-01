#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"



import logging
from bliss.plugins import utils
from bliss.saga.exception_impl import Exception as SAGAException

class PluginBaseInterface:
    '''Abstract base class for all plugins'''

    _api_type_saga_filesystem = "saga.filesystem.cpi"
    _api_type_saga_resource   = "saga.resource.cpi"
    _api_type_saga_job        = "saga.job.cpi"
    _api_type_saga_sd         = "saga.sd.cpi"
    
    def __init__(self, name, schemas, api):
        '''Class constructor'''
        self.name = name
        self.schemas = schemas
        self.supported_apis = []
        self.supported_apis.append(api)

        self.__logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')')

    def get_logger(self):
        '''Return the logger object'''
        return self.__logger

    def log_error_and_raise(self, error, message):
        '''Writes an ERROR to the plugin log and raises an exception'''
        msg = "[%s] %s %s" % (self.name, message, utils.get_traceback())
        self.__logger.error(message)
        raise SAGAException(error, msg)

    def log_debug(self, message):
        '''Writes a DEBUG message to the plugin log'''
        self.__logger.debug(message)

    def log_info(self, message):
        '''Writes an INFO to the plugin log'''
        self.__logger.info(message)
    
    def log_warning(self, message):
        '''Writes a WARNING to the plugin log'''
        self.__logger.warning(message)

    def log_error(self, message):
        '''Writes an ERROR to the plugin log'''
        self.__logger.error(message)
 

    @classmethod
    def supported_apis(self):
        '''Return the api packages this plugin supports'''
        return self._apis

    @classmethod
    def supported_schemas(self):
        '''Implements interface from _PluginBase'''
        return self._schemas

    @classmethod
    def plugin_name(self):
        '''Implements interface from _PluginBase'''
        return self._name

    @classmethod
    def sanity_check(self):
        '''Called upon registring. If an excpetion is thrown, plugin will be disabled.'''
        raise Exception("Requires implementation!")

    def get_runtime_info(self):
        '''This method is used to reveal some runtime information for this plugin'''
  #      raise exception.Exception(exception.Error.NotImplemented, "%s: get_runtime_info() is not supported by this plugin".format(repr(self))) 

