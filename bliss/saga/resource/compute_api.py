# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga                       import Url
from bliss.saga.job.service_api       import Service  as SService
from bliss.saga.resource.resource_api import Resource as SResource


class Compute(SResource):

    ######################################################################
    ## 
    def __init__(self):
        '''PRIVATE: Create a new compute resource.
        '''
        Object.__init__(self, Object.Type.ResourceComputeResource, 
                        apitype=Object.Type.ResourceAPI, session=session)


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
    #def submit(self, jsdl): 
    #    '''submit a job from JSDL description.'''
    #    if self._plugin is None:
    #        raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
    #          "Object not bound to a plugin")
#
#        return self._plugin.submit(jsdl) 


    ######################################################################
    ##
#    def get_jobs(self): 
#        '''get all managed jobs in a task container.'''
#        if self._plugin is None:
#            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
#              "Object not bound to a plugin")
#
#        return self._plugin.get_jobs () 


    ######################################################################
    ##
    # FIXME: Ole, in the spec, the compute resource IS-A job service, so
    # get_job_service() is not needed -- the instance can simply be casted into
    # a job service. I am not sure how that is rendered in Python -- I would
    # of course also simply inherit this resource type from job.service -- 
    # that seems much cleaner than re-implementing the whole job service
    # API/CPI...
    #
    def get_job_service(self): 
        '''expose this resource as legacy job service.'''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")

        return self._plugin.get_job_service () 

