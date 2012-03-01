#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import PluginBaseInterface

from bliss.saga.exception_api import Error as SAGAError
from bliss.saga.exception_api import Exception as SAGAException

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


    ######## Implementation for saga.sd.Discoverer functionality 
    ##
    def discoverer_list_services(self, discoverer_obj, service_filter, data_filter):
        errormsg = "Not implemented plugin method called: list_services()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 


    ######## Implementation for saga.sd.ServiceDescription functionality 
    ##
    def service_description_get_data(self, servide_description_obj):
        errormsg = "Not implemented plugin method called: get_data()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)


    ######## Implementation for saga.sd.ServiceDescription functionality 
    ##
    def service_data_attribute_exists(self, servide_data_obj, key):
        errormsg = "Not implemented plugin method called: attribute_exists()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)  

    ######## Implementation for saga.sd.ServiceDescription functionality 
    ##
    def service_data_get_attribute(self, servide_data_obj, key):
        errormsg = "Not implemented plugin method called: get_attribute()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)  

