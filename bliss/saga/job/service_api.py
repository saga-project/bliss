#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012 Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.object_api import Object 

class Service(Object):
    '''Loosely represents a SAGA job service as defined in GFD.90'''

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new job service object
           @param url: Url of the (remote) job manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.Type.JobService, 
                            apitype=Object.Type.JobAPI, session=session)

        if(type(url) == str):
            self._url = Url(str(url))
        else:
            self._url = url

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
        #if compute_obj.get_type() != Object.Type.ResourceCompute:
        #    raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
        #          "Service.fromcompute() expects %s object as parameter" 
        #          % (Object.Type.ResourceComputeDescription))
        
        
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
             -------------------------------------------------------------------
             js = saga.job.Service ("sge://localhost")
             j  = js.create_job    (jd)

             if      j.state == saga.job.New      : print "new"
             else                                 : print "oops!"

             j.run ()

             if      j.state == saga.job.Pending  : print "pending"
             else if j.state == saga.job.Running  : print "running"
             else                                 : print "oops!"
             -------------------------------------------------------------------
        '''
        if job_description.get_type() != Object.Type.JobDescription:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_job() expects %s object as parameter" 
                  % (Object.Type.JobDescription))

        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.service_create_job(self, job_description)

    ######################################################################
    ##
    def get_job(self, job_id):
        '''Return the job object for the given job id.
           @param job_id: The job id.

           Job objects are a local representation of a remote stateful entity.
           The job.Service supports to reconnect to those remote entities::

             -------------------------------------------------------------------
             js = saga.job.Service ("sge://localhost")
             j  = js.get_job       (my_job_id)

             if      j.state == saga.job.Pending  : print "pending"
             else if j.state == saga.job.Running  : print "running"
             else                                 : print "job is already final!"
             -------------------------------------------------------------------
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

             -------------------------------------------------------------------
             js  = saga.job.Service ("sge://localhost")
             ids = js.list ()

             if my_job_id in ids :
               print "found my job again, wohhooo!"

               j = js.get_job (my_job_id)

               if      j.state == saga.job.Pending  : print "pending"
               else if j.state == saga.job.Running  : print "running"
               else                                 : print "job is already final!"
             -------------------------------------------------------------------
        '''
        if self._plugin is not None:
            return self._plugin.service_list(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

