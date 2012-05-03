#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.Object import Object
from bliss.saga.Attributes import AttributeInterface

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
    """Loosely represents a SAGA task container as defined in GFD.90.
   
       The job.Container class allows to manage collections of L{job.Job}s
       efficiently.  It supports:
   
         - management of the job collection::
         

            jc = saga.job.Container()    # new container
   
            jc.add (job_1)               # add
            jc.add (job_2)               # some
            jc.add (job_3)               # jobs
   
            j = jc.get_job (id)          # retrieve job
   
            jc.remove (job_1)            # remove job
   
            print str(jc.size ())        # get number of jobs
            print str(jc.list ())        # get all job ids
            print str(jc.get_states ())  # get all job states

   
   
         - collective operations::
   

            jc.run ()                    # run all jobs in container
            jc.cancel ()                 # cancel all jobs in container

   
   
         - event driven programming::
   

            jc.wait (saga.job.Any)       # wait until any job in container finishes
            jc.wait (saga.job.All)       # wait until all job in container finish

    """
   
    ######################################################################
    ## 
    def __init__(self, service):
        '''Create a new job (a.k.a. 'task') container.

           @param service: Currently, a container needs to be bound to
                           a valid L{saga.job.Service} and can only hold 
                           jobs that are known to that service.  
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

           @param job: A L{job.Job} object.  The job can be in any state.

           Example:: 
             

              jc = saga.job.Container()
   
              jc.add (job_1)               # add existing job
              jc.add (js.create_job (jd))  # add new job from job service


        '''
        # FIXME: the job does not need to be in New state, as was documented
        # before

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

           @param job: The L{job.Job} object to remove.

           Example:: 
             

              jc.remove (job_1)            # remove existing job


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
    def get_job(self, job_id):
        '''Get a single job from the job container.

           @param job_id: The job id identifying the L{job.Job} to return.

           Example:: 
             

              jc.get_job ("[fork://]-[4452]")     # remove some local job


        '''
        # FIXME: this is the job id, not the object uid as documented before
        if self._plugin is not None:
            return self._plugin.container_get_job(self, job_id)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")


    ######################################################################
    ##
    def get_states(self):
        '''Get the state of all jobs in the container.

           Example:: 
             

              count = 0

              for state in jc.get_states () :
                if state == saga.job.Done :
                  count += 1
              
              print "%d jobs are done, so far" % count


        '''
        if self._plugin is not None:
            return self._plugin.container_get_states(self, job)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    
    ######################################################################
    ##
    def list(self):
        '''List all L{job.Job}s that are in the container.

           Example:: 
             

              for id in jc.list () :
                j = jc.get_job (id)
                print "job %s is in state %s" % id, j.get_state ()

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

           Example:: 
             

              print "managing %d jobs" % jc.size ()

        '''
        # FIXME: shouldn't that be rendered as len(jc) ?
        if self._plugin is not None:
            return self._plugin.container_size(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

    def __len__ (self) :
        '''Returns the number of jobs in the container. Same as Container.size().'''
        return self.size ()


    ######################################################################
    ##
    def run(self):
        '''Start all jobs in the container.

           The L{job.Job}.run() operation can only be successful for 'New' jobs -
           this L{run()<run>} method on the Container class will thus only succeed if
           all jobs in the container are in 'New' state   In that case,
           this call will invoke run() on all jobs in the container.

           Example:: 
             

              jc = saga.job.Container()
   
              jc.add (js.create_job (jd))    # add
              jc.add (js.create_job (jd))    # new
              jc.add (js.create_job (jd))    # jobs

              jc.run ()
              jc.wait (saga.job.All)

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

           The cancel() method on the job.Container class will invoke
           L{job.Job}.cancel() on all jobs in the container.

           The job.cancel() method will cancel all jobs in 'Running' and
           'Pending' state but will not alter the state of jobs which
           have already finished ('Done', 'Failed' or 'Canceled' state).

           Note that cancel() is not defined for jobs in 'New' state -- the
           application must thus ensure that no jobs in the container are 'New'.

           Example::


              jc = saga.job.Container()
   
              jc.add (js.create_job (jd))    # add
              jc.add (js.create_job (jd))    # new
              jc.add (js.create_job (jd))    # jobs

              jc.run ()
              jc.cancel ()

        '''
        # FIXME: we may want to get rid of timeout
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

           @param wait_mode: Wait for 'Any' or for 'All' jobs in the container.

           @param timeout: Timeout in seconds.

           @return: the call returns a job in a final state.  That job is then
           also removed from the container.  On 'All', it is not specified which
           job is returned.  On 'Any', the job which finished first is returned.
           On timeout, 'None' is returned.


           The wait() method on saga.job.Container will inspect all jobs in the
           container, and will return whenever job(s) enter a final state (Done,
           Failed, Canceled).

           The 'wait_mode' parameter determines when exactly the call will
           return: 

             - All: wait() returns when *all* jobs reached a final state
             - Any: wait() returns when *one* jobs reached a final state

           Example::


              jc = saga.job.Container()
   
              jc.add (js.create_job (jd))    # add
              jc.add (js.create_job (jd))    # new
              jc.add (js.create_job (jd))    # jobs

              jc.run ()
              
              while j = jc.wait () :
                print "job %s returned: %s" % j.get_id (), j.get_state ()

              # jc is empty at this point



            The wait() method can also be used for a non-blocking or timed wait,
            via the optional 'timeout' parameter.  That parameter is interpreted
            as:

              - timeout <  0 : blocking wait (default)
              - timeout == 0 : non-blocking wait, tests if any job is final
              - timeout >  0 : block for 'timeout' seconds, then return no matter what

           Example::


              jc = saga.job.Container()
   
              jc.add (js.create_job (jd))    # add
              jc.add (js.create_job (jd))    # new
              jc.add (js.create_job (jd))    # jobs

              jc.run ()
              
              try: 
                j = jc.wait (5.0)   # wait for 5 seconds

              except saga.exception.TimeOut :
                print "no job finished after 5 seconds"



              jc = saga.job.Container()
   
              jc.add (js.create_job (jd))    # add
              jc.add (js.create_job (jd))    # new
              jc.add (js.create_job (jd))    # jobs

              jc.run ()
              
              while jc.size () :
                os.sleep (1)
                print "waiting for jobs"

                try: 
                  j = jc.wait (5.0)   # wait for 5 seconds
                  print "job %s returned: %s" % j.get_id (), j.get_state ()
                except saga.exception.TimeOut :
                  # ignore timeout
                  pass

              # jc is empty at this point


        '''
        if self._plugin is not None:
            return self._plugin.container_wait(self, wait_mode, timeout)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

