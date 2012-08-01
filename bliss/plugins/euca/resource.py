# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ashley Zebrowski"
__copyright__ = "Copyright 2012, Ashley Zebrowski"
__license__   = "MIT"

import bliss.saga 
import collections

from bliss.interface import ResourcePluginInterface
#from bliss.plugins import utils
from bliss.plugins.euca.compute import EucaCompute

#object = manager
#process = compute
class ResourceBookKeeper:
    def __init__(self, parent):
        self.manager = {} #dict of resourcemanagers
        self.compute = {} #maybe replace with self.instance
        self.instance={} #keyed by compute object
        self.boto = {} #keyed by manager id
        self.parent = parent
        
    def add_manager_object(self, manager_obj):
        self.manager[hex(id(manager_obj))] = {'instance' : manager_obj, 'compute' : [], 'boto':None}

        self.boto[hex(id(manager_obj))] = EucaCompute(self.parent, manager_obj, manager_obj._url)

        #add all instances that may be running in the background
        reservations= self.boto[hex(id(manager_obj))].connection.get_all_instances()
        instances = [i for r in reservations for i in r.instances]

        for i in instances:
            compute_description=bliss.saga.resource.ComputeDescription()
            compute_resource = bliss.saga.resource.Compute()
            compute_resource._Compute__init_from_manager(manager_obj=manager_obj, 
                                                         compute_description=compute_description)
            compute_resource.vmid=i.id
            compute_resource.instance=i
            self.manager[hex(id(manager_obj))]["compute"].append(compute_resource)

                
    def add_compute_object(self, compute_obj, manager_obj):
        manager_id = hex(id(manager_obj))  
        compute_id = hex(id(compute_obj))
        try:

            #set up ssh key for the new instance
            c = self.boto[hex(id(manager_obj))].connection
            if not c.get_all_key_pairs("blisskey"):
                
                self.parent.log_info("Setting up bliss key")
                ssh_ctx = None
                x509_ctx = None
                for ctx in manager_obj.session.contexts:
                    if ctx.type is bliss.saga.Context.SSH:
                        ssh_ctx = ctx
                        self.parent.log_debug("Found SSH context to use!")
                        break
                    
                for ctx in manager_obj.session.contexts:
                    if ctx.type is bliss.saga.Context.X509:
                        x509_ctx = ctx
                        self.parent.log_debug("Found x509 context to use!")
                        break

                
            instance = self.boto[manager_id].create_instance()
            compute_obj.vmid=instance.id
            compute_obj.instance=instance
            self.manager[manager_id]['compute'].append(compute_obj)
            #self.compute[manager_id]['compute'].append(compute_obj)
            #self.manager[compute_id] = SSHJobProcess(jobdescription=job_obj.get_description(), plugin=self.parent, service_object=service_obj)
        except Exception, ex:
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                                            "Can't register job: %s" % (ex))   

    def get_compute_for_computeid(self, manager_obj, compute_id):
        '''Return the job object associated with the given job id'''
        for compute in self.list_compute_for_manager(manager_obj):
            if compute.vmid==compute_id:
                return compute

        self.parent_log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't find compute id!")

#            proc = self.get_process_for_job(job)
#            if proc.getpid(str(service_obj._url)) == job_id:  
#                return job
#            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, "Job ID not known by this plugin.")

    def list_compute_for_manager(self, manager_obj):
        '''List all compute objects that are registered with the given service'''
        manager_id = hex(id(manager_obj))  
        return self.manager[manager_id]['compute']

    def del_manager_obj(self, manager_obj):
        try:
            self.objects.remove((hex(id(manager_obj))))
        except Exception:
            pass

    def del_compute_obj(self, compute_obj):
        try:
            for s in self.manager:
                for c in self.manager[s]["compute"]:
                    if compute_obj==c:
                        print "HUZZAH, deleting compute object"
                        del self.manager[s]["compute"]
                        break
            #self.objects.remove((hex(id(manager_obj))))
        except Exception, ex:
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "Can't delete compute object: %s" % (ex))   
            pass
        compute_obj.instance.terminate()
    
#    def manager_get_compute(self, manager_obj, compute_id):    
#    def compute_resource_get_id(self, res_obj):
#    def compute_resource_get_manager(self, res_obj):
#    def manager_list_compute_resources(self, manager_obj):
#    def compute_resource_wait(self, res_obj, filter):
#    def compute_resource_get_state(self, res_obj,):

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
    Exceptions = ['saga.resource']

        ########################################
    ##
    class BookKeeper:
        '''Keeps track of job and service objects'''
        def __init__(self, parent):
            self.objects = {}
            self.processes = {}
            self.parent = parent
        
        def add_service_object(self, service_obj):
            self.objects[hex(id(service_obj))] = {'instance' : service_obj, 'jobs' : []}

        def del_service_obj(self, service_obj):
            try:
                self.objects.remove((hex(id(service_obj))))
            except Exception:
                pass

        def add_job_object(self, job_obj, service_obj):
            service_id = hex(id(service_obj))  
            job_id = hex(id(job_obj))
            try:
                self.objects[service_id]['jobs'].append(job_obj)
                self.processes[job_id] = SSHJobProcess(jobdescription=job_obj.get_description(), plugin=self.parent, service_object=service_obj)
            except Exception, ex:
                self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "Can't register job: %s" % (ex))   

        def del_job_object(self, job_obj):
            pass

        def get_service_for_job(self, job_obj):
            '''Return the service object the job is registered with'''
            for key in self.objects.keys():
                if job_obj in self.objects[key]['jobs']:
                    return self.objects[key]['instance']
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "INTERNAL ERROR: Job object %s is not known by this plugin" % (job)) 

        def get_job_for_jobid(self, service_obj, job_id):
            '''Return the job object associated with the given job id'''
            for job in self.list_jobs_for_service(service_obj):
                proc = self.get_process_for_job(job)
                if proc.getpid(str(service_obj._url)) == job_id:  
                    return job
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, "Job ID not known by this plugin.")


        def list_jobs_for_service(self, service_obj):
            '''List all jobs that are registered with the given service'''
            service_id = hex(id(service_obj))  
            return self.objects[service_id]['jobs']


        def get_process_for_job(self, job_obj):
            '''Return the local process object for a given job'''
            try: 
                return self.processes[hex(id(job_obj))]
            except Exception, ex:
                self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "INTERNAL ERROR: Job object %s is not associated with a process" % (job_obj))   
    ##
    ########################################

    def __init__(self, url):
        '''Class constructor'''
        ResourcePluginInterface.__init__(self, name=self._name, schemas=self._schemas)

        self.bookkeeper = ResourceBookKeeper(self)

    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        ## Step 3: Implement sanity_check. This method is called *once* on
        ##         Bliss startup. Here you should check if everything this 
        ##         adaptor needs is available, e.g., certain command line tools,
        ##         python modules and so on.
        ## 
        try: 
            import boto
        except ImportError, ie:
            self.log_error("Required Python module 'boto' missing: %s" % ie)
            return False
        return True

    def get_runtime_info(self): 
        '''Implements interface from _PluginBase'''
        #str = "Plugin: %s. Registered job.service objects: %s.\n%s".format(
        #       self.name, len(self.objects), repr(self.objects))
        #return str
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
       

    def register_manager_object(self, service_obj, url):
        '''Implements interface from _ResourcePluginBase'''
        #self.manager_dict[repr(service_obj) ] = {}
        self.bookkeeper.add_manager_object(service_obj)
        self.log_info("Registered new manager object %s" % (repr(service_obj)))
   

    def unregister_manager_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        self.bookkeeper.del_manager_obj(service_obj)
        self.log_info("Unregistered manager object %s" % (repr(service_obj)))

        #del self.manager_dict[repr(service_obj)]


    #self here is a EucaResourcePlugin
    def manager_create_compute(self, manager_obj, compute_description):
        '''Implements interface from _ResourcePluginBase.
           This method is called for saga.resource.manager.create_compute().
        '''
        try:
            compute_resource = bliss.saga.resource.Compute()
            compute_resource._Compute__init_from_manager(manager_obj=manager_obj, 
                                                         compute_description=compute_description)

            self.bookkeeper.add_compute_object(  compute_resource, manager_obj)
            #create a new boto instance compute_resource._boto with the
            # compute_resource._url

            #compute_resource._boto.create_instance()
            
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
#        self.log_info("IMPLEMENT ME! manager_list_compute_resources()")

        compute_list= self.bookkeeper.list_compute_for_manager(manager_obj)
        rl = [i.vmid for i in compute_list]
        return rl
        
            
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
        return self.bookkeeper.get_compute_for_computeid(manager_obj, compute_id)
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
    def compute_resource_get_state(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        res_obj.instance.update()
        state = res_obj.instance.state

        if state=="pending":
            return bliss.saga.resource.State.Pending
        if state=="running":
            return bliss.saga.resource.State.Active
        else:
            return bliss.saga.resource.State.Unknown
        return 
 #       self.log_info("IMPLEMENT ME! compute_resource_get_state()")
 #        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")
        

    def compute_resource_get_state_detail(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
        str=""
        i=res_obj.instance
        str+="Id: " + i.id + "\n"
        str+="Instance type: " + i.instance_type + "\n"
        str+="Kernel: " + i.kernel + "\n"
        str+="Ramdisk: " + i.ramdisk + "\n"
        str+="Architecture: " + "%s" % i.architecture + "\n"
        str+="Public IP: " + "%s" % (i.ip_address) + "\n"
        str+="Private IP: " + "%s" % (i.private_ip_address) + "\n"
        str+="Public DNS: " + "%s" % (i.public_dns_name) + "\n"
        str+="Private DNS: " + "%s" % (i.private_dns_name) + "\n"
        str+="Key_name: " + "%s" % i.key_name + "\n"
        str+="State: " + "%s" % i.state + "\n"
        str+="State Code: " + "%s" % (i.state_code) + "\n"
        str+="Launch time: " + "%s" % (i.launch_time) + "\n"
        return str
    
        self.log_info("IMPLEMENT ME! compute_resource_get_state_detail()")
        self.log_error_and_raise(bliss.saga.Error.NotImplemented, "Not implemented")

    #res_obj is a compute obj
    def compute_resource_get_description(self, res_obj):
        '''Implements interface from _ResourcePluginBase'''
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
        self.bookkeeper.del_compute_obj(res_obj)
        return
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

