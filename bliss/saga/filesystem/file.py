#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga import Url
from bliss.saga.object import Object 

class File(Object):
    '''Loosely represents a SAGA file as defined in GFD.90'''

    ######################################################################
    ## 
    def __init__(self, url, session=None):
        '''Construct a new file object
           @param url: Url of the (remote) job manager.
           @type  url: L{Url} 
        '''
        Object.__init__(self, Object.FilesystemFile, 
                        apitype=Object.FilesystemAPI, session=session)

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
        pass

