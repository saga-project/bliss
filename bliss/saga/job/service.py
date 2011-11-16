#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.object import Object 

class Service(Object):
    '''Loosely represents a SAGA job service as defined in GFD.90'''

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new job service object
           @param url: Url of the (remote) job manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.JobService, 
                            apitype=Object.JobAPI, session=session)

        if(type(url) == str):
            self._url = Url(str(url))
        else:
            self._url = url

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_service_object(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

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
        '''
        if job_description.get_type() != Object.JobDescription:
            raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                  "create_job() expects %s object as parameter" 
                  % (Object.JobDescription))

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
        '''
        if self._plugin is not None:
            return self._plugin.service_list(self)
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

