#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga._object_impl import Object 

class Compute(Object):

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new compute resource.
        '''
        Object.__init__(self, Object.ResourceComputeResource, 
                        apitype=Object.ResourceAPI, session=session)

    ######################################################################
    ##
    def __init_from_manager(self, manager_obj, compute_description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url = manager_obj._url
        self._compute_description = compute_description

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))
