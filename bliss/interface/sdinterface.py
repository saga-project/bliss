#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import PluginBaseInterface

from bliss.saga.exception import Error as SAGAError
from bliss.saga.exception import Exception as SAGAException

class SDPluginInterface(PluginBaseInterface):
    '''Abstract base class for all SD plugins'''

    def __init__(self, name, schemas):
        '''Class constructor'''
        PluginBaseInterface.__init__(self, name=name, schemas=schemas, 
                                     api=PluginBaseInterface._api_type_saga_sd)
    
    def register_discoverer_object(self, discoverer_obj):
        errormsg = "Not implemented plugin method called: register_discoverer_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def unregister_discoverer_object(self, discoverer_obj):
        '''This method is called upon deletion of a new discoverer object'''
        self.log_error("Not implemented plugin method called: unregister_discoverer_object()")
        # don't throw -- destructor context


    ######## Implementation for saga.job.Service functionality 
    ##
    def discoverer_list_services(self, discoverer_obj, service_filter, data_filter):
        errormsg = "Not implemented plugin method called: list_services()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 


    ######## Method templates for saga.Job attributes
    ##
    #def job_get_exitcode(self, job_obj):
    #    errormsg = "Not implemented plugin attribute accessed: job.exitcode"
    #    self.log_error_and_raise(SAGAError.NotImplemented, errormsg)   
