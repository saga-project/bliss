#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga
from bliss.saga.Object     import Object
from bliss.saga.Attributes import AttributeInterface
from bliss.utils.jobid     import JobID

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
        Object.__init__(self)
        self._apitype = 'saga.job'
      
        # set attribute interface properties
        self.attributes_extensible_  (True)
        self.attributes_camelcasing_ (True)

        # register properties with the attribute interface 
        self.attributes_register_  ('State',      self.Unknown, self.Enum,   self.Scalar, self.ReadOnly)
        self.attributes_register_  ('Exitcode',   None,         self.Int,    self.Scalar, self.ReadOnly)
        self.attributes_register_  ('JobID',      None,         self.String, self.Scalar, self.ReadOnly)
        self.attributes_register_  ('ServiceURL', None,         self.Url,    self.Scalar, self.ReadOnly)

        self.attributes_register_deprecated_  ('jobid',       'JobID')
        self.attributes_register_deprecated_  ('serviceurl', 'ServiceURL')


        self.attributes_set_enums_  ('State',   [self.Unknown, self.New,
                                                 self.Pending, self.Running, 
                                                 self.Done,    self.Failed, 
                                                 self.Canceled])
        
        self.attributes_set_getter_ ('State',    self.get_state)
        self.attributes_set_getter_ ('jobID',    self.get_job_id)
        self.attributes_set_getter_ ('Exitcode', self.get_exitcode_)


    ######################################################################
    def get_exitcode_ (self) :
        return self._plugin.job_get_exitcode (self)

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


          js = saga.job.Service("fork://localhost")
          jd = saga.job.Description ()
          jd.executable = '/bin/date'

          j1 = js.create_job(jd)
          j1.run()

          j2 = js.create_job(j1.get_description())
          j2.run()


        '''
        if self._plugin is not None:
            jd = bliss.saga.job.Description._deep_copy(self._job_description)
            return jd
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ##
    def get_state(self):
        '''Return the current state of the job.
    
        B{Example}::
    
    
    
          js = saga.job.Service("fork://localhost")
          jd = saga.job.Description ()
          jd.executable = '/bin/date'
          j  = js.create_job(jd)
    
          if   j.get_state() == saga.job.Job.New : 
              print "new"
          else : 
              print "oops!"
    
          j.run()
    
          if   j.get_state() == saga.job.Job.Pending : 
              print "pending"
          elif j.get_state() == saga.job.Job.Running : 
              print "running"
          else :
              print "oops!"
    
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

            # This is a fix for https://github.com/saga-project/bliss/issues/38.
            # If we see a JobID object that looks like [service]-[None], we just 
            # return 'None'. That's much easier than messing with every single plug-in
            # This fix also deprecates JobID on API level and moves it into the util 
            # namespace where it can still be used within plug-in context.  

            jobid = self._plugin.job_get_job_id(self)
            if type(jobid) == bliss.utils.jobid.JobID:
                if jobid.native_id == None:
                    return None
                else:
                    return jobid
            else: 
                return jobid
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


          js = saga.job.Service("fork://localhost")
          jd = saga.job.Description ()
          jd.executable = '/bin/date'
          j  = js.create_job(jd)

          if j.get_state() == saga.job.Job.New : 
              print "new"
          else : 
              print "oops!"

          j.run()

          if   j.get_state() == saga.job.Job.Pending :
              print "pending"
          elif j.get_state() == saga.job.Job.Running :
              print "running"
          else :
              print "oops!"


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
        

          js = saga.job.Service("fork://localhost")
          jd = saga.job.Description ()
          jd.executable = '/bin/date'
          j  = js.create_job(jd)

          if   j.get_state() == saga.job.Job.New :
              print "new"
          else :
              print "oops!"

          j.run()

          if   j.get_state() == saga.job.Job.Pending  :
              print "pending"
          elif j.get_state() == saga.job.Job.Running :
              print "running"
          else :
              print "oops!"

          j.cancel()

          if   j.get_state() == saga.job.Job.Canceled :
              print "canceled"
          else :
              print "oops!"

        '''
        if self._plugin is not None:
            return self._plugin.job_cancel(self)
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


          js = saga.job.Service("fork://localhost")
          jd = saga.job.Description ()
          jd.executable = '/bin/date'
          j  = js.create_job(jd)

          if   j.get_state() == saga.job.Job.New :
              print "new"
          else :
              print "oops!"

          j.run()

          if   j.get_state() == saga.job.Job.Pending :
              print "pending"
          elif j.get_state() == saga.job.Job.Running :
              print "running"
          else :
              print "oops!"

          j.wait(-1.0)

          if   j.get_state() == saga.job.Job.Done :
              print "done"
          elif j.get_state() == saga.job.Job.Failed :
              print "failed"
          else :
              print "oops!"

        '''
        if self._plugin is not None:
            return self._plugin.job_wait(self, timeout)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    ######################################################################
    ## Property:
    ExitCode = property (doc = '''
    ExitCode:
    The job's exitcode.

    this attribute is only meaningful if the job is in 'Done' or 'Final'
    state - for all other job states, this attribute value is undefined.

    B{Example}::


      js = saga.job.Service("fork://localhost")
      jd = saga.job.Description ()
      jd.executable = '/bin/date'
      j  = js.create_job(jd)

      j.run()
      j.wait()

      if j.get_state() == saga.job.Job.Failed :
        if j.exitcode == "42" :
            print "Ah, galaxy bypass error!"
        else :
            print "oops!"

    ''')

    ######################################################################
    ## Property:
    JobID = property (doc = '''
    JobID:
    The job's identifier.

    This attribute is equivalent to the value returned by job.get_job_id()
    ''')


    ######################################################################
    ## Property: 
    ServiceURL = property (doc = '''
    ServiceURL:
    The URL of the L{Service} instance managing this job.

    This attribute is represents the URL under where the job management
    service can be contacted which owns the job.  The value is equivalent to
    the service part of the job_id.

    B{Example}::


      js = saga.job.Service("fork://localhost")
      jd = saga.job.Description ()
      jd.executable = '/bin/date'
      j  = js.create_job(jd)

      if j.serviceurl == "fork://localhost" :
          print "yes!"
      else :
          print "oops!"

    ''')
