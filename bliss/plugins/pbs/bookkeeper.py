#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


import bliss.saga

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
          'containers' : dict(),
          'jobs' : dict()}
    
    
    def remove_service_object(self, service_obj):
        '''Describe me'''
        service_key = hex(id(service_obj))  
        try:
            self.objects.remove(service_key)
        except Exception:
           pass
    
    
    def remove_job_object(self, job_obj):
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
    
    
    def add_container_object(self, container_obj, service_obj):
        service_key = hex(id(service_obj))  
        container_key = hex(id(container_obj))
        try:
            self.objects[service_key]['containers'][container_key] = {
              'instance':container_obj,
              'jobs':list() }
        except Exception, ex:
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Can't register container: %s" % (ex))   
    
    def remove_container_object(self, container_obj, service_obj):
        service_key = hex(id(service_obj))  
        container_key = hex(id(container_obj))
        try:
            self.objects[service_key]['containers'].remove(container_key)
        except Exception:
            pass

    def add_job_to_container(self, job_obj, container_obj):
        '''Describe me'''
        service_key = hex(id(container_obj._service))  
        container_key = hex(id(container_obj))  
        job_key = hex(id(job_obj))
        try:
            self.objects[service_key]['containers'][container_key]['jobs'].append(job_obj) 
        except Exception, ex:
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Can't add job: %s" % (ex))   

    
    def add_job_object(self, job_obj, service_obj, saga_jobid):
        '''Describe me'''
        service_key = hex(id(service_obj))  
        job_key = hex(id(job_obj))
        try:
            self.objects[service_key]['jobs'][job_key] = {
              'instance':job_obj,
              'jobid':saga_jobid }
        except Exception, ex:
            self.parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Can't register job: %s" % (ex))   
    
    
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
    
