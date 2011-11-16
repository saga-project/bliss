#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import PluginBaseInterface

from bliss.saga.exception import Error as SAGAError
from bliss.saga.exception import Exception as SAGAException

class JobPluginInterface(PluginBaseInterface):
    '''Abstract base class for all job plugins'''
    #PluginBaseInterface._supported_apis.append(PluginBaseInterface._api_type_saga_job)
 
    def __init__(self, name, schemas):
        '''Class constructor'''
        PluginBaseInterface.__init__(self, name=name, schemas=schemas,
                                     api=PluginBaseInterface._api_type_saga_job)
    
    def register_service_object(self, service_obj):
        errormsg = "Not implemented plugin method called: register_service_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def register_job_object(self, job_obj, service_obj):
        '''This method is called upon instantiation of a new job object'''
        errormsg = "Not implemented plugin method called: register_job_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def unregister_service_object(self, service_obj):
        '''This method is called upon deletion of a new service object'''
        self.log_error("Not implemented plugin method called: unregister_service_object()")
        # don't throw -- destructor context

    def unregister_job_object(self, job_obj):
        '''This method is called upon deletion of a new job object'''
        self.log_error("Not implemented plugin method called: unregister_job_object()")
        # don't throw -- destructor context


    ######## Implementation for saga.job.Service functionality 
    ##
    def service_list(self, service_obj):
        errormsg = "Not implemented plugin method called: service_list()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def service_get_job(self, service_obj, job_id):
        errormsg = "Not implemented plugin method called: service_get_job()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)


    ######## Implementation for saga.job.Container functionality 
    ##

    def container_object_register(self, container_obj):
        errormsg = "Not implemented plugin method called: container_object_register()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_object_unregister(self, container_obj):
        errormsg = "Not implemented plugin method called: container_object_unregister()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_add(self, container_obj, job_obj):
        errormsg = "Not implemented plugin method called: container_add()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_remove(self, container_obj, job_obj):
        errormsg = "Not implemented plugin method called: container_remove()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_list(self, container_obj):
        errormsg = "Not implemented plugin method called: container_list)"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_size(self, container_obj):
        errormsg = "Not implemented plugin method called: container_size)"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_run(self, container_obj):
        errormsg = "Not implemented plugin method called: container_run)"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_cancel(self, container_obj, timeout):
        errormsg = "Not implemented plugin method called: container_cancel)"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def container_wait(self, container_obj, wait_mode, timeout):
        errormsg = "Not implemented plugin method called: container_wait)"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 


    ######## Method templates for saga.Job functionality 
    ##
    def job_get_state(self, job_obj):
        errormsg = "Not implemented plugin method called: job_get_state()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def job_get_job_id(self, jobid):
        errormsg = "Not implemented plugin method called: job_get_job_id()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def job_run(self, job_obj):
        errormsg = "Not implemented plugin method called: job_run()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def job_wait(self, job_obj, timeout):
        errormsg = "Not implemented plugin method called: job_wait()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def job_cancel(self, job_obj, timeout):
        errormsg = "Not implemented plugin method called: job_cancel()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def job_get_exitcode(self, job_obj):
        errormsg = "Not implemented plugin attribute accessed: job_get_exitcode"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)   
