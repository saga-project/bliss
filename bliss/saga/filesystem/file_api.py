#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.object_api import Object 

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

        if(type(url) == str):
            self._url = Url(str(url))
        else:
            self._url = url

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
        '''Copy the file
           @param target: Url of the copy target.
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.file_copy(self, target)

