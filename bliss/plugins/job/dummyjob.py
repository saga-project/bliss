#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


from bliss.plugins.job.jobinterface import _JobPluginBase
#from bliss.saga import job
from bliss.saga import exception


class DummyJobPlugin(_JobPluginBase):
    '''Implments a job plugin that can't do anything.'''

    ## Step 1: Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.job.dummy'

    ## Step 2: Define supported url schemas
    ## 
    _schemas = ['dummy']

    def __init__(self, url):
        '''Class constructor'''
        _JobPluginBase.__init__(self, name=self._name, schemas=self._schemas)

        ## Lists to hold associated job and service objects
        self.service_objects = []
        self.job_objects = []
    
    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        ## Step 3: Implement sanity_check. This method is called *once* on
        ##         Bliss startup. Here you should check if everything this 
        ##         adaptor needs is available, e.g., certain command line tools.
        ##         
        return True

    def register_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 4: Implement register_service_object. This method is called if 
        ##         a service object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        if service_obj.url.host != "localhost":
            self.log_error_and_raise(exception.Error.BadParameter, "Only 'localhost' can be used as hostname")        

        self.service_objects.append(service_obj) 
        self.log_info("Registered new Service object {!r}".format(repr(service_obj))) 
   

    def unregister_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        try:
            self.service_objects.remove(service_obj) 
        except Exception:
            pass

 
    def register_job_object(self, job_obj, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 6: Implement register_job_object. This method is called if 
        ##         a job object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        self.job_objects.append(job_obj)
        self.log_info("Registered new Job object {!r}".format(repr(job_obj))) 


    def unregister_job_object(self, job_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 6: Implement unregister_job_object. This method is called if
        ##         a job object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        try:
            self.job_objects.remove(job_obj) 
        except Exception:
            pass

    def job_get_state(self, job_obj):
        #return job.Job.New
        return None


    def get_runtime_info(self): 
        '''Implements interface from _PluginBase'''        
        ## Step X: Implement get_runtime_info. This method can be called on any
        ##         SAGA Object and it returns a string containing arbitrary info
        ##         from the associated adaptor. You can be creative here ;-) 
        str = "Plugin: {!r}. Registered job.service objects: {!r}. Registered job.job objects: {!r}".format(
               self.name, len(self.service_objects), len(self.job_objects))
        return str
 
