#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import PluginBaseInterface

from bliss.saga.exception_impl import Error as SAGAError
from bliss.saga.exception_impl import Exception as SAGAException

class ResourcePluginInterface(PluginBaseInterface):
    '''Abstract base class for all resource plugins'''
 
    def __init__(self, name, schemas):
        '''Class constructor'''
        PluginBaseInterface.__init__(self, name=name, schemas=schemas,
                                     api=PluginBaseInterface._api_type_saga_resource)
    
    def register_manager_object(self, service_obj):
        errormsg = "Not implemented plugin method called: register_manager_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def register_compute_object(self, compute_obj, manager_obj):
        '''This method is called upon instantiation of a new compute resource object'''
        errormsg = "Not implemented plugin method called: register_compute_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def unregister_manager_object(self, manager_obj):
        '''This method is called upon deletion of a manager object'''
        self.log_error("Not implemented plugin method called: unregister_manager_object()")
        # don't throw -- destructor context

    def unregister_compute_object(self, compute_obj):
        '''This method is called upon deletion of a compute object'''
        self.log_error("Not implemented plugin method called: unregister_compute_object()")
        # don't throw -- destructor context


    ######## Implementation for saga.job.Service functionality 
    ##
    def manager_list_ids(self, manager_obj):
        errormsg = "Not implemented plugin method called: service_list_ids()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_get_compute(self, manager_obj):
        errormsg = "Not implemented plugin method called: service_get_compute()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_release_compute(self, manager_obj):
        errormsg = "Not implemented plugin method called: service_release_compute()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 


    ######## Method templates for saga.Job functionality 
    ##
    def compute_get_state(self, job_obj):
        errormsg = "Not implemented plugin method called: compute_get_state()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 
