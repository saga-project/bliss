# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga

from bliss.saga import Url
from bliss.saga.Object import Object 

class Compute(Object):
    ''' Compute resources represent stateful entities which can run compute
    jobs.  A :class:`bliss.saga.resource.Manager` instance can create them according to
    a :class:`bliss.saga.resource.ComputeDescription`, as shown below::

      # describe the resource requirements
      cd = saga.resource.ComputeDescription()
      cd['Slots'] = 1024

      # obtain a handle to a suitable resource...
      rm = saga.resource.Manager(url)
      cr = rm.create_compute(cd)

      # ... and wait until it is active
      cr.wait(saga.resource.State.Active)
    '''

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new compute resource.
        '''
        Object.__init__(self)
        self._apitype = 'saga.resource'


    ######################################################################
    ##
    def __init_from_manager(self, manager_obj, compute_description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url = manager_obj._url
        self._compute_description = compute_description

        self._plugin  = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

    ######################################################################
    ##
    def get_state(self):
        '''Return the state of the resource
        
        A resource will only be running jobs when in Active state -- but it may
        already accept job submission requests while Pending.  In that case, the
        job requests are queued until the resource becomes Active.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.compute_resource_get_state(self)
    
    
    ######################################################################
    ##
    def get_state_detail(self):
        '''Return the state detail of the resource.
        
        As for every stateful SAGA-Python object, the state detail informs about the
        actual native backend state, which may be finer grained than the SAGA
        state model used by SAGA-Python.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.compute_resource_get_state_detail(self)
    
    
    ######################################################################
    ##
    def get_id(self):
        '''Return the id of the resource.
        
        The returned ID acts as a persistent and unique identifier for the
        resource...::
        
          
          # obtain a handle to a suitable resource and print it's id
          rm = saga.resource.Manager(url)
          cr = rm.create_compute(cd)
          id = cr.get_id()
          print "resource id: %s"  %  id


        ...and can in particular be used to reconnect to that existing
        resource::

          rm = saga.resource.Manager(url)
          cr = rm.get_compute(id)
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.compute_resource_get_id(self)
    
    
    ######################################################################
    ##
    def get_manager(self):
        '''Return the associated resource manager object.

        The returned manager is the one which created or reconnected to the
        resource::
        
          # obtain a handle to a suitable resource and print it's id
          rm1 = saga.resource.Manager(url)
          cr  = rm.create_compute(cd)
          rm2 = cr.get_manager()

          assert(rm1 == rm2)
        
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.compute_resource_get_manager(self)
    
    
    ######################################################################
    ##
    def get_description(self): 
        '''Return the associated resource description object.

        The returned description describes the actual resource properties, and
        may differ from the description submitted when creating the resource.
        In particular, the returned description here describes the *actual*
        resource properties, which may differ from the ones defined initially::
        
          # describe the resource requirements
          cd = saga.resource.ComputeDescription()
          cd['Slots'] = 1000

          # obtain a handle to a suitable resource, and inspect it
          rm1 = saga.resource.Manager(url)
          cr  = rm.create_compute(cd)
          cd2 = cr.get_description

          print   " requested : %d   / allocated : %d"    %  1024, cd2['Slots']
          # prints: requested : 1000 / allocated : 1024"  %  1024, cd2['Slots']
        
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
       
        cd = self._plugin.compute_resource_get_description(self)
        cd_copy = bliss.saga.resource.ComputeDescription._deep_copy(cd) 
        return cd
    
    ######################################################################
    ##
    def destroy(self):
        '''Destroy (close) the resource.
        
        This method is *not* just a destructor for the SAGA-Python API object, but
        rather signals the backend that the resource is not needed anymore, and
        can be released.  All jobs on that resource will subsequently be killed,
        and no new job requests can be scheduled for the resource after calling 
        destroy().
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.compute_resource_destroy(self)
    
    
    ######################################################################
    ##
    def wait(self, timeout=-1, state=2):
        '''Wait for the resource to reach a specific state.

        As resources are stateful entities, and several actions (such as job
        submission) are only allowed in very specific states, the wait() routine
        can be used to wait for the resource to reach a specific state.  By
        default, wait() will block until the resource reaches a final state
        (Destroyed, Expired or Failed), but the optional 'state' parameter can
        specify any other combination of states to wait for.
        '''

        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
                                       "Object not bound to a plugin")
        
        return self._plugin.compute_resource_wait(self, timeout, state)

    ######################################################################
    ##
    def get_job_service(self): 
        '''get access to the resource's job manager.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.compute_resource_get_job_service(self) 

