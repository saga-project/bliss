#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.plugins.job.jobinterface import _JobPluginBase
import bliss.saga.job

class LocalJobPlugin(_JobPluginBase):
    '''Implments a job plugin that can submit jobs to the local machine'''

    def __init__(self, url):
        '''Class constructor'''
        _JobPluginBase.__init__(self, name="saga.plugin.job.local")

        self.service_objects = []
        self.job_objects = []
    
    @classmethod
    def supported_schemas(self):
        '''Implements interface from _PluginBase'''
        return ['fork']

    @classmethod
    def plugin_name(self):
        '''Implements interface from _PluginBase'''
        return "saga.plugin.job.local"
        
    @classmethod
    def sanity_check(self):
        '''Implements interface from _PluginBase'''
        # No requirements for this plugin. Always pass.
        return True

    def get_runtime_info(self): 
        '''Implements interface from _PluginBase'''
        str = "Plugin: {!r}. Registered job.service objects: {!r}. Registered job.job objects: {!r}".format(
               self.name, len(self.service_objects), len(self.job_objects))
        return str
       

    def register_service_object(self, service_obj):
        '''Implements interface from _JobPluginBase'''
        # check if we can handle this serivce object. throw if not.
        self.service_objects.append(service_obj) 
        self.logger.info("Registered new Service object {!r}".format(repr(service_obj))) 
   
 
    def register_job_object(self, job_obj):
        '''Implements interface from _JobPluginBase'''
        # check if we can handle this job object. throw if not.

        self.job_objects.append(job_obj)
        self.logger.info("Registered new Job object {!r}".format(repr(job_obj))) 
 
