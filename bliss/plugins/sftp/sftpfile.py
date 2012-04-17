#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import FilesystemPluginInterface

from bliss.plugins import utils

import os, pwd
import time
import bliss.saga

import logging
import paramiko

################################################################################
################################################################################

class SSHConnectionPool:
    '''Encapsulates SSH connections
    '''
    def __init__(self, parent):
        '''Constructor
        '''
        self._parent = parent
        self._connections = dict()

    
    def key_from_object(self, fsobj):
        '''Returns a dictionary key for an object based on
           its url and contexts
        '''
        # inspect contexts and see if they're any good
        usable_ctx = None
        for ctx in fsobj.session.contexts:
            if ctx.type is bliss.saga.Context.SSH:
                usable_ctx = ctx
                break

        # use username from context, or uid if not defined
        username = pwd.getpwuid(os.getuid()).pw_name
        if usable_ctx is not None: 
            if usable_ctx.userid is not None:
                username = usable_ctx.userid

        # get port or default to 22
        port = str(22)
        if fsobj._url.port is not None:
            port = fsobj._url.port
    
        # get hostname
        hostname = 'localhost'
        if fsobj._url.host is not None:
            hostname = fsobj._url.host

        # keys have the format username@hostname:port
        return (username, hostname, port)

    
    def get_connection(self, fsobj):
        '''Return a connection object for a given file object.
           If it doesn't exist, it will get created
        '''
        (username, hostname, port) = self.key_from_object(fsobj)
        fsobj_key = "%s@%s:%s" % (username, hostname, port)

        if fsobj_key in self._connections:
            self._parent.log_debug("Found exisitng connection object for %s"\
              % fsobj_key)
            return self._connections[fsobj_key]
        else:
            try: 
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                ssh.connect(hostname=hostname, port=int(port), username=username, allow_agent=True, look_for_keys=True)
                self._parent.log_info("Created new connection object for %s" % fsobj_key)
                # add connection to connection pool
                self._connections[fsobj_key] = ssh
                return self._connections[fsobj_key] 
            except Exception, ex:
                self._parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't create SFTP connection: %s " % (str(ex)))


################################################################################
################################################################################

class SFTPFilesystemPlugin(FilesystemPluginInterface):
    '''Implements a filesystem plugin that does things via SSH
    '''
    ## Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.file.sftp'

    ## Define supported url schemas
    ## 
    _schemas = ['sftp']

    ## Define apis supported by this adaptor
    ##
    Exceptions = ['saga.filesystem']


    ##
    def __init__(self, url):
        '''Class constructor'''
        FilesystemPluginInterface.__init__(self, name=self._name, schemas=self._schemas)
        self._cp = SSHConnectionPool(self)

        # make paramiko's logger less verbose
        paramiko.util.logging.getLogger("paramiko").setLevel(logging.ERROR)

    @classmethod
    def sanity_check(self):
        '''Implements interface from PluginBaseInterface
        '''
        try:
            import paramiko
        except Exception, ex:
            raise Exception("paramiko module missing")
 
    def entry_getstat(self, obj, entry_path=None):
        # if no path is given, use the one from
        # the object's url
        path = "."


        if entry_path is not None:
            if entry_path.startswith("/") is True:
                #absolute path
                path = entry_path
            else:
                #relative path
                path = "%s/%s" % (obj._url.path, entry_path)
        elif obj._url.path is not None:
            if len(obj._url.path) > 0:
                path = obj._url.path

        try:
            ssh = self._cp.get_connection(obj)
            sftp = ssh.open_sftp()
            filestat = sftp.stat(path)
            self.log_info("SFTP stat for '%s' returned: '%s'" % (path, filestat))
            return filestat
        except IOError, ex:
            if ex.errno == 2:
                return None
            else:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't access entry: %s " % (str(ex)))
        except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't access entry: %s " % (str(ex)))


    def register_file_object(self, file_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        stat = self.entry_getstat(file_obj)
        if stat == None:
            self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
            "Couldn't open %s. Entry doesn't exist." % file_obj._url)
        else:
            pass
        

    def unregister_file_object(self, service_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        pass


    def register_directory_object(self, dir_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        stat = self.entry_getstat(dir_obj)
        if stat == None:
            self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
            "Couldn't open %s. Entry doesn't exist." % (dir_obj._url))
        elif str(stat).startswith("d") is not True:
            self.log_error_and_raise(bliss.saga.Error.BadParameter, 
            "Couldn't open %s. Entry is a file and not a directory." % (dir_obj._url))
            

    def unregister_directory_object(self, dir_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        pass


    def dir_list(self, dir_obj, pattern):
        path = "."
        if dir_obj._url.path is not None:
            path = dir_obj._url.path
        try:
            ssh = self._cp.get_connection(dir_obj)
            sftp = ssh.open_sftp()
            return sftp.listdir(path)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
            "Couldn't list directory: %s " % (str(ex)))


    def dir_get_size(self, dir_obj, path):
        '''Implements interface from FilesystemPluginInterface
        '''
        if path is not None:
            if path.startswith("/") is True:
                complete_path = path
            else:
                complete_path = "%s/%s" % (dir_obj._url.path, path)
        try:
            stat = self.entry_getstat(dir_obj, path)
            return stat.st_size    
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
            "Couldn't determine size for '%s': %s " % (path, (str(ex))))


    def dir_make_dir(self, dir_obj, path, flags):
        '''Implements interface from FilesystemPluginInterface
        '''
        if path is not None:
            if path.startswith("/") is True:
                complete_path = path
            else:
                complete_path = "%s/%s" % (dir_obj._url.path, path)
        
        # throw exception if directory already exists
        stat = self.entry_getstat(dir_obj, path)
        if stat != None:
            self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
            "Couldn't create directory '%s'. Entry already exist." % (complete_path))

        try:
            ssh = self._cp.get_connection(dir_obj)
            sftp = ssh.open_sftp()
            sftp.mkdir(complete_path)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
            "Couldn't create directory: %s " % (str(ex)))


    def dir_copy(self, dir_obj, source, target):
        '''Implements interface from FilesystemPluginInterface
        '''
        basepath = dir_obj._url.path
        full_path = os.path.join(basepath, source)

        if(type(target) == str):
            target_url = bliss.saga.Url(str(target))
        else:
            target_url = target

        if target_url.host != 'localhost':
            error = 'Only sftp://localhost/... supported as target'
            self.log_error_and_raise(bliss.saga.Error.BadParameter, 
            "Couldn't copy '%s' to '%s': %s " % (full_path, target_url, error))

        target_path = str(target_url.path)
        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                target_path += os.path.basename(full_path)
            else:
                self.log_error_and_raise(bliss.saga.Error.AlreadyExists, 
                "Couldn't copy '%s' to '%s': target already exists." % (full_path, target_url))
 
        try:
            ssh = self._cp.get_connection(dir_obj)
            sftp = ssh.open_sftp()
            self.log_info("trying to copy %s -> %s" % (full_path, target_path))
            sftp.get(full_path, target_path)
        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
            "Couldn't copy '%s' to '%s': %s " % (full_path, target_path, str(ex)))


