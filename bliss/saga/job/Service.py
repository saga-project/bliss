#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012 Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.resource import Compute
from bliss.saga.Object import Object 

import bliss.saga

class Service(Object):
    '''Loosely represents a SAGA job service as defined in GFD.90
    
    A job.Service represents anything which accepts job creation requests, and
    which manages thus created L{job.Job}s.  That can be a local shell, a remote
    ssh shell, a cluster queuing system, a IaaS backend -- you name it.

    The job.Service is identified by an URL, which usually points to the contact
    endpoint for that service.

    Example::


        my_job_id = "[fork://localhost]-[12345]"
        js  = saga.job.Service("fork://localhost")
        ids = js.list()

        if my_job_id in ids :
          print "found my job again, wohhooo!"

          j = js.get_job(my_job_id)

          if   j.get_state() == saga.job.Job.Pending  : print "pending"
          elif j.get_state() == saga.job.Job.Running  : print "running"
          else                                        : print "job is already final!"

    '''

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new job service object
           @param url: Url of the (remote) job manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.ObjectType.JobService, 
                            apitype=Object.ObjectType.JobAPI, session=session)

        if type(url) == str:
            self._url = Url(str(url))
        elif type(url) == Url:
            self._url = url
        elif type(url) == Compute:
            self._url = url._url
        else:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
             "A job.Service object must either be initialized with a URL or a resource.Compute object.")


        self._from_compute = False
        self._compute_obj = None

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_service_object(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

    ######################################################################
    ## 
    @classmethod
    def from_url(url, session=None):
        '''Initialize a new job service from (resource manager) URL.'''
        service = Service(url, session=session)
        service._from_compute = False
        return service


    ######################################################################
    ## 
    @classmethod
    def from_compute(self, compute_obj, session=None):
        '''Create a job service from a saga.resource.Compute object.'''
        
        service = Service(compute_obj, session=session)
        service._from_compute = True
        sservice._compute_obj = compute_obj
        return service        


    ######################################################################
    ## 
    def __del__(self):
        '''Delete the service in a civilised fashion.'''
        if self._plugin is not None:
            self._plugin.unregister_service_object(self)
        else:
            pass # can't throw here

    ######################################################################
    ##
    def create_job(self, job_description):
        '''Create a new job object.

           @param job_description: The description for the new job.
           @type  job_description: L{Description} 

           create_job() accepts a job description, which described the
           application instance to be created by the backend.  The create_job()
           method is not actually attempting to *run* the job, but merely parses
           the job description for syntactic and semantic consistency.  The job
           returned object is thus not in 'Pending' or 'Running', but rather in
           'New' state.  The actual submission is performed by calling run() on
           the job object.  

           Example::

             js = saga.job.Service("fork://localhost")
             jd = saga.job.Description ()
             jd.executable = '/bin/date'
             j  = js.create_job(jd)

             if   j.get_state() == saga.job.Job.New      : print "new"
             else                                        : print "oops!"

             j.run()

             if   j.get_state() == saga.job.Job.Pending  : print "pending"
             elif j.get_state() == saga.job.Job.Running  : print "running"
             else                                        : print "oops!"

        '''
        if type(job_description) != bliss.saga.job.Description:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_job() expects job.Description as parameter.")

        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            jd = bliss.saga.job.Description._deep_copy(job_description)
            return self._plugin.service_create_job(self, jd)

    ######################################################################
    ##
    def get_job(self, job_id):
        '''Return the job object for the given job id.
           @param job_id: The job id.

           Job objects are a local representation of a remote stateful entity.
           The job.Service supports to reconnect to those remote entities::


             js = saga.job.Service("fork://localhost")
             j  = js.get_job(my_job_id)

             if   j.get_state() == saga.job.Job.Pending  : print "pending"
             elif j.get_state() == saga.job.Job.Running  : print "running"
             else                                        : print "job is already final!"

        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.service_get_job(self, job_id)

    ######################################################################
    ##
    def list(self):
        '''List all jobs managed by this service instance.

           As the job.Service represents a job management backend, list() will
           return a list of job IDs for all jobs which are known to the backend,
           and which can potentially be accessed and managed by the application.


           Example::


             js  = saga.job.Service("fork://localhost")
             ids = js.list()

             if my_job_id in ids :
               print "found my job again, wohhooo!"

               j = js.get_job(my_job_id)

               if   j.get_state() == saga.job.Job.Pending  : print "pending"
               elif j.get_state() == saga.job.Job.Running  : print "running"
               else                                        : print "job is already final!"

        '''
        if self._plugin is not None:
            return self._plugin.service_list(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

