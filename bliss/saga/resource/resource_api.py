# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.object_api import Object 

class Resource(Object):
    ''' FIXME: Ole, make this an interface if you want '''

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new resource.
        '''
        Object.__init__(self, Object.ResourcResource, 
                        apitype=Object.ResourceAPI, session=session)


    ######################################################################
    ##
    def __init_from_manager(self, manager_obj, description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url     = manager_obj._url
        self._description = description

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))


    ######################################################################
    ##
    def get_type(self):
        '''Return the type of the resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
        return self._plugin.get_type(self)

    
    ######################################################################
    ##
    def get_state(self):
        '''Return the state of the resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
        return self._plugin.get_state(self)

    
    ######################################################################
    ##
    def get_state_detail(self):
        '''Return the state detail of the resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
        return self._plugin.get_state_detail(self)

    
    ######################################################################
    ##
    def get_id(self):
        '''Return the id of the resource'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
        return self._plugin.get_id(self)

    
    ######################################################################
    ##
    def get_manager(self):
        '''Return the associated resource manager object.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
        return self._plugin.get_manager(self)
    

    ######################################################################
    ##
    def get_description(self): 
        '''Return the associated resource description object.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
        return self._description 

    ######################################################################
    ##
    def destroy(self, drain=False):
        '''Destroy (close) the resource.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        
        return self._plugin.destroy(self, drain)


    ######################################################################
    ##
    def wait(self, timeout=-1, state="Final"):
        '''Wait for the resource to reach a specific state.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.wait(self, state, timeout)


