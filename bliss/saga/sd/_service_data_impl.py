#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga.object_impl import Object
from bliss.saga.attributes_impl import AttributeInterface


class ServiceData(Object, AttributeInterface):
    '''Loosely represents a SAGA service data object as defined in GFD.R-P.144'''
    def __init__(self):
        '''Construct a new service data object
        '''
        Object.__init__(self, Object.SDServiceData, 
                        apitype=Object.JobAPI,)
        AttributeInterface.__init__(self)


    def __init_from_service_description(self, service_description_obj):
        '''Constructor'''
        self._discoverer = service_description_obj._discoverer
        self._url = self._discoverer._url

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("SerivceData object bound to plugin %s" % (repr(self._plugin)))


    def __del__(self):
        '''Destructor.
        '''
        if self._plugin is not None:
            self._plugin.unregister_discoverer_object(self)


    ######################################################################
    ##
    def attribute_exists(self, key):
        '''Implementation of AttributeInterface'''
        if self._plugin is not None:
            return self._plugin.service_data_attribute_exists(self, key) 
        else:
            raise bliss.saga.Exception(
              bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
    ######################################################################
    ##
    def get_attribute(self, key):
        '''Implementation of AttributeInterface'''
        if self._plugin is not None:
            return self._plugin.service_data_get_attribute(self, key) 
        else:
            raise bliss.saga.Exception(
              bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
    
    ######################################################################
    ##
    def set_attribute(self, key, value):
        '''Implementation of AttributeInterface'''
        raise bliss.saga.Exception(bliss.saga.Error.PermissionDenied,
          "Couldn't set attribute '%s'. ServiceData attributes are read-only!" \
          % (key))

    ######################################################################
    ##
    def remove_attribure(self, key):
        '''Implementation of AttributeInterface'''
        raise bliss.saga.Exception(bliss.saga.Error.PermissionDenied,
          "Couldn't remove attribute '%s'. ServiceData attributes are read-only!" \
          % (key))

