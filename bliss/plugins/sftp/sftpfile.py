# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import FilesystemPluginInterface

import os, pwd
import time
import bliss.saga

import logging
import paramiko

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

        # url username always overwrites everything else!
        if fsobj._url.username is not None:
            username = fsobj._url.username

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

    def remove_connection(self, fsobj): 
        '''Remove a connection from the pool. If it is still open, it 
           is closed automatically'''
        (username, hostname, port) = self.key_from_object(fsobj)
        fsobj_key = "%s@%s:%s" % (username, hostname, port)

        if self._connections.has_key(fsobj_key):
            try:
                # try to close connection, but ignore any errors
                conn = self.get_connection(fsobj)
                conn.close()
            except Exception:
                pass
            #delete the connection from dict
            del self._connections[fsobj_key]
    
    def get_connection(self, fsobj):
        '''Return a connection object for a given file/dir object.
           If it doesn't exist, it is created
        '''
        (username, hostname, port) = self.key_from_object(fsobj)
        fsobj_key = "%s@%s:%s" % (username, hostname, port)
        if fsobj_key in self._connections:
            self._parent.log_debug("Found exisitng connection object for %s"\
              % fsobj_key)
            return self._connections[fsobj_key]
        else:
            #try: 
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                ssh.connect(hostname=hostname, port=int(port), username=username, allow_agent=True, look_for_keys=True)
                self._parent.log_info("Created new connection object for %s" % fsobj_key)
                # add connection to connection pool
                self._connections[fsobj_key] = ssh
                return self._connections[fsobj_key] 
            #except Exception, ex:
            #    self._parent.log_error_and_raise(bliss.saga.Error.NoSuccess, 
            #    "Couldn't create SFTP connection: %s " % (str(ex)))


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
    ######################################################################
    ##  
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
                "Couldn't access entry '%s': %s " % (path,(str(ex))))
        except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't access entry '%s': %s " % (path,(str(ex))))

    ######################################################################
    ## 
    def register_file_object(self, file_obj, flags):
        '''Implements interface from FilesystemPluginInterface
        '''
        furl = file_obj._url
        if (furl.host == "localhost") or (furl.host == None):
            # This is a local file!
            file_obj.is_local = True

            if os.path.exists(furl.path):
                if os.path.isdir(furl.path) == True:
                    self.log_error_and_raise(bliss.saga.Error.BadParameter, 
                     "Couldn't open file %s. URL points to a directory." % (file_obj._url))       
            else:                        
                self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
                 "Couldn't open %s. File doesn't exist." % (file_obj._url))

        else:
            file_obj.is_local = False

            try:
                ssh = self._cp.get_connection(file_obj)
                sftp = ssh.open_sftp()
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't open file: %s " % (str(ex)))

            stat = self.entry_getstat(file_obj)
            if stat == None:
                self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
                 "Couldn't open %s. File doesn't exist." % (file_obj._url))
            elif str(stat).startswith("d") is True:
                self.log_error_and_raise(bliss.saga.Error.BadParameter, 
                 "Couldn't open file %s. URL points to a directory." % (file_obj._url))       
 
    ######################################################################
    ## 
    def unregister_file_object(self, service_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        pass

    ######################################################################
    ## 
    def register_directory_object(self, dir_obj, flags):
        '''Implements interface from FilesystemPluginInterface
        '''
        furl = dir_obj._url
        if (furl.host == "localhost") or (furl.host == None):
            # This is a local file!
            dir_obj.is_local = True

            if os.path.exists(furl.path):
                if os.path.isdir(furl.path) == False:
                    self.log_error_and_raise(bliss.saga.Error.BadParameter, 
                     "Couldn't open directory %s. URL points to a file." % (dir_obj._url))       
            else:                   
                if flags & bliss.saga.filesystem.Create:
                    self.dir_make_dir(dir_obj, furl.path, flags)
                else:
                    self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
                    "Couldn't open %s. File doesn't exist." % (dir_obj._url))

        else:
            dir_obj.is_local = False
            # This is a remote file
            try:
                ssh = self._cp.get_connection(dir_obj)
                sftp = ssh.open_sftp()
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't open file: %s " % (str(ex)))

            stat = self.entry_getstat(dir_obj)
            if stat == None:
                if flags & bliss.saga.filesystem.Create:
                    self.dir_make_dir(dir_obj, furl.path, flags)
                else:
                    self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
                    "Couldn't open %s. File doesn't exist." % (dir_obj._url))
            elif str(stat).startswith("d") is False:
                self.log_error_and_raise(bliss.saga.Error.BadParameter, 
                 "Couldn't open directory %s. URL points to a file." % (dir_obj._url))       

        #try:
        #    ssh = self._cp.get_connection(dir_obj)
        #    sftp = ssh.open_sftp()
        #except Exception, ex:
        #    self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
        #    "Couldn't open directory '%s': %s " % (dir_obj._url, str(ex)))


        #stat = self.entry_getstat(dir_obj)
        #if stat == None:
        #    self.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
        #    "Couldn't open %s. Entry doesn't exist." % (dir_obj._url))
        #elif str(stat).startswith("d") is not True:
        #    self.log_error_and_raise(bliss.saga.Error.BadParameter, 
        #    "Couldn't open %s. Entry is a file and not a directory." % (dir_obj._url))
            
    ######################################################################
    ## 
    def unregister_directory_object(self, dir_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        pass

    ######################################################################
    ## 
    def dir_close(self, dir_obj):
        ssh = self._cp.remove_connection(dir_obj)

    ######################################################################
    ## 
    def dir_list(self, dir_obj):
        
        complete_path = dir_obj._url.path

        # LOCAL FILESYSTEM
        if dir_obj.is_local:
            return os.listdir(complete_path)

        # REMOTE FILESYSTEM VIA SFTP
        else:
            try:
                self.log_info("Trying to LSDIR '%s'" % (complete_path))
                ssh = self._cp.get_connection(dir_obj)
                sftp = ssh.open_sftp()
                return sftp.listdir(complete_path)
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                 "Couldn't list directory: %s " % (str(ex)))

    def _rmtree(self, sftp, path):
        from stat import S_ISDIR
        '''Recursively delete contents of remote path'''
        
        for attr in sftp.listdir_attr(path):
            fullname = '%s/%s' % (path, attr.filename)
            if S_ISDIR(attr.st_mode):
                self._rmtree(sftp, fullname)
                self.log_info("Trying to RMDIR '%s'" % (fullname))
                sftp.rmdir(fullname)
            else:
                self.log_info("Trying to RM '%s'" % (fullname))
                sftp.remove(fullname)                


    ######################################################################
    ## 
    def dir_remove(self, dir_obj, path):
        if path != None:
            complete_path = os.path.join(dir_obj._url.path, path)
        else:
            complete_path = dir_obj._url.path

        # LOCAL FILESYSTEM
        if dir_obj.is_local:
            from shutil import rmtree
            return rmtree(complete_path)

        # REMOTE FILESYSTEM VIA SFTP
        else:
            try:
                self.log_info("Trying to (recursively) RMDIR '%s'" % (complete_path))
                ssh = self._cp.get_connection(dir_obj)
                sftp = ssh.open_sftp()
                self._rmtree(sftp, complete_path)
                sftp.rmdir(complete_path)
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                 "Couldn't remove directory: %s " % (str(ex)))

    ######################################################################
    ## 
    def dir_get_size(self, dir_obj, path):
        '''Implements interface from FilesystemPluginInterface
        '''
        if path != None:
            complete_path = os.path.join(dir_obj._url.path, path)
        else:
            complete_path = dir_obj._url.path

        # LOCAL FILESYSTEM
        if dir_obj.is_local:
            return os.path.getsize(complete_path)

        # REMOTE FILESYSTEM VIA SFTP
        else:
            try:
                stat = self.entry_getstat(dir_obj, complete_path)
                return stat.st_size    
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't determine size for '%s': %s " % (complete_path, (str(ex))))

    ######################################################################
    ## 
    def file_get_size(self, file_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        complete_path = file_obj._url.path

        # LOCAL FILESYSTEM
        if file_obj.is_local:
            return os.path.getsize(complete_path)

        # REMOTE FILESYSTEM VIA SFTP
        else:
            try:
                stat = self.entry_getstat(file_obj, complete_path)
                return stat.st_size    
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't determine size for '%s': %s " % (complete_path, (str(ex))))

    ######################################################################
    ## 
    def dir_open_dir(self, dir_obj, path, flags):
        '''Implements interface from FilesystemPluginInterface
        '''
        if path != None:
            complete_path = os.path.join(dir_obj._url.path, path)
        else:
            complete_path = dir_obj._url.path

        url = bliss.saga.Url(dir_obj._url)
        url.path = complete_path

        return bliss.saga.filesystem.Directory(url, flags)    

    ######################################################################
    ## 
    def dir_make_dir(self, dir_obj, path, flags):
        '''Implements interface from FilesystemPluginInterface
        '''
        complete_path = os.path.join(dir_obj._url.path, path)

        # LOCAL FILESYSTEM
        if dir_obj.is_local:
            if os.path.exists(complete_path):
                if flags & bliss.saga.filesystem.Overwrite:
                    pass # do nothing
                else:
                    self.log_error_and_raise(bliss.saga.Error.AlreadyExists, 
                    "Couldn't create directory '%s'. Entry already exist." % (complete_path))
            else:
                os.mkdir(complete_path)

        # REMOTE FILESYSTEM VIA SFTP
        else:
            # throw exception if directory already exists
            stat = self.entry_getstat(dir_obj, path)
            if stat != None:
                if flags & bliss.saga.filesystem.Overwrite:
                    pass # do nothing
                else:            
                    self.log_error_and_raise(bliss.saga.Error.AlreadyExists, 
                    "Couldn't create directory '%s'. Entry already exist." % (complete_path))

            try:
                ssh = self._cp.get_connection(dir_obj)
                sftp = ssh.open_sftp()
                sftp.mkdir(complete_path)
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                 "Couldn't create directory '%s': %s " % (complete_path, str(ex)))

    ######################################################################
    ## 
    def file_copy(self, file_obj, target):
        '''Implements interface from FilesystemPluginInterface
        '''
        surl = file_obj._url
        turl = bliss.saga.Url(target)
      
        # remote -> local copy 
        # we allow the following operations:
        # sftp://host/file -> sftp://localhost/dir/(file)
        # sftp://host/file -> sftp://localhost/dir/(file) 
        # sftp://host/file -> sftp:///dir/(file)

        if surl.host != 'localhost' and surl.host != None:
            if (turl.scheme == 'sftp' and turl.host == 'localhost') or \
               (turl.scheme == 'sftp' and turl.host == None):
                
                dest = '.'
                sftp_get_target = ''
                if turl.path != None: 
                    dest = turl.path
                if os.path.exists(dest):
                    if os.path.isdir(dest) == True:
                        # copy to existing directory
                        name = os.path.basename(surl.path)
                        path = os.path.dirname(dest)
                        sftp_get_target = os.path.join(path, name)
                        self.log_info("Trying to copy remote file '%s' into local dir '%s' as file '%s'" % (surl, path, name))
                    else:
                        # target file exists. 'Overwrite' flag must be set
                        name = os.path.basename(dest)
                        path = os.path.dirname(dest)
                        sftp_get_target = os.path.join(path, name)
                        self.log_info("Trying to copy remote file '%s' to local dir '%s' as file '%s'" % (surl, path, name))
                else:
                    if os.path.basename(turl.path) != '':
                        name = os.path.basename(turl.path)
                    else:
                        name = os.path.basename(surl.path)
                    path = os.path.dirname(dest)
                    sftp_get_target = os.path.join(path, name)
                    self.log_info("Trying to copy remote file '%s' to local dir '%s' as file '%s'" % (surl, path, name))
                    if os.path.exists(os.path.dirname(dest)) != True:
                        self.log_error_and_raise(bliss.saga.Error.BadParameter, 
                          "Can't copy remote file '%s' to non-existing local directory '%s'." % (surl, path))

            else:
                self.log_error_and_raise(bliss.saga.Error.BadParameter, 
                 "Can't copy remote file '%s' to non-local location '%s'." % (surl, turl))

            # At this point we're good to execute the remote -> local copy operation
            try:
                ssh = self._cp.get_connection(file_obj)
                sftp = ssh.open_sftp()
                sftp.get(surl.path, sftp_get_target)
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                 "Couldn't copy file '%s' to '%s': %s " % (surl, turl, str(ex)))

        # local -> remote copy
        # we allow the following operations:
        # sftp://localhost/file -> sftp://host/dir/(file)
        # sftp:////file -> sftp://localhost/dir/ (remote -> local copy)

        else:
            # we know that the source path exists, however, we don't have
            # a connection to the target server yet, since the object 
            # was constructed with a 'local' URL. We need to do that manually

            sftp_put_source = surl.path
            sftp_put_target = turl.path
            if os.path.basename(turl.path) == '':
                sftp_put_target = os.path.join(sftp_put_target, os.path.basename(sftp_put_source))

            hostname = turl.host
            if turl.port != None:
                port = turl.port
            else:
                port = 22
            if turl.username != None:
                username = turl.username
            else:
                username = pwd.getpwuid(os.getuid()).pw_name

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
                ssh.connect(hostname=hostname, port=int(port), username=username, allow_agent=True, look_for_keys=True)
                sftp = ssh.open_sftp()
                self.log_info("Trying to PUT '%s' -> '%s'" % (sftp_put_source, sftp_put_target))
                sftp.put(sftp_put_source, sftp_put_target)
                sftp.close()
            except Exception, ex:
                self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                 "Couldn't copy file '%s' to '%s': %s " % (surl, turl, str(ex)))




    ######################################################################
    ## 
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




