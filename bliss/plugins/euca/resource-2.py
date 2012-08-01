# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ashley Zebrowski"
__copyright__ = "Copyright 2012, Ashley Zebrowski"
__license__   = "MIT"

import bliss.saga 
import collections

from bliss.interface import ResourcePluginInterface
from bliss.plugins import utils
from bliss.plugins.euca.compute import EucaCompute

class EucaResourcePlugin(ResourcePluginInterface):
    '''Implements a job plugin that can submit jobs to a bigjob server'''

    ## Step 1: Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.resource.euca'

    ## Step 2: Define supported url schemas
    ## 
    _schemas = ['euca']

    ## Step 3: Define apis supported by this adaptor
    ##
    _apis = ['saga.resource']

    def __init__(self, url):
        '''Class constructor'''
        ResourcePluginInterface.__init__(self, name=self._name, schemas=self._schemas)

        #manager_dict[manager_object] = {} #list of EucaCompute items
        self.compute_dict = {}      

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
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
       

    def register_manager_object(self, service_obj, url):
        '''Implements interface from _ResourcePluginBase'''
        self.manager_dict[repr(service_obj) ] = {}
        self.log_info("Registered new manager object %s" % (repr(service_obj)))
   

    def unregister_manager_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        self.log_info("Unregistered manager object %s" % (repr(service_obj)))
        del self.manager_dict[repr(service_obj)]


    #self here is a EucaResourcePlugin
    def manager_create_compute(self, manager_obj, compute_description):
        '''Implements interface from _ResourcePluginBase.
           This method is called for saga.resource.manager.create_compute().
        '''
        try:
            compute_resource = bliss.saga.resource.Compute()
            compute_resource._Compute__init_from_manager(manager_obj=manager_obj, 
                                                         compute_description=compute_description)

            #create a new boto instance compute_resource._boto with the
            # compute_resource._url
            compute_resource._boto = EucaCompute(computedescription=compute_description,
                                                 plugin=self,
                                                 service_object=manager_obj)

            compute_resource._boto.create_instance()
            
            
            return compute_resource
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create a new compute resource: %s " % (str(ex)))


    def manager_create_storage(self, manager_obj, storage_description):
        '''Implements interface from _ResourcePluginBase.
           This method is called for saga.resource.manager.create_compute().
        '''
        try:
            storage_resource = bliss.saga.resource.Storage()
            storage_resource._Storage__init_from_manager(manager_obj=manager_obj, 
                                                         storage_description=storage_description)
            return storage_resource
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create a new storage resource: %s " % (str(ex)))


    def manager_list_compute_resources(self, manager_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_list_compute_resources()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def manager_list_storage_resources(self, manager_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_list_storage_resources()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
            
    def manager_list_compute_templates(self, manager_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_list_compute_templates()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def manager_list_storage_templates(self, manager_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
        
    def manager_get_template_details(self, manager_obj, template_id):
        '''Implements interface from _ResourcePluginBase'''
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def manager_get_compute(self, manager_obj, compute_id):
        '''Implements interface from _ResourcePluginBase'''
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def manager_get_storage(self, manager_obj, storage_id):
        '''Implements interface from _ResourcePluginBase'''
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
        
    def manager_destroy_compute(self, manager_obj, compute_id, drain):
        '''Implements interface from _ResourcePluginBase'''
        compute_resource._boto.terminate()
        
        #self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def manager_destroy_storage(self, manager_obj, storage_id, drain):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! manager_destroy_storage()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def compute_resource_wait(self, res_obj, filter):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! compute_resource_wait()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    #res obj is the compute object we want to work with!
    def compute_resource_get_state(self, res_obj,):
        '''Implements interface from _ResourcePluginBase'''
        return res_obj._boto.get_state()
 #       self.log_info("IMPLEMENT ME! compute_resource_get_state()")
 #        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
        

    def compute_resource_get_state_detail(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! compute_resource_get_state_detail()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    #res_obj is a compute obj
    def compute_resource_get_description(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        print "*****************"
        #print res_obj
        return res_obj._boto.get_description()

    def compute_resource_get_id(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! compute_resource_get_id()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def compute_resource_get_manager(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! compute_resource_get_manager()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
 
    def compute_resource_destroy(self, res_obj, drain):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! compute_resource_destroy()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    def storage_resource_wait(self, res_obj, filter):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_wait()")

    def storage_resource_get_state(self, res_obj,):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_get_state()")  

    def storage_resource_get_state_detail(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_get_state_detail()")  

    def storage_resource_get_description(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_get_description()")  

    def storage_resource_get_id(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_get_id()")  

    def storage_resource_get_manager(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_get_manager()")   

    def storage_resource_get_filesystem(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_get_filesystem()")   

    def storage_resource_destroy(self, res_obj, drain):
        '''Implements interface from _ResourcePluginBase'''
        self.log_info("IMPLEMENT ME! storage_resource_destroy()")   

