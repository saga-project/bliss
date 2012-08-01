# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ashley Zebrowski"
__copyright__ = "Copyright 2012, Ashley Zebrowski"
__license__   = "MIT"

import bliss.saga

from bliss.plugins import utils
from bliss.interface import ResourcePluginInterface
from bliss.interface import JobPluginInterface
from bliss.plugins.euca.compute import EucaCompute

class EucaResourcePlugin(ResourcePluginInterface):
    _name = 'saga.plugin.resource.euca'
    _schemas = ['euca']
    _apis = ['saga.resource']

    def __init__(self, url):
        '''Class constructor'''
        ResourcePluginInterface.__init__(self, name=self._name, schemas=self._schemas)
        self.bookkeeper = self.BookKeeper(self)
    
    ########################################
    ##
    class BookKeeper:
        '''Keeps track of job and service objects'''
        def __init__(self, parent):
            self.objects = {}
            self.processes = {}
            self.parent = parent
        
        def add_service_object(self, service_obj):
            self.objects[hex(id(service_obj))] = {'instance' : service_obj, 'jobs' : [], 'compute' : []}

        def del_service_obj(self, service_obj):
            try:
                self.objects.remove((hex(id(service_obj))))
            except Exception:
                pass

##############################

        def add_compute_object(self, compute_obj, service_obj):
            service_id = hex(id(service_obj))  
            compute_id = hex(id(compute_obj))
            try:
                self.objects[service_id]['compute'].append(compute_obj)
                self.processes[compute_id] = EucaCompute(computedescription=None, plugin=self.parent, service_object=service_obj)
            except Exception, ex:
                self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                                                "Can't register compute: %s %s" % (ex, utils.get_traceback()))   

        def del_compute_object(self, compute_obj):
            pass

        def get_service_for_compute(self, compute_obj):
            '''Return the service object the compute object is registered with'''
            for key in self.objects.keys():
                if compute_obj in self.objects[key]['compute']:
                    return self.objects[key]['instance']
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "INTERNAL ERROR: Compute object %s is not known by this plugin %s" % (compute, utils.get_traceback())) 

        def get_compute_for_computeid(self, service_obj, compute_id):
            '''Return the compute object associated with the given compute id'''
            for compute in self.list_compute_for_service(service_obj):
            
                proc = self.get_process_for_compute(compute)
                if proc.getpid(str(service_obj._url)) == compute_id:

                    # NEED TO UPDATE COMPUTE PROCESS HERE
                    return compute
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, "Compute ID not known by this plugin.")


        def list_compute_for_service(self, service_obj):
            '''List all compute objects that are registered with the given service'''
            service_id = hex(id(service_obj))  
            return self.objects[service_id]['compute']


        def get_process_for_compute(self, compute_obj):
            '''Return the local process object for a given compute object'''
            try: 
                return self.processes[hex(id(compute_obj))]
            except Exception, ex:
                self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "INTERNAL ERROR: Compute object %s is not associated with a process %s" % (compute_obj, utils.get_traceback()))   

###################################################


    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        try:
            import boto
        except:
            print "Module boto missing -- plugin disabled.  (NEEDS BOTO)"
            return False

        return True

    def register_manager_object(self, service_obj, url):
        self.bookkeeper.add_service_object(service_obj)
        self.log_info("Registered new manager object %s" % (repr(service_obj))) 

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
    #    self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 



    ######## Implementation for saga.resource.Manager functionality 
    ##
    def manager_create_compute(self, manager_obj, compute_desc):
        try:
            self.log_info("Trying to create a compute resource")
            compute = bliss.saga.resource.Compute()
            compute._Compute__init_from_manager(manager_obj=manager_obj,
                                                         compute_description=compute_desc)
            self.bookkeeper.add_compute_object(compute, manager_obj)
        except:
            self.log_error_and_raise(bliss.saga.Error, "Some sort of error")

    def manager_create_storage(self, manager_obj, storage_desc):
        '''This method is called upon instantiation of a new storage resource object'''
        errormsg = "Not implemented plugin method called: manager_create_storage()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def manager_list_compute_resources(self, manager_obj):
        try:
            return self.bookkeeper.list_compute_for_service(manager_obj)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Error listing compute resources") 

    def manager_list_storage_resources(self, manager_obj):
        errormsg = "Not implemented plugin method called: manager_list_storage_resources()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def manager_list_compute_templates(self, manager_obj):
        errormsg = "Not implemented plugin method called: manager_list_compute_templates()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)

    def manager_list_storage_templates(self, manager_obj):
        errormsg = "Not implemented plugin method called: manager_list_storage_templates()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)

    def manager_get_template_details(self, manager_obj, t_id):
        errormsg = "Not implemented plugin method called: manager_get_template_detail()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)  

    def manager_get_compute(self, manager_obj, compute_id):
        try:
#            print manager_obj, compute_id
#            print self.bookkeeper.get_process_for_compute(compute_id)
            return self.bookkeeper.get_compute_for_computeid(manager_obj, compute_id)
        except:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't get compute") 

    def manager_get_storage(self, manager_obj, storage_id):
        errormsg = "Not implemented plugin method called: manager_get_storage()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def manager_destroy_compute(self, manager_obj, compute_id, drain):
        try:
            c = self.bookkeeper.get_process_for_compute(compute_id)
            c.terminate()
        except:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't destroy compute") 

    def manager_destroy_storage(self, manager_obj, storage_id, drain):
        errormsg = "Not implemented plugin method called: manager_destroy_compute()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg, drain) 


    ######## Method templates for saga.resource.Compute functionality 
    ##
    def compute_resource_get_state(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_state()"
        #self.bookkeeper.get_process_for_compute(res_obj)
        #res_obj is a Compute object
        try:
            p = self.bookkeeper.get_process_for_compute(res_obj)
            return p.getstate()
        except:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't get state") 

    def compute_resource_get_state_detail(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_state_detail()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def compute_resource_get_id(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_id()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)

    def compute_resource_get_manager(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_manager()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)  

    def compute_resource_get_description(self, res_obj):
        errormsg = "Not implemented plugin method called: compute_resource_get_description()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)  

    def compute_resource_destroy(self, res_obj, drain):
        errormsg = "Not implemented plugin method called: compute_resource_destroy()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def compute_resource_wait(self, res_obj, filter):
        errormsg = "Not implemented plugin method called: compute_resource_wait()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    ######## Method templates for saga.resource.Storage functionality 
    ##
    def storage_resource_get_state(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_state()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def storage_resource_get_state_detail(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_state_detail()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def storage_resource_get_id(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_id()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)

    def storage_resource_get_manager(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_manager()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)  

    def storage_resource_get_description(self, res_obj):
        errormsg = "Not implemented plugin method called: storage_resource_get_description()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg)  

    def storage_resource_destroy(self, res_obj, drain):
        errormsg = "Not implemented plugin method called: storage_resource_destroy()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

    def storage_resource_wait(self, res_obj, filter):
        errormsg = "Not implemented plugin method called: storage_resource_wait()"
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, errormsg) 

