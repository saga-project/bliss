#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import logging

from bliss.plugins.pluginbase import _PluginBase
from bliss.plugins.pluginbase import _api_type_saga_job

from bliss.saga import exception
import bliss.saga.job


class _JobPluginBase(_PluginBase):
    '''Abstract base class for all job plugins'''
    
    def __init__(self, name, schemas):
        '''Class constructor'''
        _PluginBase.__init__(self, name=name, schemas=schemas)
    
    @classmethod
    def supported_api(self):
        '''Implements interface from _PluginBase'''
        return _api_type_saga_job

    def create_job(self, service_obj, job_description):     
        '''Implement interface from _JobPluginBase'''
        job = bliss.saga.job.Job()
        job._Job__init_from_service(service_obj=service_obj, job_desc=job_description)
        return job

    def register_service_object(self, service_obj):
        self.log_error("Not implemented plugin method called: register_service_object()")
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg) 

    def register_job_object(self, job_obj, service_obj):
        '''This method is called upon instantiation of a new job object'''
        self.log_error("Not implemented plugin method called: register_job_object()")
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg) 

    def unregister_service_object(self, service_obj):
        '''This method is called upon deletion of a new service object'''
        self.log_error("Not implemented plugin method called: unregister_service_object()")
        # don't throw -- destructor context

    def unregister_job_object(self, job_obj):
        '''This method is called upon deletion of a new job object'''
        self.log_error("Not implemented plugin method called: unregister_job_object()")
        # don't throw -- destructor context

    def get_job(self, job_id):
        errormsg = "Not implemented plugin method called: get_job()"
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg)

    def list(self):
        errormsg = "Not implemented plugin method called: list()"
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg) 

    def job_get_state(self, job_obj):
        errormsg = "Not implemented plugin method called: job.get_state()"
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg) 

    def job_get_job_id(self, job_obj):
        errormsg = "Not implemented plugin method called: job.get_job_id()"
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg) 

    def job_run(self, job_obj):
        errormsg = "Not implemented plugin method called: job.run()"
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg) 

    def job_wait(self, job_obj, timeout):
        errormsg = "Not implemented plugin method called: job.wait()"
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg)

    def job_cancel(self, job_obj, timeout):
        errormsg = "Not implemented plugin method called: job.cancel()"
        self.log_error_and_raise(exception.Error.NotImplemented, errormsg)  
