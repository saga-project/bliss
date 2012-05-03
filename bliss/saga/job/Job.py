#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Object     import Object
from bliss.saga.Attributes import AttributeInterface

class JobID(object):
    '''Represents a SAGA job ID (Not part of GFD.90)
      
       The SAGA job ID is usually considered to be an opaque string, but in
       general is expected to be formatted as::

         '[backend-url]-[native-id]'

       (including brackets!), where 'backend-url' is the contact URL for the job
       manager who 'owns' the job, and 'native-id' is the job id as issued and
       understood by that job manager.

       Bliss exposes those components of the job ID in this class, which allows
       to create new IDs and to parse / split existing IDs.

       Example::


         js = saga.job.Service('ssh://remote.host.net')
         j = js.create_job(jd)
         id = j.get_job_id() 

         print "job id: %s"  %  id

         js_url = id.

    '''
    
    ######################################################################
    ##
    def __init__(self, service_url, native_id):
        '''Create a new job id.

           @param service_url : The URL of the job service of the job.
           @param native_id:    The native id (a.k.a. backend id) of the job.

           This function will mostly be useful for plugin developers, which
           frequently will have to create valid job IDs.
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
        doc = "The job ID's native id component"
        def fget(self):
            return self._native
        return locals()
    native_id = property(**native_id())


class Job(Object, AttributeInterface):
    '''Loosely represents a SAGA job as defined in GFD.90
    
    A 'Job' represents a running application instance, which may consist of one
    or more processes.  Jobs are created by submitting a Job description to
    a Job submission system -- usually a queuing system, or some other service
    which spawns jobs on the user's behalf.

    Jobs have a unique ID (see get_job_id()), and are stateful entities -- their
    'state' attribute changes according to a well defined state model:

    A job as returned by job.Service.create(jd) is in 'New' state -- it is not
    yet submitted to the job submission backend.  Once it was submitted, via
    run(), it will enter the 'Pending' state, where it waits to get actually
    executed by the backend (e.g. waiting in a queue etc).  Once the job is
    actually executed, it enters the 'Running' state -- only in that state is
    the job actually consuming resources (CPU, memory, ...).

    Jobs can leave the 'Running' state in three different ways: they finish
    successfully on their own ('Done'), they finish unsuccessfully on their own,
    or get canceled by the job management backend ('Failed'), or they get
    actively canceled by the user or the application ('Canceled').

    The methods defined on the Job object serve two purposes: inspecting the
    job's state, and initiating job state transitions.
    '''
    
    
    New      = "saga.job.Job.New"      
    '''Indicates that the job hasn't been started yet'''

    Pending  = "saga.job.Job.Pending"  
    '''Indicates that the job is waiting to be executed (NOT IN GFD.90)'''

    Running  = "saga.job.Job.Running"  
    '''Indicates that the job is executing

    Note that Bliss does not expose the 'Suspended' state -- Suspended jobs will
    be reported as 'Running'.
    '''

    Done     = "saga.job.Job.Done"     
    '''Indicates that the job has successfully executed''' 

    Failed   = "saga.job.Job.Failed"   
    '''Indicates that the execution of the job has failed'''

    Canceled = "saga.job.Job.Canceled" 
    '''Indicates that the job has been canceled either by the user or the system'''

    Unknown  = "saga.job.Job.Unknown"  
    '''Indicates that the job is in an unexpected state'''


    ######################################################################
    ##
    def __init__(self):
        '''PRIVATE Constructor (don't call explicitly!)'''
        Object.__init__(self, Object.Type.Job, apitype=Object.Type.JobAPI)
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
    #def get_stderr(self):
    #    '''B{Not Implemented:} Bliss does not support I/O streaming.  Please use
    #       file staging to retrieve stdout and stderr files.
    #    '''
    #    raise bliss.saga.Exception(bliss.saga.Error.NotImplemented, 
    #      "Bliss doesn't suppport get_stderr()")

    ######################################################################
    ##
    #def get_stdout(self):
    #    '''B{Not Implemented:} Bliss does not support I/O streaming.
    #    '''
    #    raise bliss.saga.Exception(bliss.saga.Error.NotImplemented, 
    #      "Bliss doesn't suppport get_stdout()")

    ######################################################################
    ##
    def get_description(self):
        '''Return the job description this job was created from.
        
        The returned description can be used to inspect job properties
        (executable name, arguments, etc.).  It can also be used to start
        identical job instances.

        The returned job description will in general reflect the actual state of
        the running job, and is not necessarily a simple copy of the job
        description which was used to create the job instance.  For example, the
        environment variables in the returned job description may reflect the
        actual environment of the running job instance.


        B{Example}::


          js = saga.job.Service("sge://localhost")

          j1 = js.create_job(jd)
          j1.run()

          j2 = js.create_job(j1.get_description())
          j2.run()


        '''
        if self._plugin is not None:
            return self._job_description
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def get_state(self):
        '''Return the current state of the job.

        B{Example}::



          js = saga.job.Service("sge://localhost")
          j  = js.create_job(jd)

          if j.get_state() == saga.job.New : print "new"
          else : print "oops!"

          j.run()

          if j.get_state() == saga.job.Pending : print "pending"
          else if j.get_state() == saga.job.Running : print "running"
          else : print "oops!"

        '''
        if self._plugin is not None:
            return self._plugin.job_get_state(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def get_job_id(self):
        '''Return the identifier for the job.'''
        if self._plugin is not None:
            return self._plugin.job_get_job_id(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def run(self):
        '''Execute the job via the associated job service.
        
        Request that the job is being executed by the backend.  If the backend
        is accepting this run request, the job will move to the 'Pending' or
        'Running' state -- otherwise this method will raise an error, and the
        job will be moved to 'Failed'.


        B{Example}::


          js = saga.job.Service("sge://localhost")
          j  = js.create_job(jd)

          if j.state == saga.job.New : print "new"
          else : print "oops!"

          j.run()

          if j.state == saga.job.Pending : print "pending"
          else if j.state == saga.job.Running : print "running"
          else : print "oops!"


        '''
        if self._plugin is not None:
            return self._plugin.job_run(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def cancel(self):
        '''Cancel the execution of the job.

           B{Example}::
           

             js = saga.job.Service("sge://localhost")
             j = js.create_job(jd)

             if j.state == saga.job.New : print "new"
             else : print "oops!"

             j.run()

             if j.state == saga.job.Pending  : print "pending"
             else if j.state == saga.job.Running : print "running"
             else : print "oops!"

             j.cancel()

             if j.state == saga.job.Canceled : print "canceled"
             else : print "oops!"

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

        The optional timeout parameter specifies the time to wait, and accepts
        the following values::

          timeout <  0  : wait forever (block)
          timeout == 0  : wait not at all (non-blocking test)
          timeout >  0  : wait for 'timeout' seconds

        On a non-negative timeout, the call can thus return even if the job is
        not in final state, and the application should check the actual job
        state.  The default timeout value is '-1.0' (blocking).

        B{Example}::


          js = saga.job.Service("sge://localhost")
          j = js.create_job(jd)

          if j.state == saga.job.New : print "new"
          else : print "oops!"

          j.run()

          if j.state == saga.job.Pending : print "pending"
          else if j.state == saga.job.Running : print "running"
          else : print "oops!"

          j.wait(-1.0)

          if j.state == saga.job.Done : print "done"
          if j.state == saga.job.Faile : print "failed"
          else : print "oops!"

        '''
        if self._plugin is not None:
            return self._plugin.job_wait(self, timeout)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ## Property:
    def exitcode():
        '''The job's exitcode.

        this attribute is only meaningful if the job is in 'Done' or 'Final'
        state - for all other job states, this attribute value is undefined.

        B{Example}::


          js = saga.job.Service("sge://localhost")
          j = js.create_job(jd)

          j.run()
          j.wait()

          if j.state == saga.job.Failed :
            if j.exitcode == "42" : print "Ah, galaxy bypass error!"
            else : print "oops!"

        '''

        def fget(self):
            if self._plugin is not None:
                return self._plugin.job_get_exitcode(self)
        return locals()
    exitcode = property(**exitcode())


    ######################################################################
    ## Property:
    def jobid():
        '''The job's identifier.

        This attribute is equivalent to the value returned by job.get_job_id()
        '''

        def fget(self):
            if self._plugin is not None:
                return self._plugin.job_get_job_id(self)
        return locals()
    jobid = property(**jobid())


    ######################################################################
    ## Property: 
    def serviceurl():
        '''The job's management URL.

        This attribute is represents the URL under where the job management
        service can be contacted which owns the job.  The value is equivalent to
        the service part of the job_id.

        B{Example}::


          js = saga.job.Service("sge://localhost")
          j = js.create_job(jd)

          if j.serviceurl == "sge://localhost" : print "yes!"
          else : print "oops!"

        '''
        doc = "The URL of the L{Service} instance managing this job."
        def fget(self):
            if self._plugin is not None:
                return str(self._url)
        return locals()
    serviceurl = property(**serviceurl())

