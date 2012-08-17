# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import subprocess
from time import sleep
from sshconnection import SSHConnection, SSHConnectionException

class CommandWrapperException(Exception):
    '''Raised for CommandWrapper exceptions.
    '''

class CommandWrapper(object):
    '''This class represent a wrapper for arbitrary commands.
       It can either execute them locally or via ssh.
    '''

    @classmethod
    def initAsLocalWrapper(self, logger):
        cw = CommandWrapper(logger)
        cw._mode = 'local'
        cw._is_connected = False # for consistency 
        return cw

    @classmethod
    def initAsSSHWrapper(self, logger, hostname, port=22, username='', password='', userkey=''):
        cw = CommandWrapper(logger)
        cw._mode = 'ssh'
        cw.hostname = hostname
        cw.port = port
        cw.username = username
        cw.password = password
        cw.userkey = userkey
        cw._is_connected = False
        return cw

    @classmethod
    def initAsGSISSHWrapper(self, logger, hostname, port=22, username='', password='', x509_userproxy=''):
        cw = CommandWrapper(logger)
        cw._mode = 'gsissh'
        cw.hostname = hostname
        cw.port = port
        cw.username = username
        cw.password = password
        cw.x509_userproxy = x509_userproxy
        cw._is_connected = False
        return cw

    ######################################################################
    ##
    def __init__(self, logger):
        '''Constructor'''
        self._logger = logger

        # connection tracker
        self._ssh_was_connected = False

     
    ######################################################################
    ##
    def __del__(self): 
        self.disconnect()

    ######################################################################
    ##
    def connect(self):
        '''Connect'''
        if self._mode == 'local':
            self._is_connected = True

        elif self._mode == 'ssh':
            if self.hostname is None:
                raise CommandWrapperException("No hostname defined")  
            #self._logger.log_info('Trying to establish SSH connection with: %s' % cw.hostname)
            try:
                self._connection = SSHConnection(gsissh=False)
                self._connection.login(hostname=self.hostname, port=self.port,
                                       username=self.username, password=self.password)
                self._is_connected = True
            except SSHConnectionException, e:
                raise CommandWrapperException(str(e))

        elif self._mode == 'gsissh':
            if self.hostname is None:
                raise CommandWrapperException("No hostname defined")  
            #self._pi.log_info('Trying to establish GSISSH connection with: %s' % cw.hostname)
            try:
                self._connection = SSHConnection(gsissh=True)
                self._connection.login(hostname=self.hostname, port=self.port,
                                       username=self.username, password=self.password)
                self._is_connected = True
            except SSHConnectionException, e:
                raise CommandWrapperException(str(e))



    ######################################################################
    ##
    def disconnect(self):
        '''Disconnect'''
        if self._mode == 'local':
            pass
        elif self._mode == 'ssh':
            if self._is_connected:
                self._connection.logout()
        elif self._mode == 'gsissh':
            if self._is_connected:
                self._connection.logout()



    ######################################################################
    ##
    def run(self, executable, arguments=[]):
        '''Runs a command (blocking)'''

        if not self._is_connected:
            raise CommandWrapperException("Command wrapper is not connected")

        cmd = executable
        for arg in arguments:
            cmd += " %s " % (arg)

        if self._mode == 'local':
            job_error = None
            job_output = None
            returncode = None

            pid = subprocess.Popen(cmd, shell=True, 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.STDOUT)
            out, err = pid.communicate() 
            cwr = CommandWrapperResult(command=cmd,
                                       stdout=out,
                                       returncode=pid.returncode)
            return cwr                
            
        elif self._mode == 'ssh' or self._mode == 'gsissh':
            
            try:
                result = self._connection.execute(cmd)
                cwr = CommandWrapperResult(command=cmd,
                                           stdout=result['output'],
                                           returncode=result['exitcode'])
                return cwr
            except SSHConnectionException, e:
                raise CommandWrapperException(str(e))



        # run a command via SSH
#        if self._via_ssh is True:
#            try:
#                result = self._ssh_connection.run(cmd)
#                cwr = CommandWrapperResult(command=cmd,
#                                           stdout=result.stdout,
#                                           stderr=result.stderr,
#                                           returncode=result.returncode)
#                self._ssh_was_connected = True
#                return cwr 
#
#            except SSHError, ex:
#                # Try to reconnect once. This makes sense in case the
#                # connection has timed out
#                if self._ssh_was_connected is True:
#                    try:
#                        # just wait a bit before we re-connect. 
#                        self._pi.log_warning("Conection problems: %s" % str(ex))
#                        self._pi.log_warning("Trying to re-connect to %s" % self._ssh_hostname)
#
#                        sleep(10) 
#                        self._ssh_connection = SSHConnection(server=self._ssh_hostname, 
#                                                             identity_file=self._ssh_key,
#                                                             login=self._ssh_username)
#                        result = self._ssh_connection.run(cmd)
#                        cwr = CommandWrapperResult(command=cmd,
#                                                   stdout=result.stdout,
#                                                   stderr=result.stderr,
#                                                   returncode=result.returncode)
#                        return cwr  
#                    except SSHError, ex:
#                        raise ex #Exception("Re-connection failed")
#                else:
                 #   raise

class CommandWrapperResult(object):
    '''Represents a result.
    '''

    ######################################################################
    ##
    def __init__(self, command, stdout=None, returncode=None):
        self.command = command
        self.stdout = stdout
        self.returncode = returncode

    ######################################################################
    ##
    def __str__(self):
        return unicode(self).decode('utf-8', 'ignore')

    ######################################################################
    ##
    def __unicode__(self):
        ret = []
        ret.append(u'command: %s' % unicode(self.command))
        ret.append(u'stdout: %s' % unicode(self.stdout))
        ret.append(u'returncode: %s' % unicode(self.returncode))
        return u'\n'.join(ret)

