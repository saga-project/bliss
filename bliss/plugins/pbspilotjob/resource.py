#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga 

from bliss.interface import ResourcePluginInterface
from bliss.plugins import utils

class PBSPilotJobResourcePlugin(ResourcePluginInterface):
    '''Implements a job plugin that can submit jobs to a bigjob server'''

    ## Step 1: Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.resource.pbspilotjob'

    ## Step 2: Define supported url schemas
    ## 
    _schemas = ['pbs+ssh']

    ## Step 3: Define apis supported by this adaptor
    ##
    _apis = ['saga.resource']

    def __init__(self, url):
        '''Class constructor'''
        ResourcePluginInterface.__init__(self, name=self._name, schemas=self._schemas)

    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        ## Step 3: Implement sanity_check. This method is called *once* on
        ##         Bliss startup. Here you should check if everything this 
        ##         adaptor needs is available, e.g., certain command line tools,
        ##         python modules and so on.
        ##         
        return True

    def get_runtime_info(self): 
        '''Implements interface from _PluginBase'''
        #str = "Plugin: %s. Registered job.service objects: %s.\n%s".format(
        #       self.name, len(self.objects), repr(self.objects))
        #return str
       

    def register_manager_object(self, service_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("Registered new manager object %s" % (repr(service_obj))) 
   

    def unregister_manager_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        self.log_info("Unegistered manager object %s" % (repr(service_obj))) 



    def manager_create_compute(self, manager_obj, compute_description):
        '''Implements interface from _ResourcePluginBase.
           This method is called for saga.resource.manager.create_compute().
        '''
        try:
            compute_resource = bliss.saga.resource.Compute()
            compute_resource._Compute__init_from_manager(manager_obj=manager_obj, 
                                                         compute_description=compute_description)
            return compute_resource
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create a new compute resource: %s " % (str(ex)))


    def manager_list_resources(self, manager_obj, filter):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_list_resources()") 

    def manager_list_templates(self, manager_obj, filter):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_list_templates()") 

    def manager_get_template_details(self, manager_obj, template_id):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_get_templates_details()") 

    def manager_get_compute(self, manager_obj, compute_id):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_get_compute()") 

    def manager_get_storage(self, manager_obj, storage_id):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_get_storage()") 

    def manager_destroy_compute(self, manager_obj, compute_id, drain):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_destroy_compute()") 

    def resource_wait(self, res_obj, filter):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! resource_wait()")

    def resource_get_state(self, res_obj,):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! resource_get_state()")  

    def resource_get_state_detail(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! resource_get_state_detail()")  

    def resource_get_description(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! resource_get_description()")  

    def resource_get_id(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! resource_get_id()")  

    def resource_get_manager(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! resource_get_manager()")   
 

