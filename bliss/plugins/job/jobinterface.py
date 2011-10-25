#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import logging

from bliss.plugins.pluginbase import _PluginBase
from bliss.plugins.pluginbase import _api_type_saga_job

from bliss.saga import exception
import bliss.saga.job


class _JobPluginBase(_PluginBase):
    '''Abstract base class for all job plugins'''
    
    def __init__(self, name):
        '''Class constructor'''
        _PluginBase.__init__(self, name=name)
        self.logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')') 
    
    @classmethod
    def supported_api(self):
        '''Implements interface from _PluginBase'''
        return _api_type_saga_job

    def create_job(self, js_url, job_description):     
        '''Implement interface from _JobPluginBase'''
        job = bliss.saga.job.Job(js_url, job_description)
        return job

    def register_service_object(self, service_obj):
        '''This method is called upon instantiation of a new service object'''
        raise exception.Exception(NotImplemented, "{!s}: register_service_object() is not implemented".format(repr(self))) 

    def register_job_object(self, job_obj):
        '''This method is called upon instatiation of a new job object'''
        raise exception.Exception(NotImplemented, "{!s}: register_job_object() is not implemented".format(repr(self))) 

    def get_job(self, job_id):
        self.logger.error("Not implemented plugin method called: get_job()")
        raise exception.Exception(NotImplemented, "{!s}: get_job() is not implemented".format(repr(self))) 

    def list(self):
        self.logger.error("Not implemented plugin method called: list()")
        raise exception.Exception(NotImplemented, "{!s}: list_jobs() is not implemented".format(repr(self)))  

