#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object_api import Object
from bliss.saga.attributes_api import AttributeInterface

class WaitMode:
    ''' Specifies the condition on which a wait() operation on
        a L{saga.job.Container} returns.
    '''
  
    Any = "saga.job.WaitMode.Any"
    '''wait() returns only if all tasks in the container
       reach a final state.
    '''
    All = "saga.job.WaitMode.All"
    '''wait() returns if one or more tasks in the container 
       reach a final state.
    '''

class Container(Object):
    '''Loosely represents a SAGA taks container as defined in GFD.90.

       Since Bliss doesn't support the superflous concept of a tasks,
       we decided to rename task container into job container.
    '''
   
    ######################################################################
    ## 
    def __init__(self, service):
        '''Create a new job (a.k.a. 'task') container.
           @param service: Currently, a container needs to be bound to
                           a valid L{saga.job.Service} and can only hold 
                           jobs that are known to that serivce.  
        '''
        Object.__init__(self, Object.Type.JobContainer, apitype=Object.Type.JobAPI)
        
        # parameter checks
        if service.get_type() != Object.Type.JobService:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "Container c'tor expects %s object as parameter" 
                  % (Object.Type.JobService))
      
        self._service = service
        self._url = service._url
        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.container_object_register(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

    ######################################################################
    ##
    def __del__(self):
        '''Delete the container in a civilised fashion.'''
        if self._plugin is not None:
            self._plugin.container_object_unregister(self)
        else:
            pass # destructor. can't throw here

    ######################################################################
    ##
    def add(self, job):
        '''Add a job to the container.
           @param job: A saga.job.Job object in 'New' state.
        '''
        # parameter checks
        if job.get_type() != Object.Type.Job:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
              "add() expects %s object as parameter" % (Object.Type.Job))

        if self._plugin is not None:
            return self._plugin.container_add_job(self, job)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def remove(self, job):
        '''Remove a job from the container.
           @param job: The saga.job.Job object to remove.
        '''
        # parameter checks
        if job.get_type() != Object.Type.Job:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
              "remove() expects %s object as parameter" % (Object.Type.Job))

        if self._plugin is not None:
            return self._plugin.container_remove_job(self, job)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def get_job(self, job_uid):
        '''Get a single job from the job container.
           @param job_uid: The object uid itenifying the job.
        '''
        if self._plugin is not None:
            return self._plugin.container_get_job(self, job_uid)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def get_states(self):
        '''Get the states of all jobs in the container.
        '''
        if self._plugin is not None:
            return self._plugin.container_get_states(self, job)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    
    ######################################################################
    ##
    def list(self):
        '''List all jobs that are in the container.
        '''
        if self._plugin is not None:
            return self._plugin.container_list(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def size(self):
        '''Return the number of elements in the container.
        '''
        if self._plugin is not None:
            return self._plugin.container_size(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def run(self):
        '''Start all jobs in the container.
        '''
        if self._plugin is not None:
            return self._plugin.container_run(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def cancel(self, timeout=0):
        '''Cancel the execution of all jobs in the container.
           @param timeout: Timeout in seconds.
        '''
        if self._plugin is not None:
            return self._plugin.container_cancel(self, timeout)
            return None
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def wait(self, wait_mode=WaitMode.All, timeout=-1):
        '''Wait for jobs in the task container to finish execution.
           @param wait_mode: Wait for any or for all jobs in the container.
           @param timeout: Timeout in seconds.
        '''
        if self._plugin is not None:
            return self._plugin.container_wait(self, wait_mode, timeout)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

