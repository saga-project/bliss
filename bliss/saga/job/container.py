#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import copy
from bliss.saga.object import Object
from bliss.saga.attributes import AttributeInterface
from bliss.saga import exception



class WaitMode:
    Any = "Any"
    '''wait() returns only if all tasks in the container
       reach a final state.'''
    All = "All"
    '''wait() returns if one or more tasks in the container 
       reach a final state.'''

class Container(Object):
    '''Loosely represents a SAGA taks container as defined in GFD.90.
       Since Bliss doesn't support the superflous concept of a task,
       we decided to rename task container into job container.
    '''
    
    def __init__(self, service):
        '''Create a new task container.
           @param service: currently, a container needs to be bound to
                           a valid saga.job.Service. 
        '''
        Object.__init__(self, Object.JobContainer, apitype=Object.JobAPI)
        
        # parameter checks
        if service.get_type() != Object.JobService:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "Container c'tor expects %s object as parameter" 
                  % (Object.JobService))
      
        self._service = service
        self._url = service._url
        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Container object bound to plugin %s" % (repr(self._plugin)))

    #def __del__(self):
    #    '''Tear down the object in a more or less civilised fashion.'''
    #    if self._plugin is not None:
    #        self._plugin.unregister_job_object(self)
    #    else:
    #        pass # can't throw here

    def add(self, job_obj):
        '''Add a job to the container.
           @param job_obj: A saga.job.Job object in 'New' state.
        '''
        # parameter checks
        if service.get_type() != Object.Job:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "add() expects %s object as parameter" 
                  % (Object.Job))

    def remove(self, job_obj):
        '''Remove a job from the container.
           @param job_obj: The saga.job.Job object to remove.
        '''
        # parameter checks
        if service.get_type() != Object.Job:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "remove() expects %s object as parameter" 
                  % (Object.Job))

    def list(self):
        '''List all jobs that are in the container.
        '''

    def size(self):
        '''Return the number of elements in the container.
        '''

    def run(self):
        '''Execute the job via the associated job service.'''
        if self._plugin is not None:
            return self._plugin.job_run(self)
            return None
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

    def cancel(self, timeout=0):
        '''Cancel the execution of the job.
           @param timeout: Timeout in seconds.
        '''
        if self._plugin is not None:
            return self._plugin.job_container_cancel(self, timeout)
            return None
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

    def wait(self, wait_mode=WaitMode.All, timeout=-1):
        '''Wait for jobs in the task container to finish execution.
           @param wait_mode: Wait for any or for all jobs in the container.
           @param timeout: Timeout in seconds.
        '''
        if self._plugin is not None:
            return self._plugin.job_container_wait(self, timeout)
            return None
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

