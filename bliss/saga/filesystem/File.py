# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga 
from bliss.saga.Object import Object 

class File(Object):
    '''Loosely represents a SAGA file as defined in GFD.90'''

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new file object
           @param url: Url of the (remote) job manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.Type.FilesystemFile, 
                        apitype=Object.Type.FilesystemAPI, session=session)

        if type(url) == str:
            self._url = bliss.saga.Url(str(url))
        elif type(url) == bliss.saga.Url:
            self._url = url
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
              "File constructor expects str or bliss.saga.Url type as 'url' parameter")

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_file_object(self)
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
    def copy(self, target):
        '''Copy the file to another location
           @param target: Url of the copy target.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            if type(target) == str:
                target_url = bliss.saga.Url(str(target))
            elif type(target) == bliss.saga.Url:
                target_url = url
            else:
                raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
                  "File.copy() expects str or bliss.saga.Url type as 'target' parameter")

            return self._plugin.file_copy(self, target)

    ######################################################################
    ## 
    def move(self, target):
        '''Move the file to another location
           @param target: Url of the copy target.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.file_copy(self, target)

    ######################################################################
    ## 
    def remove(self):
        '''Delete the file
           @param target: Url of the copy target.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.file_copy(self, target)

    ######################################################################
    ## 
    def get_size(self):
        '''Returns the size of a file (in bytes)
           @param path: path of the file
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.file_get_size(self)
