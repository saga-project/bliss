#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga._object_impl import Object 

class Manager(Object):
    '''Loosely defines a SAGA Resource object as defined in GWD-R.xx'''

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new resource manager object
           @param url: Url of the (remote) resource manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.ResourceService, 
                        apitype=Object.ResourceAPI, session=session)

        if(type(url) == str):
            self._url = Url(str(url))
        else:
            self._url = url

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_service_object(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

    ######################################################################
    ## 
    def __del__(self):
        '''Delete the manager in a civilised fashion.'''
        if self._plugin is not None:
            self._plugin.unregister_service_object(self)
        else:
            pass # can't throw here


