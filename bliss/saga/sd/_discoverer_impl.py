#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga.object_impl import Object as SObject
from bliss.saga.exception_impl import Exception as SException
from bliss.saga.exception_impl import Error as SError
from bliss.saga.url_impl import Url

class Discoverer(SObject):
    '''Loosely represents a SAGA service discoverer as defined in GFD.R-P.144'''
    def __init__(self, url, session=None):
        '''Construct a new service discoverer object
           @param url: Url of the (remote) service provider.
           @type  url: L{Url} 
        '''
        if(type(url) == str):
            self._url = Url(str(url))
        else:
            # assume it's a URL object
            self._url = url

        SObject.__init__(self, objtype=SObject.SDDiscoverer, 
                        apitype=SObject.SDAPI, session=session)
        self._plugin = SObject._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_discoverer_object(self)
        self._logger.info("Discoverer object bound to plugin %s" % (repr(self._plugin)))

    def __del__(self):
        '''Destructor.
        '''
        if self._plugin is not None:
            self._plugin.unregister_discoverer_object(self)

    ######################################################################
    ##
    def list_services(self, service_filter=None, data_filter=None):
        '''Returns the set of services that pass the set of specified filters.
        '''
        if self._plugin is None:
            raise SException(SError.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.discoverer_list_services(self, 
              service_filter, data_filter)

