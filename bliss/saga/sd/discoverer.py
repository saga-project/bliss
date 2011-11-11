#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga.object import Object 
from bliss.saga import exception
from bliss.saga.url import Url

class Discoverer(Object):
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

        Object.__init__(self, objtype=Object.SDDiscoverer, 
                        apitype=Object.SDAPI, session=session)
        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_service_object(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

    def __del__(self):
        '''Destructor.
        '''
        #if self._plugin is not None:
        #    self._plugin.unregister_service_object(self)

    ######################################################################
    ##
    def list_services(self, service_filter=None, data_filter=None):
        '''Returns the set of services that pass the set of specified filters.
           @param job_id: The job id.
        '''
        if self._plugin is None:
            raise exception.Exception(exception.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.discoverer_list_services(self, 
              service_filter, data_filter)

