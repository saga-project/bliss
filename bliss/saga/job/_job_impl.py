#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga._object_impl import Object
from bliss.saga._attributes_impl import AttributeInterface

class JobID(object):
    '''Represents a SAGA job ID (Not part of GFD.90)'''
    
    ######################################################################
    ##
    def __init__(self, service_url, native_id):
        '''Create a new job id.
           @param service_url : The URL of the job service of the job.
           @param native_id: The native id (a.k.a. backend id) of the job.
        '''
        self._service = service_url
        self._native = native_id

    ######################################################################
    ##
    def __str__(self):
        '''String representation.'''
        return "[%s]-[%s]" % (self._service, self._native)

    ######################################################################
    ##
    def service_url():
        doc = "The job id's service url component"
        def fget(self):
            return self._service
        return locals()
    service_url = property(**service_url())

    ######################################################################
    ##
    def native_id():
        doc = "The job id's native id component"
        def fget(self):
            return self._native
        return locals()
    native_id = property(**native_id())


class Job(Object, AttributeInterface):
    '''Loosely represents a SAGA job as defined in GFD.90'''
    
    Canceled = "saga.job.Job.Canceled"
    '''Indicates that the job has been canceled either by the user or the system'''
    Done     = "saga.job.Job.Done"
    '''Indicates that the job has successfully executed''' 
    Failed   = "saga.job.Job.Failed"
    '''Indicates that the execution of the job has failed'''
    New      = "saga.job.Job.New"
    '''Indicates that the job hasn't been started yet'''
    Running  = "saga.job.Job.Running"
    '''Indicates that the job is executing'''
    Waiting  = "saga.job.Job.Waiting"
    '''Indicates that the job is waiting to be executed (NOT IN GFD.90)'''
    Unknown  = "saga.job.Job.Unknown"
    '''Indicates that the job is in an unexpected state'''

    ######################################################################
    ##
    def __init__(self):
        '''PRIVATE Constructor (don't call explicitly!)'''
        Object.__init__(self, Object.Job, apitype=Object.JobAPI)
        AttributeInterface.__init__(self)
      
        # register properties with the attribute interface 
        self._register_ro_attribute     (name="Exitcode", 
                                         accessor=self.__class__.exitcode) 
        self._register_ro_attribute     (name="JobID", 
                                         accessor=self.__class__.jobid)  
        self._register_ro_attribute     (name="ServiceURL", 
                                         accessor=self.__class__.serviceurl)  

    ######################################################################
    ##
    def __init_from_service(self, service_obj, job_desc):
        '''Constructor'''
        self._service = service_obj
        self._url = service_obj._url
        self._job_description = job_desc

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

    ######################################################################
    ##
    def __del__(self):
        '''Delete the job in a civilised fashion.'''
        if self._plugin is not None:
            self._plugin.unregister_job_object(self)
        else:
            pass # can't throw here

    ######################################################################
    ##
    def get_stderr(self):
        '''B{Not Implemented:} Bliss finds this method unnecessary and \
           generally poorly supported by distributed middelware - use \
           U{Air<http://oweidner.github.com/air/>} instead for scalable 
           output streaming and much more.
        '''
        raise bliss.saga.Exception(bliss.saga.Error.NotImplemented, 
          "Bliss doesn't suppport get_stderr()")

    ######################################################################
    ##
    def get_stdout(self):
        '''B{Not Implemented:} Bliss finds this method unnecessary and \
           generally poorly supported by distributed middelware - use \
           U{Air<http://oweidner.github.com/air/>} instead for scalable 
           output 
        '''
        raise bliss.saga.Exception(bliss.saga.Error.NotImplemented, 
          "Bliss doesn't suppport get_stdout()")

    ######################################################################
    ##
    def get_description(self):
        '''Return the job description this job was created from.'''
        if self._plugin is not None:
            return self._job_description
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def get_state(self):
        '''Return the current state of the job.'''
        if self._plugin is not None:
            return self._plugin.job_get_state(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def get_job_id(self):
        '''Return the identifier for the job (B{I{not officially part of GFD.90}}).
        '''
        if self._plugin is not None:
            return self._plugin.job_get_job_id(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def run(self):
        '''Execute the job via the associated job service.'''
        if self._plugin is not None:
            return self._plugin.job_run(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def cancel(self, timeout=0):
        '''Cancel the execution of the job.
           @param timeout: Timeout in seconds.
        '''
        if self._plugin is not None:
            return self._plugin.job_cancel(self, timeout)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def wait(self, timeout=-1):
        '''Wait for a running job to finish execution.
           @param timeout: Timeout in seconds.
        '''
        if self._plugin is not None:
            return self._plugin.job_wait(self, timeout)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ## Property:
    def exitcode():
        doc = "The job's exitcode."
        def fget(self):
            if self._plugin is not None:
                return self._plugin.job_get_exitcode(self)
        return locals()
    exitcode = property(**exitcode())

    ######################################################################
    ## Property:
    def jobid():
        doc = "The job's identifier."
        def fget(self):
            if self._plugin is not None:
                return self._plugin.job_get_job_id(self)
        return locals()
    jobid = property(**jobid())

    ######################################################################
    ## Property: 
    def serviceurl():
        doc = "The URL of the L{Service} instance managing this job."
        def fget(self):
            if self._plugin is not None:
                return str(self._url)
        return locals()
    serviceurl = property(**serviceurl())

