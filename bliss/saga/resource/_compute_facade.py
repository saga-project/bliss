#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
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


    ######################################################################
    ##
    def wait(self, state, timeout=-1):
        '''Wait for the compute resource to reach a specific state.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.compute_wait(self, state, timeout)


    ######################################################################
    ##
    def get_state(self):
        '''Return the state of the compute resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.compute_get_state(self, job_description)

    
    ######################################################################
    ##
    def get_manager(self):
        '''Return the associated resource manager object.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.compute_get_manager(self, job_description)
    

    ######################################################################
    ##
    def get_description(self): 
        '''Return the associated (compute) resource description object.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._compute_description 
