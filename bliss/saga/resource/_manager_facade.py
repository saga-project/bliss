#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.object_impl import Object 

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
        self._plugin.register_manager_object(self)
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
    def list_resources(self, r_type="*"):
        '''List known resource ids'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_list_resources(self, r_type)

    ######################################################################
    ## 
    def describe_resource(self, r_id):
        '''get resource description'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_describe_resource(self, r_id)

    ######################################################################
    ## 
    def list_templates(self, ttype="*"):
        '''List available template names'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_list_templated(self, ttype)

    ######################################################################
    ## 
    def describe_template(self, t_id):
        '''get template description'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_describe_template(self, t_id)

    ######################################################################
    ## 
    def get_resource(self, r_id):
        '''get resource handle for some id'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_get_resource(self, r_id)

    ######################################################################
    ## 
    def create_compute(self, compute_description):
        '''Instantiate (request) a new compute resource'''

        if description.get_type() != Object.ResourceComputeDescription:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_compute() expects %s object as parameter" 
                  % (Object.ResourceComputeDescription))

        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_create_compute(self, description)


    ######################################################################
    ## 
    def get_compute(self, compute_id):
        '''Return the resource handle for an existing compute resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_get_compute(self, compute_id)


    ######################################################################
    ## 
    def get_compute(self, js_instance):
        '''Return the resource handle for a legacy saga.job.service'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_get_compute(self, js_instance)


    ######################################################################
    ## 
    def destroy_compute(self, compute_id, drain=False):
        '''Destroy (close) an existing compute resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_destroy_compute(self, compute_id, drain)


    ######################################################################
    ## 
    def create_storage(self, storage_description):
        '''Instantiate (request) a new storage resource'''

        if description.get_type() != Object.ResourceStorageDescription:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_storage() expects %s object as parameter" 
                  % (Object.ResourceStorageDescription))

        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_create_storage(self, description)


    ######################################################################
    ## 
    def get_storage(self, storage_id):
        '''Return the resource handle for an existing storage resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_get_storage(self, storage_id)


    ######################################################################
    ## 
    def get_storage(self, fs_instance):
        '''Return the resource handle for a legacy saga.filesystem::directory'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_get_storage(self, fs_instance)


    ######################################################################
    ## 
    def destroy_storage(self, storage_id, drain=False):
        '''Destroy (close) an existing storage resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_destroy_storage(self, storage_id, drain)


    ######################################################################
    ## 
    def create_network(self, network_description):
        '''Instantiate (request) a new network resource'''

        if description.get_type() != Object.ResourceNetworkDescription:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_network() expects %s object as parameter" 
                  % (Object.ResourceNetworkDescription))

        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_create_network(self, description)


    ######################################################################
    ## 
    def get_network(self, network_id):
        '''Return the resource handle for an existing network resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_get_network(self, network_id)


    ######################################################################
    ## 
    def destroy_network(self, network_id, drain=False):
        '''Destroy (close) an existing network resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_destroy_network(self, network_id, drain)


    ######################################################################
    ## 
    def create_pool(self, pool_description):
        '''Instantiate (request) a new pool resource'''

        if description.get_type() != Object.ResourcePoolDescription:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_pool() expects %s object as parameter" 
                  % (Object.ResourcePoolDescription))

        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_create_pool(self, description)


    ######################################################################
    ## 
    def get_pool(self, pool_id):
        '''Return the resource handle for an existing pool resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_get_pool(self, pool_id)


    ######################################################################
    ## 
    def destroy_pool(self, pool_id, drain=False):
        '''Destroy (close) an existing pool resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.manager_destroy_pool(self, pool_id, drain)


