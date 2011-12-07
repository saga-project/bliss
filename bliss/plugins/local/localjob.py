#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import JobPluginInterface
from bliss.plugins.local.process import LocalJobProcess

from bliss.plugins import utils
import bliss.saga 

class LocalJobPlugin(JobPluginInterface):
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
                self.processes[job_id] = LocalJobProcess(jobdescription=job_obj.get_description(), plugin=self.parent)
            except Exception, ex:
                self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "Can't register job: %s %s" % (ex, utils.get_traceback()))   

        def del_job_object(self, job_obj):
            pass

        def get_service_for_job(self, job_obj):
            '''Return the service object the job is registered with'''
            for key in self.objects.keys():
                if job_obj in self.objects[key]['jobs']:
                    return self.objects[key]['instance']
            self.parrent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "INTERNAL ERROR: Job object %s is not known by this plugin %s" % (job, utils.get_traceback())) 

        def get_job_for_jobid(self, service_obj, job_id):
            '''Return the job object associated with the given job id'''
            for job in self.list_jobs_for_service(service_obj):
                proc = self.get_process_for_job(job)
                if proc.getpid(str(service_obj._url)) == job_id:  
                    return job
            self.parrent.log_error_and_raise(bliss.saga.Error.NoSuccess, "Job ID not known by this plugin.")


        def list_jobs_for_service(self, service_obj):
            '''List all jobs that are registered with the given service'''
            service_id = hex(id(service_obj))  
            return self.objects[service_id]['jobs']


        def get_process_for_job(self, job_obj):
            '''Return the local process object for a given job'''
            try: 
                return self.processes[hex(id(job_obj))]
            except Exception, ex:
                self.parrent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "INTERNAL ERROR: Job object %s is not associated with a process %s" % (job_obj, utils.get_traceback()))   
    ##
    ########################################


    ## Step 1: Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.job.local'

    ## Step 2: Define supported url schemas
    ## 
    _schemas = ['fork']

    ## Step 3: Define apis supported by this adaptor
    ##
    _apis = ['saga.job']

    def __init__(self, url):
        '''Class constructor'''
        JobPluginInterface.__init__(self, name=self._name, schemas=self._schemas)
        self.bookkeeper = self.BookKeeper(self)

    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        ## Step 3: Implement sanity_check. This method is called *once* on
        ##         Bliss startup. Here you should check if everything this 
        ##         adaptor needs is available, e.g., certain command line tools,
        ##         python modules and so on.
        ##         
        try: 
            import subprocess
        except Exception, ex:
            print "module missing -- plugin disabled. (NEEDS LOGGING SUPPORT)"
            return False 
        return True

    def get_runtime_info(self): 
        '''Implements interface from _PluginBase'''
        #str = "Plugin: %s. Registered job.service objects: %s.\n%s".format(
        #       self.name, len(self.objects), repr(self.objects))
        #return str
       

    def register_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 4: Implement register_service_object. This method is called if 
        ##         a service object is instantiated with a url schema that matches 
        ##         this adaptor. You can still reject it by throwing an exception.
        if service_obj._url.host != "localhost":
            self.log_error_and_raise(bliss.saga.Error.BadParameter, "Only 'localhost' can be used as hostname")        
      
        self.bookkeeper.add_service_object(service_obj)
        self.log_info("Registered new service object %s" % (repr(service_obj))) 
   

    def unregister_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 5: Implement unregister_service_object. This method is called if
        ##         a service object associated with this plugin is deleted. You
        ##         shouldn't throw an exception here, since this method is called
        ##         by the destructor!
        self.bookkeeper.del_service_object(service_obj)
        self.log_info("Unegistered new service object %s" % (repr(service_obj))) 

 
    #def register_job_object(self, job_obj, service_obj):
    #    '''Implements interface from _JobPluginBase'''
    #    ## Step 6: Implement register_job_object. This method is called if 
    #    ##         a job object is instantiated via the service.create_job() call.
    #    ##         You can still reject it by throwing an exception.
    #    self.bookkeeper.add_job_object(job_obj, service_obj)   
    #    self.log_info("Registered new job object %s" % (repr(job_obj))) 

    def unregister_job_object(self, job_obj):
        '''Implements interface from _JobPluginBase'''
        self.bookkeeper.del_job_object(job_obj)
        self.log_info("Unegisteredjob object %s" % (repr(job_obj))) 


    def service_create_job(self, service_obj, job_description):
        '''Implements interface from _JobPluginBase.
           This method is called for saga.Service.create_job().
        '''
        if job_description.executable is None:   
            self.log_error_and_raise(bliss.saga.Error.BadParameter, 
              "No executable defined in job description")
        try:
            job = bliss.saga.job.Job()
            job._Job__init_from_service(service_obj=service_obj, 
                                        job_desc=job_description)
            #self.bookkeeper.add_job_object_to_service(job, service_obj,
            #    bliss.saga.job.JobID(service_obj._url, None))
            self.bookkeeper.add_job_object(job, service_obj)   

            return job
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create a new job because: %s " % (str(ex)))


    def service_list(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        ## Step 76: Implement service_list_jobs() 
        try:
            return self.bookkeeper.list_jobs_for_service(service_obj)   
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't retreive job list because: %s " % (str(ex)))


    def service_get_job(self, service_obj, job_id):
        '''Implements interface from _JobPluginBase'''
        ## Step 76: Implement service_get_job() 
        try:
            return self.bookkeeper.get_job_for_jobid(service_obj, job_id)   
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't get job list because: %s " % (str(ex)))


    def job_get_state(self, job):
        '''Implements interface from _JobPluginBase'''
        try:
            service = self.bookkeeper.get_service_for_job(job)
            return self.bookkeeper.get_process_for_job(job).getstate()  
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't get job state because: %s " % (str(ex)))


    def job_get_job_id(self, job):
        '''Implements interface from _JobPluginBase'''
        try:
            service = self.bookkeeper.get_service_for_job(job)
            return self.bookkeeper.get_process_for_job(job).getpid(str(service._url))  
            self.log_info("Started local process: %s %s" % (job.get_description().executable, job.get_description().arguments)) 
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't get job id because: %s " % (str(ex)))


    def job_run(self, job):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.run()
        if job.get_description().executable is None:   
            self.log_error_and_raise(bliss.saga.Error.BadParameter, "No executable defined in job description")
        try:
            service = self.bookkeeper.get_service_for_job(job)
            self.bookkeeper.get_process_for_job(job).run(job.get_description())  
            self.log_info("Started local process: %s %s" % (job.get_description().executable, job.get_description().arguments))
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't run job because: %s " % (str(ex)))


    def job_cancel(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.cancel()
        try:
            self.bookkeeper.get_process_for_job(job).terminate()  
            self.log_info("Terminated local process: %s %s" % (job.get_description().executable, job.get_description().arguments)) 
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't cancel job because: %s (already finished?)" % (str(ex)))

 
    def job_wait(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.wait()
        try:
            service = self.bookkeeper.get_service_for_job(job)
            self.bookkeeper.get_process_for_job(job).wait(timeout)   
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't wait for the job because: %s " % (str(ex)))

    def job_get_exitcode(self, job_obj):
        '''Implements interface from _JobPluginBase'''
        try:
            service = self.bookkeeper.get_service_for_job(job_obj)
            #process = self.bookkeeper.get_process_for_job(job_obj)
            #jobstate = process.getstate()

            #if jobstate != bliss.saga.Job.Done or jobstate != bliss.saga.job.Failed:
            #    self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't get the job's exitcode. Job must be in 'Done' or 'Failed' state.")
            #else:
            return self.bookkeeper.get_process_for_job(job_obj).get_exitcode()   
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, "Couldn't get exitcode for job because: %s " % (str(ex)))

