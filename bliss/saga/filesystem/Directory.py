# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.Object import Object 

class Directory(Object):
    '''Loosely represents a SAGA directory as defined in GFD.90'''

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new file object
           @param url: Url of the (remote) job manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.Type.FilesystemDirectory, 
                        apitype=Object.Type.FilesystemAPI, session=session)

        if(type(url) == str):
            self._url = Url(str(url))
        else:
            self._url = url

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_directory_object(self)
        self._logger.info("Bound to plugin %s" % (repr(self._plugin)))

    ######################################################################
    ## 
    def __del__(self):
        '''Delete the file object in a civilised fashion.
        '''
        if self._plugin is not None:
            self._plugin.unregister_file_object(self)
        else:
            pass # can't throw here

    ######################################################################
    ## 
    def list(self, pattern=None):
        '''List the directory's content
           @param pattern: File name pattern (like POSIX 'ls')
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.dir_list(self, pattern)

    ######################################################################
    ## 
    def make_dir(self, path, flags=None):
        '''Create a new directoy
           @param path: name/path of the new directory
           @param flags: directory creation flags
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.dir_make_dir(self, path, flags)

    ######################################################################
    ## 
    def copy(self, source, target):
        '''Copy a file from source to target
           @param source: path of the file to copy
           @param target: destination path
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.dir_copy(self, source, target)

    ######################################################################
    ## 
    def get_size(self, path):
        '''Returns the size of a file (in bytes)
           @param path: path of the file
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.dir_get_size(self, path)


    ######################################################################
    ## 
    def close(self):
        '''Closes the directory. 
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.dir_close(self)

