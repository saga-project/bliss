#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.job.jobinterface  import _JobPluginBase
from bliss.plugins.job.pbssh.cmdlinewrapper import PBSSHCmdLineWrapper, PBSService
from bliss.plugins import utils

import bliss.saga

class PBSOverSSHJobPlugin(_JobPluginBase):
    '''Implements a job plugin that can submit jobs to remote PBS cluster via SSH
    '''
    ## Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.job.pbssh'

    ## Define supported url schemas
    ## 
    _schemas = ['pbs+ssh', 'pbs']

    ######################################################################
    ##
    class BookKeeper:
        '''Keeps track of job and service objects'''
        def __init__(self, parent):
            self.objects = {}
            self.parent = parent
        

        def add_service_object(self, service_obj, pbs_obj):
            '''Describe me'''
            service_key = hex(id(service_obj))  
            self.objects[service_key] = {
              'saga_instance' : service_obj, 
              'pbs_instance' : pbs_obj, 
              'jobs' : dict()}


        def remove_service_obj(self, service_obj):
            '''Describe me'''
            service_key = hex(id(service_obj))  
            try:
                self.objects.remove(service_key)
            except Exception:
                pass


        def remove_job_obj(self, job_obj):
            '''Describe me'''
            service_key = hex(id(self.get_service_for_job(job_obj)))  
            job_key = hex(id(job_obj))  
            try:
                self.objects[service_key]['jobs'].remove(job_key)
            except Exception:
                pass


        def get_pbswrapper_for_service(self, service_obj):
            '''Describe me'''
            service_key = hex(id(service_obj))  
            return self.objects[service_key]['pbs_instance']


        def add_job_object_to_service(self, job_obj, service_obj, saga_jobid):
            '''Describe me'''
            service_key = hex(id(service_obj))  
            job_key = hex(id(job_obj))
            try:
                self.objects[service_key]['jobs'][job_key] = {
                  'instance':job_obj,
                  'jobid':saga_jobid }
            except Exception, ex:
                self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "Can't register job: %s %s" % (ex, utils.get_traceback()))   


        def get_service_for_job(self, job_obj):
            '''Return the service object the job is registered with'''
            for key in self.objects.keys():
                job_key = hex(id(job_obj))
                if job_key in self.objects[key]['jobs']:
                    return self.objects[key]['saga_instance']
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "INTERNAL ERROR: Job object %s is not known by this plugin %s" \
              % (job_obj, utils.get_traceback())) 


        def get_jobid_for_job(self, job_obj):
            '''Return the local process object for a given job'''
            try:
                service_key = hex(id(self.get_service_for_job(job_obj)))  
                job_key = hex(id(job_obj))  
                return self.objects[service_key]['jobs'][job_key]['jobid']
            except Exception, ex:
                self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "INTERNAL ERROR: Job object %s is not associated with a process %s" \
                  % (job_obj, utils.get_traceback()))   



    ######################################################################
    ##
    def __init__(self, url):
        '''Class constructor'''
        _JobPluginBase.__init__(self, name=self._name, schemas=self._schemas)
        self.bookkeeper = self.BookKeeper(self)

    ######################################################################
    ##
    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        try: 
            from openssh_wrapper import SSHConnection
        except Exception, ex:
            raise Exception("openssh_wrapper module missing")

    ######################################################################
    ##
    def register_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        pbs_obj = PBSService(self, service_obj)
        self.bookkeeper.add_service_object(service_obj, pbs_obj)
        self.log_info("Registered new service object %s" \
          % (repr(service_obj))) 

    ######################################################################
    ##
    def unregister_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        self.bookkeeper.remove_service_object(service_obj)
        self.log_info("Unegistered new service object %s" \
          % (repr(service_obj))) 


    ######################################################################
    ##
    def unregister_job_object(self, job_obj):
        '''Implements interface from _JobPluginBase'''
        self.bookkeeper.remove_job_object(job_obj)
        self.log_info("Unegisteredjob object %s" \
          % (repr(job_obj))) 


    ######################################################################
    ##  
    def service_list(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        try:
            pbs = self.bookkeeper.get_pbswrapper_for_service(service_obj)
            return pbs.list_jobs()
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't retreive job list because: %s " % (str(ex)))

    ######################################################################
    ##  
    def service_create_job(self, service_obj, job_desc):
        '''Implements interface from _JobPluginBase'''


    ######################################################################
    ##
    def service_get_job(self, service_obj, job_id):
        '''Implements interface from _JobPluginBase'''
        ## Step 76: Implement service_get_job() 
        try:
            # get some information about the job
            pbs = self.bookkeeper.get_pbswrapper_for_service(service_obj)
            jobinfo = pbs.get_jobinfo(job_id)

            job_description = bliss.saga.job.Description()
            job_description.queue = jobinfo.queue
            job = bliss.saga.job.Job()
            job._Job__init_from_service(service_obj=service_obj, 
                                        job_desc=job_description)
            self.bookkeeper.add_job_object_to_service(job, service_obj, job_id)
            return job
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't reconnect to job because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_get_state(self, job):
        '''Implements interface from _JobPluginBase'''
        try:
            service = self.bookkeeper.get_service_for_job(job)
            pbs = self.bookkeeper.get_pbswrapper_for_service(service)
            # jobs disappear from the pbs job list
            # once they're done. 
            return pbs.get_job_state(job.get_job_id())  
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't get job state because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_get_job_id(self, job):
        '''Implements interface from _JobPluginBase'''
        try:
            return self.bookkeeper.get_jobid_for_job(job)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't get job id because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_run(self, job):
        '''Implements interface from _JobPluginBase'''
        if job.get_description().executable is None:   
            self.log_error_and_raise(bliss.saga.Error.BadParameter, 
              "No executable defined in job description")
        try:
            service = self.bookkeeper.get_service_for_job(job)

            self.bookkeeper.get_process_for_job(job).run()  
            self.log_info("Started local process: %s %s" \
              % (job.get_description().executable, job.get_description().arguments))
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't run job because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_cancel(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        ## Step X: implement job.cancel()
        try:
            self.bookkeeper.get_process_for_job(job).terminate()  
            self.log_info("Terminated local process: %s %s" \
              % (job.get_description().executable, job.get_description().arguments)) 
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't cancel job because: %s (already finished?)" % (str(ex)))


    ######################################################################
    ## 
    def job_wait(self, job, timeout):
        '''Implements interface from _JobPluginBase'''
        try:
            service = self.bookkeeper.get_service_for_job(job)
            self.bookkeeper.get_process_for_job(job).wait(timeout)   
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't wait for the job because: %s " % (str(ex)))

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
