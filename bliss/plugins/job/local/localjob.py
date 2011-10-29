#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.job.jobinterface  import _JobPluginBase
from bliss.plugins.job.local.process import LocalJobProcess

from bliss.saga import exception
import bliss.saga.job

class LocalJobPlugin(_JobPluginBase):
    '''Implements a job plugin that can submit jobs to the local machine'''

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
                self.processes[job_id] = LocalJobProcess(executable=job_obj.get_description().executable,
                                                         arguments=job_obj.get_description().arguments,
                                                         environment=job_obj.get_description().environment)
            except Exception, ex:
                self.parent.log_error_and_raise(exception.Error.NoSuccess, "Can't register job: {!r}".format(ex))   

        def del_job_object(self, job_obj):
            pass

        def get_service_for_job(self, job_obj):
            '''Return the service object the job is registered with'''
            for key in self.objects.keys():
                if job_obj in self.objects[key]['jobs']:
                    return self.objects[key]['instance']
            self.parrent.log_error_and_raise(exception.Error.NoSuccess, 
            "INTERNAL ERROR: Job object {!r} is not known by this plugin".format(job))   


        def get_process_for_job(self, job_obj):
            '''Return the local process object for a given job'''
            try: 
                return self.processes[hex(id(job_obj))]
            except Exception, ex:
                self.parrent.log_error_and_raise(exception.Error.NoSuccess, 
                "INTERNAL ERROR: Job object {!r} is not associated with a process".format(job_obj))   

    ##
    ########################################


    ## Step 1: Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.job.local'

    ## Step 2: Define supported url schemas
    ## 
    _schemas = ['fork']

    def __init__(self, url):
        '''Class constructor'''
        _JobPluginBase.__init__(self, name=self._name, schemas=self._schemas)
        self.bookkeeper = self.BookKeeper(self)

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
        #str = "Plugin: {!r}. Registered job.service objects: {!r}.\n{!r}".format(
        #       self.name, len(self.objects), repr(self.objects))
        #return str
       

    def register_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 4: Implement register_service_object. This method is called if 
        ##         a service object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        if service_obj.url.host != "localhost":
            self.log_error_and_raise(exception.Error.BadParameter, "Only 'localhost' can be used as hostname")        
      
        self.bookkeeper.add_service_object(service_obj)
        self.log_info("Registered new service object {!r}".format(repr(service_obj))) 
   

    def unregister_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        self.bookkeeper.del_service_object(service_obj)
        self.log_info("Unegistered new service object {!r}".format(repr(service_obj))) 

 
    def register_job_object(self, job_obj, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 6: Implement register_job_object. This method is called if 
        ##         a job object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        self.bookkeeper.add_job_object(job_obj, service_obj)        
        self.log_info("Registered new job object {!r}".format(repr(job_obj))) 

    def unregister_job_object(self, job_obj):
        '''Implements interface from _JobPluginBase'''
        self.bookkeeper.del_job_object(job_obj)
        self.log_info("Unegisteredjob object {!r}".format(repr(job_obj))) 

    def job_get_state(self, job):
        '''Implements interface from _JobPluginBase'''
        service = self.bookkeeper.get_service_for_job(job)

        try:
            return self.bookkeeper.get_process_for_job(job).getstate()  
        except Exception, ex:
            self.log_error_and_raise(exception.Error.NoSuccess, "Coudln't get job state because: {!s} ".format(str(ex)))


    def job_get_job_id(self, job):
        '''Implements interface from _JobPluginBase'''
        service = self.bookkeeper.get_service_for_job(job)
        try:
            pid = self.bookkeeper.get_process_for_job(job).getpid()  
            return "[{!s}]-[{!s}]".format(str(service.url), pid)
            self.log_info("Started local process: {!r} {!r}".format(job.get_description().executable, job.get_description().arguments)) 
        except Exception, ex:
            self.log_error_and_raise(exception.Error.NoSuccess, "Coudln't get job id because: {!s} ".format(str(ex)))


    def job_run(self, job):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.run()
        service = self.bookkeeper.get_service_for_job(job)
        if job.get_description().executable == "":   
            self.log_error_and_raise(exception.Error.BadParameter, "No executable defined in job description")
        try:
            self.bookkeeper.get_process_for_job(job).run()  
            self.log_info("Started local process: {!r} {!r}".format(job.get_description().executable, job.get_description().arguments)) 
        except Exception, ex:
            self.log_error_and_raise(exception.Error.NoSuccess, "Coudln't run job because: {!s} ".format(str(ex)))


    def job_cancel(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.cancel()
        try:
            self.bookkeeper.get_process_for_job(job).terminate()  
            self.log_info("Terminated local process: {!r} {!r}".format(job.get_description().executable, job.get_description().arguments)) 
        except Exception, ex:
            self.log_error_and_raise(exception.Error.NoSuccess, "Coudln't cancel job because: {!s} (already finished?)".format(str(ex)))

 
    def job_wait(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.wait()
        service = self.bookkeeper.get_service_for_job(job)
        try:
            self.bookkeeper.get_process_for_job(job).wait()   
        except Exception, ex:
            self.log_error_and_raise(exception.Error.NoSuccess, "Coudln't wait for the job because: {!s} ".format(str(ex)))

