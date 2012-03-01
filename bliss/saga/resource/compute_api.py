# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga                       import Url
from bliss.saga.job.service_api      import Service  as SService
from bliss.saga.resource.resource_api import Resource as SResource


class Compute(SResource):

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new compute resource.
        '''
        Object.__init__(self, Object.ResourceComputeResource, 
                        apitype=Object.ResourceAPI, session=session)


    ######################################################################
    ##
    #  FIXME: not sure if that should be overloaded or not...
    def __init_from_manager(self, manager_obj, compute_description):
        '''(Hidden) Constructor'''
        self._manager = manager_obj
        self._url     = manager_obj._url
        self._compute_description = compute_description

        self._plugin  = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))


    ######################################################################
    ##
    def submit(self, jsdl): 
        '''submit a job from JSDL description.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.submit (jsdl) 


    ######################################################################
    ##
    def get_jobs(self): 
        '''submit a job from JSDL description.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.get_jobs () 


    ######################################################################
    ##
    def get_job_service(self): 
        '''submit a job from JSDL description.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self.get_job_service () 

