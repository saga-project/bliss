#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.job.jobinterface import _JobPluginBase
from bliss.saga import exception
import bliss.saga.job


class LocalJobPlugin(_JobPluginBase):
    '''Implments a job plugin that can submit jobs to the local machine'''

    ## Step 1: Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.job.local'

    ## Step 2: Define supported url schemas
    ## 
    _schemas = ['fork']

    def __init__(self, url):
        '''Class constructor'''
        _JobPluginBase.__init__(self, name=self._name, schemas=self._schemas)
        self.objects = {}
    
    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        ## Step 3: Implement sanity_check. This method is called *once* on
        ##         Bliss startup. Here you should check if everything this 
        ##         adaptor needs is available, e.g., certain command line tools.
        ##         
        return True

    def get_runtime_info(self): 
        '''Implements interface from _PluginBase'''
        str = "Plugin: {!r}. Registered job.service objects: {!r}.\n{!r}".format(
               self.name, len(self.objects), repr(self.objects))
        return str
       

    def register_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 4: Implement register_service_object. This method is called if 
        ##         a service object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        if service_obj.url.host != "localhost":
            self.log_error_and_raise(exception.Error.BadParameter, "Only 'localhost' can be used as hostname")        

        self.objects[hex(id(service_obj))] = {'instance' : service_obj, 'jobs' : []} 
        self.log_info("Registered new service object {!r}".format(repr(service_obj))) 
   

    def unregister_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        try:
            self.objects.remove((hex(id(service_obj))))
        except Exception:
            pass

 
    def register_job_object(self, job_obj, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 6: Implement register_job_object. This method is called if 
        ##         a job object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        service_id = hex(id(service_obj))  
 
        try:
            self.objects[service_id]['jobs'].append(job_obj)
            self.log_info("Registered new job object {!r}".format(repr(job_obj))) 
        except Exception, ex:
            self.log_error_and_raise(exception.Error.NoSuccess, "Can't register job: {!r}".format(ex))        



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
 
