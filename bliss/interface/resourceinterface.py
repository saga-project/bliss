# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import PluginBaseInterface

from bliss.saga.Error import Error as SAGAError
from bliss.saga.Exception import Exception as SAGAException

class ResourcePluginInterface(PluginBaseInterface):
    '''Abstract base class for all resource plugins'''
 
    def __init__(self, name, schemas):
        '''Class constructor'''
        PluginBaseInterface.__init__(self, name=name, schemas=schemas,
                                     api=PluginBaseInterface.Exception_type_saga_resource)
    
    def register_manager_object(self, service_obj, url):
        errormsg = "Not implemented plugin method called: register_manager_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 


    def unregister_manager_object(self, manager_obj, url):
        '''This method is called upon deletion of a manager object'''
        self.log_error("Not implemented plugin method called: unregister_manager_object()")
        # don't throw -- destructor context

    #def unregister_compute_object(self, compute_obj):
    #    '''This method is called upon deletion of a compute object'''
    #    self.log_error("Not implemented plugin method called: unregister_compute_object()")
    #    # don't throw -- destructor context

    #def unregister_storage_object(self, compute_obj, manager_obj):
    #    '''This method is called upon instantiation of a new compute resource object'''
    #    errormsg = "Not implemented plugin method called: unregister_storage_object()"
    #    self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 



    ######## Implementation for saga.resource.Manager functionality 
    ##
    def manager_create_compute(self, manager_obj, compute_desc):
        '''This method is called upon instantiation of a new compute resource object'''
        errormsg = "Not implemented plugin method called: manager_create_compute()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_create_storage(self, manager_obj, storage_desc):
        '''This method is called upon instantiation of a new storage resource object'''
        errormsg = "Not implemented plugin method called: manager_create_storage()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_list_compute_resources(self, manager_obj):
        errormsg = "Not implemented plugin method called: manager_list_compute_resources()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_list_storage_resources(self, manager_obj):
        errormsg = "Not implemented plugin method called: manager_list_storage_resources()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_list_compute_templates(self, manager_obj):
        errormsg = "Not implemented plugin method called: manager_list_compute_templates()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def manager_list_storage_templates(self, manager_obj):
        errormsg = "Not implemented plugin method called: manager_list_storage_templates()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def manager_get_template_details(self, manager_obj, t_id):
        errormsg = "Not implemented plugin method called: manager_get_template_detail()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)  

    def manager_get_compute(self, manager_obj, compute_id):
        errormsg = "Not implemented plugin method called: manager_get_compute()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_get_storage(self, manager_obj, storage_id):
        errormsg = "Not implemented plugin method called: manager_get_storage()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_destroy_compute(self, manager_obj, compute_id, drain):
        errormsg = "Not implemented plugin method called: manager_destroy_compute()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def manager_destroy_storage(self, manager_obj, storage_id, drain):
        errormsg = "Not implemented plugin method called: manager_destroy_compute()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg, drain) 


    ######## Method templates for saga.resource.Compute functionality 
    ##
    def compute_resource_get_state(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_state()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def compute_resource_get_state_detail(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_state_detail()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def compute_resource_get_id(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_id()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def compute_resource_get_manager(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_manager()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)  

    def compute_resource_get_description(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_description()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)  

    def compute_resource_destroy(self, res_obj, drain):
        errormsg = "Not implemented plugin method called: compute_resource_destroy()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def compute_resource_wait(self, res_obj, filter):
        errormsg = "Not implemented plugin method called: compute_resource_wait()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    ######## Method templates for saga.resource.Storage functionality 
    ##
    def storage_resource_get_state(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_state()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def storage_resource_get_state_detail(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_state_detail()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def storage_resource_get_id(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_id()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def storage_resource_get_manager(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_manager()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)  

    def storage_resource_get_description(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_description()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)  

    def storage_resource_destroy(self, res_obj, drain):
        errormsg = "Not implemented plugin method called: storage_resource_destroy()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def storage_resource_wait(self, res_obj, filter):
        errormsg = "Not implemented plugin method called: storage_resource_wait()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

