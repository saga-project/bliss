# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga 
from bliss.saga.Object import Object 

class File(Object):
    '''Loosely represents a SAGA file as defined in GFD.90

    The saga.filesystem.File class represents, as the name indicates,
    a file on some (local or remote) filesystem.  That class offers
    a number of operations on that file, such as copy, move and remove::
    
        # get a file handle
        file = saga.filesystem.File("sftp://localhost/tmp/data/data.bin")
    
        # copy the file
        file.copy ("sftp://localhost/tmp/data/data.bak")

        # move the file
        file.move ("sftp://localhost/tmp/data/data.new")

    '''

    ######################################################################
    ## 
    def __init__(self, url, flags=None, session=None):
        '''Construct a new file object

           @param url: Url of the (remote) file
           @type  url: L{Url} 

           The specified file is expected to exist -- otherwise a DoesNotExist
           exception is raised.  Also, the URL must point to a file (not to
           a directory), otherwise a BadParameter exception is raised.

           Example::

               # get a file handle
               file = saga.filesystem.File("sftp://localhost/tmp/data/data.bin")
    
               # print the file's size
               print file.get_size ()

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

        if flags is None:
            _flags = 0
        else:
            _flags = flags

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_file_object(self, flags)
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
    def get_url(self):
        '''Return the complete url pointing to the file.

           The call will return the complete url pointing to
           this file as a saga.Url object::

               # print URL of a file
               file = saga.filesystem.File("sftp://localhost/etc/passwd")
               print file.get_url()
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._url

    ######################################################################
    ## 
    def copy(self, target, flags=None):
        '''Copy the file to another location

           @param target: Url of the copy target.
           @param flags: Flags to use for the operation.


           The file is copied to the given target location.  The target URL must
           be an absolute path, and can be a target file name or target
           directory name.  If the target file exists, it is overwritten::

               # copy a file
               file = saga.filesystem.Directory("sftp://localhost/tmp/data/data.bin")
               file.copy ("sftp://localhost/tmp/data/data.bak")
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            if type(target) == str:
                _target_url = bliss.saga.Url(str(target))
            elif type(target) == bliss.saga.Url:
                _target_url = target
            else:
                raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
                  "File.copy() expects str or bliss.saga.Url type as 'target' parameter")

            if flags is None:
                _flags = 0
            else:
                _flags = flags

            return self._plugin.file_copy(self, _target_url, _flags)

    ######################################################################
    ## 
    def move(self, target, flags=None):
        '''Move the file to another location

           @param target: Url of the move target.
           @param flags: Flags to use for the operation.

           The file is copied to the given target location.  The target URL must
           be an absolute path, and can be a target file name or target
           directory name.  If the target file exists, it is overwritten::

               # copy a file
               file = saga.filesystem.Directory("sftp://localhost/tmp/data/data.bin")
               file.move ("sftp://localhost/tmp/data/data.bak")
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            if type(target) == str:
                _target_url = bliss.saga.Url(str(target))
            elif type(target) == bliss.saga.Url:
                _target_url = target
            else:
                raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
                  "File.move() expects str or bliss.saga.Url type as 'target' parameter")

            if flags is None:
                _flags = 0
            else:
                _flags = flags

        else:
            return self._plugin.file_move(self, _target_url, _flags)

    ######################################################################
    ## 
    def remove(self):
        '''Delete the file '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.file_remove(self)

    ######################################################################
    ## 
    def get_size(self):
        '''Returns the size of a file (in bytes)

           Example::

               # get a file handle
               file = saga.filesystem.File("sftp://localhost/tmp/data/data.bin")
    
               # print the file's size
               print file.get_size ()

        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.file_get_size(self)

