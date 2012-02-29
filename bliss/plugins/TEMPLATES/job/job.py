#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga 
from bliss.plugins import utils
from bliss.interface import JobPluginInterface

class NullJobPlugin(JobPluginInterface):
    '''Implements a 'null' plugin that does absolutely nothing
       but print things to the console'''

    ## Step 1: Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.job.null'

    ## Step 2: Define supported url schemas
    ## 
    _schemas = ['null']

    ## Step 3: Define apis supported by this adaptor
    ##
    _apis = ['saga.job']

    def __init__(self, url):
        '''Class constructor'''
        JobPluginInterface.__init__(self, name=self._name, schemas=self._schemas)


    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        ## Step 4: Implement sanity_check. This method is called *once* on
        ##         Bliss startup. Here you should check if everything this 
        ##         adaptor needs is available, e.g., certain command line tools,
        ##         python modules and so on.
        ##         
        try: 
            import subprocess
            return True
        except Exception, ex:
            return False 


    def get_runtime_info(self): 
        '''Implements interface from _PluginBase'''
        ## Optional: Can be used for plug-in introspection during runtime.
        ## Return whatever you think is appropriate / releavent for the user. 
        return 'Hi there. I am the Null Plugin and I have nothing to say!' 


    def register_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement register_service_object. This method is called if 
        ##         a service object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        
        ## This plug-in only accepts 'localhost' URLs
        if service_obj._url.host != "localhost":
            self.log_error_and_raise(bliss.saga.Error.BadParameter, "Only 'localhost' can be used as hostname")        
        self.log_info("Registered new service object %s" % (repr(service_obj))) 

        ## YOU HAVE TO TAKE TRACK OF KNOWN OBJECTS YOURSELF, E.G., BY USING A 
        ## DICTIONARY. HAVE A LOOK AT THE 'LOCAL' ADAPTOR FOR A PRACTICAL EXAMPLE


    def unregister_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 6: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        self.log_info("Unegistered service object %s" % (repr(service_obj))) 

 
    def unregister_job_object(self, job_obj):
        ## Step 7: Implement unregister_job_object. This method is called if
        ##         a job object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        '''Implements interface from _JobPluginBase'''
        self.log_info("Unegisteredjob object %s" % (repr(job_obj))) 


    def service_create_job(self, service_obj, job_description):
        '''Implements interface from _JobPluginBase.
           This method is called for saga.Service.create_job().
        '''
        if job_description.executable is None:   
            self.log_error_and_raise(bliss.saga.Error.BadParameter, 
              "No executable defined in job description")
        try:
            ## Create a new job object
            job = bliss.saga.job.Job()
            job._Job__init_from_service(service_obj=service_obj, 
                                        job_desc=job_description)

            ## YOU HAVE TO TAKE TRACK OF KNOWN OBJECTS YOURSELF, E.G., BY USING A 
            ## DICTIONARY. HAVE A LOOK AT THE 'LOCAL' ADAPTOR FOR A PRACTICAL EXAMPLE
            self.log_info("service.create_job() called")
            return job
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create a new job because: %s " % (str(ex)))


    def service_list(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        self.log_info("service.list() calle")
        return list()


    def service_get_job(self, service_obj, job_id):
        '''Implements interface from _JobPluginBase''' 
        self.log_info("service.get_job() called")
        return None


    def job_get_state(self, job):
        '''Implements interface from _JobPluginBase'''
        self.log_info("job.get_state() called")
        return bliss.saga.job.Job.Unknown


    def job_get_job_id(self, job):
        '''Implements interface from _JobPluginBase'''
        self.log_info("job.get_job_id() called")
        return "[0000]-[0000]"


    def job_run(self, job):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.run()
        if job.get_description().executable is None:   
            self.log_error_and_raise(bliss.saga.Error.BadParameter, "No executable defined in job description")
        self.log_info("job.run() called")


    def job_cancel(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.cancel()
        self.log_info("job.cancel() called")

 
    def job_wait(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.wait()
        self.log_info("job.wait() called")


    def job_get_exitcode(self, job_obj):
        '''Implements interface from _JobPluginBase'''
        self.log_info("job.get_exitcode() called")

