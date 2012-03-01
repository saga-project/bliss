#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga                           import Url
from bliss.saga.resource.resource_api import Resource as SResource


class Network(SResource):

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new network resource.
        '''
        Object.__init__(self, Object.ResourceNetworkResource, 
                        apitype=Object.ResourceAPI, session=session)


    ######################################################################
    ##
    #  FIXME: not sure if that should be overloaded or not...
    def __init_from_manager(self, manager_obj, network_description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url     = manager_obj._url
        self._network_description = network_description

        self._plugin  = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))


