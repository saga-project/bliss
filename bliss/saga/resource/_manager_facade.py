#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga._object_impl import Object 

class Manager(Object):

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new resource manager object
           @param url: Url of the (remote) resource manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.ResourceManager, 
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

    ######################################################################
    ## 
    def list_ids(self, filter="*"):
        '''List known instances'''
        if self._plugin is not None:
            return self._plugin.manager_list_ids(self, filter)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ## 
    def list_templates(self, filter="*"):
        '''List available templates'''
        if self._plugin is not None:
            return self._plugin.manager_list_templated(self, filter)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ## 
    def create_compute(self, description):
        '''Instantiate (request) a new compute resource'''

        if description.get_type() != Object.ResourceComputeDescription:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_compute() expects %s object as parameter" 
                  % (Object.ResourceComputeDescription))

        if self._plugin is not None:
            return self._plugin.manager_create_compute(self, description)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ## 
    def get_compute(self, compute_id):
        '''Return the resource handle for an existing compute resource'''
        if self._plugin is not None:
            return self._plugin.manager_get_compute(self, compute_id)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ## 
    def release_compute(self, compute_id):
        '''Release (close) an existing compute resource'''
        if self._plugin is not None:
            return self._plugin.manager_release_compute(self, compute_id)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ## 
    def create_storage(self, description):
        '''Instantiate (request) a new storage resource'''
        if self._plugin is not None:
            return self._plugin.manager_create_storage(self, description)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ## 
    def get_storage(self, storage_id):
        '''Return the resource handle for an existing storage resource'''
        if self._plugin is not None:
            return self._plugin.manager_get_storage(storage_id)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ## 
    def release_storage(self, storage_id):
        '''Release (close) an existing storage resource'''
        if self._plugin is not None:
            return self._plugin.manager_release_storage(storage_id)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

