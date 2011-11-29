#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.interface import FilesystemPluginInterface

from bliss.plugins import utils

import os
import time
import paramiko
import bliss.saga

################################################################################
################################################################################

class SSHFilesystemPlugin(FilesystemPluginInterface):
    '''Implements a filesystem plugin that does things via SSH
    '''
    ## Define adaptor name. Convention is:
    ##         saga.plugin.<package>.<name>
    _name = 'saga.plugin.file.ssh'

    ## Define supported url schemas
    ## 
    _schemas = ['ssh']

    ## Define apis supported by this adaptor
    ##
    _apis = ['saga.filesystem']


    ######################################################################
    ##
    def __init__(self, url):
        '''Class constructor'''
        FilesystemPluginInterface.__init__(self, name=self._name, schemas=self._schemas)

    ######################################################################
    ##
    @classmethod
    def sanity_check(self):
        '''Implements interface from PluginBaseInterface
        '''
        try:
            import paramiko
        except Exception, ex:
            raise Exception("paramiko module missing")
 

    def register_file_object(self, service_obj):
        '''Implements interface from FilesystemPluginInterface
        '''
        host = service_obj._url.host
        port = int(service_obj._url.port)

        usable_ctx = None
        for ctx in service_obj.session.contexts:
            if ctx.type is bliss.saga.Context.SSH:
                print "found ssh context: %s" % str(ctx)
                usable_ctx = ctx
                break

        try:
            #privkey = paramiko.RSAKey.from_private_key_file (usable_ctx.usercert)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            ssh.connect(hostname=host, username=usable_ctx.userid, allow_agent=True, look_for_keys=True)
            sftp = ssh.open_sftp()
            print sftp.listdir()

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls /tmp')
            print ssh_stdout.read()

            sftp.close()
            ssh.close()




        except Exception, ex:
            self.log_error_and_raise(bliss.saga.Error.NoSuccess, 
              "Couldn't create new file object because: %s " % (str(ex)))
            

    def unregister_file_object(self, service_obj):
        '''Implements interface from FilesystemPluginInterface
        '''


        

