# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.Object import Object 

class Storage(Object):
    ''' Storage resources represent stateful entities which can store
    data.  A L{resource.Manager} instance can create them according to
    a L{resource.StorageDescription}, as shown below::

      # describe the resource requirements
      sd = saga.resource.StorageDescription ()
      sd['Size'] = 1024    # MB

      # obtain a handle to a suitable resource...
      rm = saga.resource.Manager (url)
      sr = rm.create_storage (sd)

      # ... and wait until the storage space is available
      sr.wait (saga.resource.State.Active)
    '''

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new storage resource.
        '''
        Object.__init__(self, Object.Type.ResourceStorage, 
                        apitype=Object.Type.ResourceAPI)


    ######################################################################
    ##
    def __init_from_manager(self, manager_obj, storage_description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url     = manager_obj._url
        self._storage_description = storage_description
        
        self._plugin  = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))
    
    ######################################################################
    ##
    def get_state(self):
        # FIXME: as Bliss does not have async ops, the semantics descriped
        # below does not make much sense....
        '''Return the state of the resource.
        
        A resource will only be able to store data when in Active state -- but it may
        already accept storage requests while Pending.  In that case, the
        storage requests are queued until the resource becomes Active.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.storage_resource_get_state(self)
    
    
    ######################################################################
    ##
    def get_state_detail(self):
        '''Return the state detail of the resource.
        
        As for every stateful Bliss object, the state detail informs about the
        actual native backend state, which may be finer grained than the SAGA
        state model used by Bliss.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.storage_resource_get_state_detail(self)
    
    
    ######################################################################
    ##
    def get_id(self):
        '''Return the id of the resource
        
        The returned ID acts as a persistent and unique identifier for the
        resource...::
        
          
          # obtain a handle to a suitable resource and print it's id
          rm = saga.resource.Manager (url)
          sr = rm.create_storage (sd)
          id = sr.get_id ()
          print "resource id: %s"  %  id


        ...and can in particular be used to reconnect to that existing
        resource::

          rm = saga.resource.Manager (url)
          sr = rm.get_storage (id)
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.storage_resource_get_id(self)
    
    
    ######################################################################
    ##
    def get_manager(self):
        '''Return the associated resource manager object.

        The returned manager is the one which created or reconnected to the
        resource::
        
          # obtain a handle to a suitable resource and print it's id
          rm1 = saga.resource.Manager (url)
          sr  = rm.create_storage (sd)
          rm2 = sr.get_manager ()

          assert ( rm1 == rm2 )
        
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.storage_resource_get_manager(self)
    
    
    ######################################################################
    ##
    def get_description(self): 
        '''Return the associated resource description object.

        The returned description describes the actual resource properties, and
        may differ from the description submitted when creating the resource.
        In particular, the returned description here describes the *actual*
        resource properties, which may differ from the ones defined initially::
        
          # describe the resource requirements
          sd = saga.resource.StorageDescription ()
          sd['Size'] = 1024 # MB

          # obtain a handle to a suitable resource, and inspect it
          rm1 = saga.resource.Manager (url)
          sr  = rm.create_compute (sd)
          sd2 = sr.get_description

          print   " requested : %d   / allocated : %d"    %  1024, sd2['Size']
          # prints: requested : 1024 / allocated : 2048"  %  1024, sd2['Size']
        
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.storage_resource_get_description(self)
    
    ######################################################################
    ##
    def destroy(self, drain=False):
        # FIXME: as Bliss does not have async ops, the drain semantics described
        # below does not make much sense....
        '''Destroy (close) the resource.
        
        This method is *not* just a destructor for the Bliss API object, but
        rather signals the backend that the resource is not needed anymore, and
        can be released.  All data on that resource will subsequently be purged
        -- but setting the optional 'drain' flag to 'True' can request that the
        actual resource release is delayed by the backend until all current data
        transfer operations have reached a final state.  Either way, no new 
        data transfer requests can be started for the resource after calling 
        destroy().
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.storage_resource_destroy(self, drain)
    
    
    ######################################################################
    ##
    def wait(self, timeout=-1, state="Final"):
        '''Wait for the resource to reach a specific state.

        As resources are stateful entities, and several actions (such as data
        transfers) are only allowed in very specific states, the wait() routine
        can be used to wait for the resource to reach a specific state.  By
        default, wait() will block until the resource reaches a final state
        (Destroyed, Expired or Failed), but the optional 'state' parameter can
        specify any other combination of states to wait for.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.storage_resource_wait(self, state)

    ######################################################################
    ##
    def get_filesystem(self): 
        # FIXME: this is assymetric: either have
        #
        #   d  = saga.filesystem.Directory (sr)
        #   js = saga.job.Service          (cr)
        #
        # or
        #
        #   d  = sr.get_filesystem  ()
        #   js = cr.get_job_service ()
        #
        '''get access to the storage resource's file system.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.storage_resource_get_filesystem (self) 

