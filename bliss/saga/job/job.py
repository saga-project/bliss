#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import copy
from bliss.saga.object import Object
from bliss.saga import exception

class Job(Object):
    '''Loosely represents a SAGA job as defined in GFD.90'''
    
    Canceled = "Canceled"
    '''Indicates that the job has been canceled either by the user or the system'''
    Done     = "Done"
    '''Indicates that the job has successfully executed''' 
    Failed   = "Failed"
    '''Indicates that the execution of the job has failed'''
    New      = "New"
    '''Indicates that the job hasn't been started yet'''
    Running  = "Running"
    '''Indicates that the job is executing'''
    Unknown  = "Unknown"
    '''Indicates that the job is in an unexpected state'''

    def __init__(self):
        '''Constructor - not to be called directly'''
        Object.__init__(self, Object.Job)

    def __init_from_service(self, service_obj, job_desc):
        '''Constructor'''
        self.service = service_obj
        self.url = service_obj.url
        self._job_description = job_desc

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_job_object(job_obj=self, service_obj=self.service)
        self._logger.info("Object bound to plugin {!s}".format(repr(self._plugin)))

    def __del__(self):
        '''Tear down the object in a more or less civilised fashion.'''
        if self._plugin is not None:
            self._plugin.unregister_job_object(self)
        else:
            pass # can't throw here

    def get_stderr(self):
        '''B{Not Implemented:} Bliss finds this method unnecessary and generally poorly \
           supported by distributed middelware - use U{Air<http://oweidner.github.com/air/>} \
           instead for scalable output streaming and much more.
        '''

        raise exception.Exception(exception.Error.NotImplemented, "Bliss doesn't suppport get_stderr()")

    def get_stdout(self):
        '''B{Not Implemented:} Bliss finds this method unnecessary and generally poorly \
           supported by distributed middleware - use U{Air<http://oweidner.github.com/air/>}  \
           instead for scalable output streaming and much more.
        '''
        raise exception.Exception(exception.Error.NotImplemented, "Bliss doesn't suppport get_stdout()")

    def get_description(self):
        '''Return the job description this job was created from.'''
        if self._plugin is not None:
            return self._job_description
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

    def get_state(self):
        '''Return the current state of the job.'''
        if self._plugin is not None:
            return self._plugin.job_get_state(self)
            return None
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

    def get_job_id(self):
        '''Return the identifier for the job (B{I{not officially part of GFD.90}}).

           Job identifier I{should} follow the folling scheme::
              [backend url]-[native jobid]
        '''
        if self._plugin is not None:
            return self._plugin.job_get_job_id(self)
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")


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
            return self._plugin.job_cancel(self, timeout)
            return None
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

    def wait(self, timeout=-1):
        '''Wait for a running job to finish execution.
           @param timeout: Timeout in seconds.
        '''
        if self._plugin is not None:
            return self._plugin.job_wait(self, timeout)
            return None
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

