# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import JobPluginInterface, SDPluginInterface

from bliss.plugins.pbs.cmdlinewrapper import PBSService
from bliss.plugins.pbs.bookkeeper import BookKeeper

import time
import bliss.saga

################################################################################
################################################################################

class PBSJobPlugin(JobPluginInterface, SDPluginInterface):
    '''Implements a job plugin that can submit jobs to remote PBS cluster via SSH
    '''
    ## Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.job.pbssh'

    ## Define supported url schemas
    ## 
    _schemas = ['pbs+ssh', 'pbs', 
                'torque', 'torque+ssh', 
                'xt5torque', 'xt5torque+ssh']

    ## Define apis supported by this adaptor
    ##
    _apis = ['saga.job', 'saga.sd']


    ######################################################################
    ##
    def __init__(self, url):
        '''Class constructor'''
        JobPluginInterface.__init__(self, name=self._name, schemas=self._schemas)
        self.bookkeeper = BookKeeper(self)

    ######################################################################
    ##
    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        pass

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
        self.log_info("Unegistered service object %s" \
          % (repr(service_obj)))

    ######################################################################
    ##
    def register_discoverer_object(self, discoverer_obj):
        '''Implements interface from SDPluginInterface'''
        pbs_obj = PBSService(self, discoverer_obj)
        self.bookkeeper.add_service_object(discoverer_obj, pbs_obj)
        self.log_info("Registered new discoverer object %s" \
          % (repr(discoverer_obj))) 

    ######################################################################
    ##
    def unregister_discoverer_object(self, discoverer_obj):
        '''Implements interface from SDPluginInterface'''
        pass


    ######################################################################
    ##
    def discoverer_list_services(self, discoverer_obj, 
                                 service_filter, data_filter):
        '''Implements interface from SDPluginInterface'''
        try:
            pbs = self.bookkeeper.get_pbswrapper_for_service(discoverer_obj)
            service_info = pbs.get_service_info() # triggers ssh connection attempt
            desc = bliss.saga.sd.ServiceDescription()  
            desc._ServiceDescription__init_from_discoverer(discoverer_obj) 
            ## set values
            desc._url = discoverer_obj._url 
            desc._type = "org.ogf.saga.service.job"
            desc._name = "PBS Job Scheduler"

            #desc.Exceptionementor = 
            #desc._site = 
            #desc._uid = 

            return [desc]       

        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't retreive service list because: %s " % (str(ex)))


    ######################################################################
    ##
    def service_description_get_data(self, service_description_obj):
        '''Implements interface from SDPluginInterface'''
        try:
            pbs = self.bookkeeper.get_pbswrapper_for_service(service_description_obj._discoverer)
            service_info = pbs.get_service_info() # triggers ssh connection attempt        

            data = bliss.saga.sd.ServiceData()
            data._ServiceData__init_from_service_description(service_description_obj)
            return data
    
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't retreive service data because: %s " % (str(ex)))

    ######################################################################
    ##
    def service_data_get_attribute(self, serivce_data_obj, key):
        '''Implements interface from SDPluginInterface'''
        try:
            pbs = self.bookkeeper.get_pbswrapper_for_service(serivce_data_obj._discoverer)
            service_info = pbs.get_service_info() # triggers ssh connection attempt
            
            return service_info.get_attribute(key)     
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't retreive service data because: %s " % (str(ex)))
   

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
            self.bookkeeper.add_job_object(job, service_obj,
                bliss.saga.job.JobID(service_obj._url, None))
            return job
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create a new job because: %s " % (str(ex)))


    ######################################################################
    ##
    def service_get_job(self, service_obj, job_id):
        '''Implements interface from _JobPluginBase.
           This method is called for saga.Service.get_job().
        '''
        try:
            # get some information about the job
            pbs = self.bookkeeper.get_pbswrapper_for_service(service_obj)
            jobinfo = pbs.get_jobinfo(job_id)

            job_description = bliss.saga.job.Description()
            job_description.queue = jobinfo.queue
            job = bliss.saga.job.Job()
            job._Job__init_from_service(service_obj=service_obj, 
                                        job_desc=job_description)
            self.bookkeeper.add_job_object(job, service_obj, job_id)
            return job
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't reconnect to job because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_get_state(self, job):
        '''Implements interface from _JobPluginBase.
           This method is called for the saga.Job.state property.'''
        try:
            if self.bookkeeper.get_jobid_for_job(job).native_id == None:
                ## The job hasn't been submitted yet - don't process
                ## it using the PBSwrapper. 
                return bliss.saga.job.Job.New
            else:
                service = self.bookkeeper.get_service_for_job(job)
                pbs = self.bookkeeper.get_pbswrapper_for_service(service)
                return pbs.get_job_state(job.get_job_id())  
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't get job state because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_get_job_id(self, job):
        '''Implements interface from _JobPluginBase.
           This method is called for saga.Job.get_job_id().
        '''
        try:
            if self.bookkeeper.get_jobid_for_job(job).native_id == None:
                ## The job hasn't been submitted yet - don't process
                ## it using the PBSwrapper. 
                return self.bookkeeper.get_jobid_for_job(job)
            else:
                return self.bookkeeper.get_jobid_for_job(job)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't get job id because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_run(self, job):
        '''Implements interface from _JobPluginBase'''
        if self.bookkeeper.get_jobid_for_job(job).native_id != None:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't run the job because: job is not in 'New' state.")

        try:
            service = self.bookkeeper.get_service_for_job(job)
            pbs = self.bookkeeper.get_pbswrapper_for_service(service)
            jobinfo = pbs.submit_job(job) 
            
            sagajobid = bliss.saga.job.JobID(service._url, jobinfo.jobid)
            self.bookkeeper.add_job_object(job, service, sagajobid)

            self.log_info("Started local process: %s %s" \
              % (job.get_description().executable, job.get_description().arguments))
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't run job because: %s " % (str(ex)))


    ######################################################################
    ##
    def job_cancel(self, job_obj):
        '''Implements interface from _JobPluginBase.
           This method is called for saga.Job.cancel().
        '''
        try:
            service = self.bookkeeper.get_service_for_job(job_obj)
            pbs = self.bookkeeper.get_pbswrapper_for_service(service)
            jobinfo = pbs.cancel_job(self.job_get_job_id(job_obj)) 

        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't cancel job because: %s (already finished?)" % (str(ex)))

    ######################################################################
    ## 
    def job_wait(self, job_obj, timeout):
        '''Implements interface from _JobPluginBase.
           This method is called for saga.Job.wait().'''
        try:
            while True:
                state = self.job_get_state(job_obj)
                if state == bliss.saga.job.Job.Running \
                or state == bliss.saga.job.Job.Pending:
                    time.sleep(2)
                else:
                    break
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't wait for job because: %s (already finished?)" % (str(ex)))
 

    ######################################################################
    ## 
    def job_get_exitcode(self, job_obj):
        '''Implements interface from JobPluginInterface.'''
        try:
            service = self.bookkeeper.get_service_for_job(job_obj)
            pbs = self.bookkeeper.get_pbswrapper_for_service(service)
            return pbs.get_jobinfo(self.job_get_job_id(job_obj)).exitcode
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't get job exitcode because: %s " % (str(ex)))

    ######################################################################
    ## 
    def container_object_register(self, container_obj):
        '''Implements interface from JobPluginInterface.'''
        try:
            self.bookkeeper.add_container_object(container_obj, 
              container_obj._service)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create a new job because: %s " % (str(ex)))

    ######################################################################
    ## 
    def container_object_unregister(self, container_obj):
        '''Implements interface from JobPluginInterface.'''
        self.bookkeeper.remove_container_object(service_obj)
        self.log_info("Unegistered container object %s" \
          % (repr(service_obj)))

    ######################################################################
    ## 
    def container_list(self, container_obj):
        '''Implements interface from JobPluginInterface.'''
        try:
            return self.bookkeeper.container_list(container_obj)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't list jobs from container because: %s " % (str(ex)))



    ######################################################################
    ## 
    def container_size(self, container_obj):
        '''Implements interface from JobPluginInterface.'''
        try:
            return len(self.bookkeeper.container_list(container_obj))
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't list jobs from container because: %s " % (str(ex)))



    ######################################################################
    ## 
    def container_add_job(self, container_obj, job_obj):
        '''Implements interface from JobPluginInterface.'''
        if container_obj._service != job_obj._service:
            self.log_error_and_raise(bliss.saga.Error.BadParameter, 
              "Couldn't add job to container because job and container \
               don't seem to be managed to the same service object.")
        try:
            service = self.bookkeeper.add_job_to_container(job_obj, container_obj)
            self.log_info("Added job %s to container %s" % (str(job_obj), str(container_obj)))
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't add job to container because: %s " % (str(ex)))


    ######################################################################
    ## 
    def container_remove_job(self, container_obj, job_obj):
        '''Implements interface from JobPluginInterface.'''
        try:
            service = self.bookkeeper.remove_job_from_container(job_obj, container_obj)
            self.log_info("Removed job %s from container %s" % (str(job_obj), str(container_obj)))
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't remove job from container because: %s " % (str(ex)))


    ######################################################################
    ## 
    def container_run(self, container_obj):
        try: 
            for job in self.container_list(container_obj):
                self.job_run(job)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't start all jobs in the container because: %s " % (str(ex)))


    ######################################################################
    ## 
    def container_get_job(self, container_obj, job_uid):
        try: 
            for job in self.container_list(container_obj):
                if job_uid == job.id:
                    return job
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Container doesn't contain a job with uid: %s " % (job_uid))            
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't start all jobs in the container because: %s " % (str(ex)))
         

    ######################################################################
    ##
    def job_get_bulk_states(self, container):
        '''Optimized bulk-state query for container jobs'''
        try:
            states = list()
            notnew = list()
            for job in self.container_list(container):
                if self.bookkeeper.get_jobid_for_job(job).native_id == None:
                    states.append(bliss.saga.job.Job.New)
                else:
                    notnew.append(job.get_job_id())
                
            pbs = self.bookkeeper.get_pbswrapper_for_service(container._service)
            for state in pbs.get_bulk_job_states(notnew):
                states.append(state)
            return states
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't get bulk (container) job states because: %s " % (str(ex)))

    ######################################################################
    ## 
    def container_wait(self, container_obj, wait_mode, timeout):
        try: 
            for job in self.container_list(container_obj):
                self.job_wait(job, timeout)

        #    all_done = False
        #    while not all_done:
        #        for state in self.job_get_bulk_states(container_obj):
        #            jobs_not_done = 0
        #            if state == bliss.saga.job.Job.Running \
        #            or state == bliss.saga.job.Job.Pending:
        #                jobs_not_done += 1
        #            
        #            if jobs_not_done > 0:
        #                all_done = False
        #                time.sleep(2)
        #            else:
        #                all_done = True
        #
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't wait for jobs in the container because: %s " % (str(ex)))

