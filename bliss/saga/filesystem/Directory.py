# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import fnmatch
import bliss.saga 
from bliss.saga import Url
from bliss.saga.Object import Object 

class Directory(Object):
    '''Loosely represents a SAGA directory as defined in GFD.90
    
    The saga.filesystem.Directory class represents, as the name indicates,
    a directory on some (local or remote) filesystem.  That class offers
    a number of operations on that directory, such as listing its contents,
    copying files, or creating subdirectories::
    
        # get a directory handle
        dir = saga.filesystem.Directory("sftp://localhost/tmp/")
    
        # create a subdir
        dir.make_dir ("data/")
    
        # list contents of the directory
        files = dir.list ()
    
        # copy *.dat files into the subdir
        for f in files :
            if f ^ '^.*\.dat$' :
                dir.copy (f, "sftp://localhost/tmp/data/")
    '''

    ######################################################################
    ## 
    def __init__(self, url, flags=None, session=None):
        '''Construct a new directory object

           @param url: Url of the (remote) file system.
           @type  url: L{Url} 

           The specified directory is expected to exist -- otherwise
           a DoesNotExist exception is raised.  Also, the URL must point to
           a directory (not to a file), otherwise a BadParameter exception is
           raised.

           Example::

               # open some directory
               dir = saga.filesystem.Directory("sftp://localhost/tmp/")

               # and list its contents
               files = dir.list ()

        '''
        Object.__init__(self, Object.Type.FilesystemDirectory, 
                        apitype=Object.Type.FilesystemAPI, session=session)

        if type(url) == str:
            self._url = bliss.saga.Url(str(url))
        elif type(url) == bliss.saga.Url:
            self._url = url
        else:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
              "File constructor expects str or bliss.saga.Url type as 'url' parameter")

        # Directory paths end with "/" by convention
        if self._url.path.endswith("/") != True :
            self._url.path = "%s/" % self._url.path

        if flags is None:
            _flags = 0
        else:
            _flags = flags

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_directory_object(self, _flags)
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
        '''Return the complete url pointing to the directory.

           The call will return the complete url pointing to
           this directory as a saga.Url object::

               # print URL of a directory
               dir = saga.filesystem.Directory("sftp://localhost/tmp/")
               print dir.get_url()
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._url


    ######################################################################
    ## 
    def list(self, pattern=None):
        '''List the directory's content
           @param pattern: File name pattern (like POSIX 'ls', e.g. '*.txt')

           The call will return a list of files and subdirectories within the
           directory::

               # list contents of the directory
               for f in dir.list() :
                   print f

        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            if pattern != None:
                try:
                    filtered_entries = []
                    for entry in self._plugin.dir_list(self):
                        if fnmatch.fnmatch(entry, pattern):
                            filtered_entries.append(entry)
                    return filtered_entries
                except Exception, ex:
                    raise bliss.saga.Exception(bliss.saga.Error.BadParameter, 
                    "Problem with filter pattern '%s': %s" % (pattern, ex))
            else:   
                return self._plugin.dir_list(self)

    ######################################################################
    ## 
    def remove(self, path=None):
        '''Removes the directory

           If no path is given, the remote directory associated with
           the object is removed. If a relative or absolute path is given,
           that given target is removed instead.  The target must be a 
           directory.

           @param path: (relative or absolute) path to a directory

       
           Example::

               # remove a subdir 'data' in /tmp
               dir = saga.filesystem.Directory("sftp://localhost/tmp/")
               dir.remove ('data/')
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            return self._plugin.dir_remove(self, path)

    ######################################################################
    ## 
    def make_dir(self, path, flags=None):
        '''Create a new directoy
           @param path: name/path of the new directory
           @param flags: directory creation flags

           The call creates a directory at the given location.

           Example::

               # create a subdir 'data' in /tmp
               dir = saga.filesystem.Directory("sftp://localhost/tmp/")
               dir.make_dir ('data/')

        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            if flags is None:
                _flags = 0
            else:
                _flags = flags
            return self._plugin.dir_make_dir(self, path, _flags)


    ######################################################################
    ## 
    def open_dir(self, path, flags=None):
        '''Open and return a new directoy
           @param path: name/path of the directory to open
           @param flags: directory creation flags

           The call opens and returns a directory at the given location.

           Example::

               # create a subdir 'data' in /tmp
               dir = saga.filesystem.Directory("sftp://localhost/tmp/")
               data = dir.open_dir ('data/', saga.filesystem.Create)
        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            if flags is None:
                _flags = 0
            else:
                _flags = flags
            return self._plugin.dir_open_dir(self, path, _flags)


    ######################################################################
    ## 
    def copy(self, source, target, flags=None):
        '''Copy a file from source to target
           @param source: path of the file to copy
           @param target: absolute URL of target directory

           The source is copied to the given target directory.  The path of the
           source can be relative::

               # copy a file
               dir = saga.filesystem.Directory("sftp://localhost/tmp/")
               dir.copy ("./data.bin", "sftp://localhost/tmp/data/")

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
                  "Directory.copy() expects str or bliss.saga.Url type as 'target' parameter")

            if type(source) == str:
                _source_url = bliss.saga.Url(str(source))
            elif type(source) == bliss.saga.Url:
                _source_url = source
            else:
                raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
                  "Directory.copy() expects str or bliss.saga.Url type as 'source' parameter")

            if flags is None:
                _flags = 0
            else:
                _flags = flags

            return self._plugin.dir_copy(self, _source_url, _target_url, _flags)

    ######################################################################
    ## 
    def move(self, source, target, flags=None):
        '''Move a file from source to target
           @param source: path of the file to copy
           @param target: absolute URL of target directory

           The source is moved to the given target directory.  The path of the
           source can be relative::

               # copy a file
               dir = saga.filesystem.Directory("sftp://localhost/tmp/")
               dir.move ("./data.bin", "sftp://localhost/tmp/data/")

        '''
        if self._plugin is None:
            raise bliss.saga.Exception(bliss.saga.Error.NoSuccess, 
              "Object not bound to a plugin")
        else:
            if type(target) == str:
                target_url = bliss.saga.Url(str(target))
            elif type(target) == bliss.saga.Url:
                target_url = target
            else:
                raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
                  "Directory.move() expects str or bliss.saga.Url type as 'target' parameter")

            if type(source) == str:
                _source_url = bliss.saga.Url(str(source))
            elif type(source) == bliss.saga.Url:
                _source_url = source
            else:
                raise bliss.saga.Exception(bliss.saga.Error.NoSuccess,
                  "Directory.move() expects str or bliss.saga.Url type as 'source' parameter")

            if flags is None:
                _flags = 0
            else:
                _flags = flags

            return self._plugin.dir_move(self, _source_url, _target_url, _flags)

    ######################################################################
    ## 
    def get_size(self, path=None):
        '''Returns the size of a file or directory (in bytes)

           @param path: path of the file or directory

           Example::

               # inspect a file for its size
               dir  = saga.filesystem.Directory("sftp://localhost/tmp/")
               size = dir.get_size ('data/data.bin')
               print size

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

