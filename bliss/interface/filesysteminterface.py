#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import PluginBaseInterface

from bliss.saga.exception_impl import Error as SAGAError
from bliss.saga.exception_impl import Exception as SAGAException

class FilesystemPluginInterface(PluginBaseInterface):
    '''Abstract base class for all filesystem plugins'''
 
    def __init__(self, name, schemas):
        '''Class constructor'''
        PluginBaseInterface.__init__(self, name=name, schemas=schemas,
                                     api=PluginBaseInterface._api_type_saga_filesystem)
    
    def register_file_object(self, file_obj):
        '''This method is called upon instantiation of a new file object
        '''
        errormsg = "Not implemented plugin method called: register_file_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def unregister_file_object(self, file_obj):
        '''This method is called upon deletion of a file object
        '''
        self.log_error("Not implemented plugin method called: unregister_file_object()")
        # don't throw -- destructor context

    def register_directory_object(self, dir_obj):
        '''This method is called upon instantiation of a new file object
        '''
        errormsg = "Not implemented plugin method called: register_directory_object()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def unregister_directory_object(self, dir_obj):
        '''This method is called upon deletion of a file object
        '''
        self.log_error("Not implemented plugin method called: unregister_directory_object()")
        # don't throw -- destructor context

    def file_copy(self, file_obj, target_url):
        '''This method is called upon file.copy()
        '''
        errormsg = "Not implemented plugin method called: file_copy()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg) 

    def dir_list(self, dir_obj, pattern):
        '''This method is called upon file.copy()
        '''
        errormsg = "Not implemented plugin method called: dir_list()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def dir_make_dir(self, dir_obj, path, flags):
        '''This methid is called upon dir.make_dir()
        ''' 
        errormsg = "Not implemented plugin method called: dir_make_dir()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def dir_copy(self, dir_obj, source, target):
        '''This methid is called upon dir.copy()
        ''' 
        errormsg = "Not implemented plugin method called: dir_copy()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

    def dir_get_size(self, dir_obj, path):
        '''This methid is called upon dir.get_size()
        ''' 
        errormsg = "Not implemented plugin method called: dir_copy()"
        self.log_error_and_raise(SAGAError.NotImplemented, errormsg)

