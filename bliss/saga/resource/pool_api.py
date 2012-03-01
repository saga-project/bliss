#!env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.resource.resource_api import Resource as SResource

class Pool(SResource):

    ######################################################################
    ## 
    def __init__(self):
        '''Create a new (empty) resource pool.
        '''
        Object.__init__(self, Object.ResourcePool, 
                        apitype=Object.ResourceAPI, session=session)

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_service_object(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))


    ######################################################################
    ##
    #  FIXME: not sure if that should be overloaded or not...
    def __init_from_manager(self, manager_obj, pool_description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url     = manager_obj._url
        self._network_description = pool_description

        self._plugin  = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))


    ######################################################################
    ##
    def add(self, resource): 
        '''add a resource to the managed pool.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.add (resource) 


    ######################################################################
    ##
    # FIXME:  I don't think overloading like this makes sense in python?
    def add(self, id): 
        '''add an identified resource to the managed pool.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.add (id) 


    ######################################################################
    ##
    def remove(self, resource): 
        '''remove a resource from the managed pool.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.remove (resource) 


    ######################################################################
    ##
    # FIXME:  I don't think overloading like this makes sense in python?
    def remove(self, id): 
        '''remove an identified resource from the managed pool.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.remove (id) 


    ######################################################################
    ##
    def list(self, r_type="*"): 
        '''list resources in the managed pool.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.list (r_type) 


    ######################################################################
    ##
    def get(self, id):
        '''get resource from the managed pool.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.get (id) 


    ######################################################################
    ##
    def list_policies(self):
        '''list available pool policy names.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.list_policies () 


    ######################################################################
    ##
    def describe_policy(self, name):
        '''describe a pool policy.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.describe_policy (name) 


    ######################################################################
    ##
    def set_policy(self, name):
        '''set a pool policy.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.set_policy (name) 


    ######################################################################
    ##
    def get_compute(self):
        '''get an interface to the pool's compute capabilities'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.get_compute (name) 


    ######################################################################
    ##
    def get_storage(self):
        '''get an interface to the pool's storage capabilities'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.get_storage (name) 


    ######################################################################
    ##
    def get_network(self):
        '''get an interface to the pool's network capabilities'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.get_network (name) 


