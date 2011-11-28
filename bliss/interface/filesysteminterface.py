#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import PluginBaseInterface

from bliss.saga.exception import Error as SAGAError
from bliss.saga.exception import Exception as SAGAException

class FilesystemPluginInterface(PluginBaseInterface):
    '''Abstract base class for all filesystem plugins'''
 
    def __init__(self, name, schemas):
        '''Class constructor'''
        PluginBaseInterface.__init__(self, name=name, schemas=schemas,
                                     api=PluginBaseInterface._api_type_saga_filesystem)
    
    def register_file_object(self, service_obj):
        errormsg = "Not implemented plugin method called: register_service_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def unregister_file_object(self, service_obj):
        '''This method is called upon deletion of a new service object'''
        self.log_error("Not implemented plugin method called: unregister_service_object()")
        # don't throw -- destructor context
