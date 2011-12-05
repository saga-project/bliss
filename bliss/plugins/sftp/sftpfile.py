#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
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
    _name = 'saga.plugin.file.ssh'

    ## Define supported url schemas
    ## 
    _schemas = ['sftp']

    ## Define apis supported by this adaptor
    ##
    _apis = ['saga.filesystem']


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
 
    def entry_exists(self, obj, entry_path=None):
        # if no path is given, use the one from
        # the object's url
        if entry_path is not None:
            if entry_path.startswith("/") is True:
                #absolute path
                path = entry_path
            else:
                #relative path
                path = "%s/%s" % (obj._url.path, entry_path)
        elif obj._url.path is not None:
            path = obj._url.path
        else:
            path = "."
        try:
            ssh = self._cp.get_connection(obj)
            sftp = ssh.open_sftp()
            filestat = sftp.stat(path)
            self.log_info("SFTP stat for '%s' returned: '%s'" % (path, filestat))
            return True
        except IOError, ex:
            if ex.errno == 2:
                return False
            else:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't open directory: %s " % (str(ex)))
        except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't open directory: %s " % (str(ex)))



    def register_file_object(self, file_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        if self.entry_exists(file_obj) != True:
            self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
            "Couldn't open %s. File doesn't exist." % file_obj._url)
        else:
            pass
        

    def unregister_file_object(self, service_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        pass


    def register_directory_object(self, dir_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        if self.entry_exists(dir_obj) != True:
            self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
            "Couldn't open %s. File doesn't exist." % (dir_obj._url))
        else:
            pass

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
            self._parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
            "Couldn't list directory: %s " % (str(ex)))


    def dir_make_dir(self, dir_obj, path, flags):
        '''Implements interface from FilesystemPluginInterface
        '''
        if path is not None:
            if path.startswith("/") is True:
                complete_path = path
            else:
                complete_path = "%s/%s" % (dir_obj._url.path, path)
        
        # throw exception if directory already exists
        if self.entry_exists(dir_obj, path) == True:
            self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
            "Couldn't create directory '%s'. Entry already exist." % (complete_path))

        try:
            ssh = self._cp.get_connection(dir_obj)
            sftp = ssh.open_sftp()
            sftp.mkdir(complete_path)
        except Exception, ex:
            self._parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
            "Couldn't create directory: %s " % (str(ex)))


