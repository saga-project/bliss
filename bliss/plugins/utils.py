# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import traceback
import StringIO

from openssh_wrapper import SSHConnection

def get_traceback(prefix="\n*** "):
    '''returns the last traceback as a string with a given prefix'''
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    if fp.getvalue() == "None\n":
        return "(No Traceback)"
    else:
        return prefix+fp.getvalue() 


class CommandWrapper(object):
    '''This class represent a wrapper for arbitrary commands.
       It can either execute them local or via ssh.
    '''

    ######################################################################
    ##
    def __init__(self, logger, via_ssh=None, ssh_username=None, 
                 ssh_hostname=None, ssh_key=None):
        '''Constructor'''
        self._via_ssh = via_ssh
        self._ssh_username = ssh_username
        self._ssh_hostname = ssh_hostname
        self._ssh_key = ssh_key

        self._output = None
        self._error = None
        self._returncode = None

        if self._via_ssh is True:
            if self._ssh_hostname is None:
                raise Exception("No hostname defined")  
          
            self._ssh_connection = SSHConnection(server=self._ssh_hostname, 
                                                 identity_file=self._ssh_key,
                                                 login=self._ssh_username)

    def run(self, executable, arguments):
        '''Runs a command (blocking)'''
        self._output = None
        self._error = None
        self._returncode = None

        if self._via_ssh is True:
            cmd = executable
            for arg in arguments:
                cmd += " %s " % (arg)
            result = self._ssh_connection.run(cmd)
            self._output = result.output
            self._error = result.error
            self._returncode = result.returncode

        else:
            pass #popen.communicate()

    ######################################################################
    ## Property
    def stdoutput():
        def fget(self):
            return self._output
        return locals()
    stdoutput = property(**stdoutput())

    ######################################################################
    ## Property
    def stderror():
        def fget(self):
            return self._error
        return locals()
    stderror = property(**stderror())

    ######################################################################
    ## Property
    def returncode():
        def fget(self):
            return self._returncode
        return locals()
    returncode = property(**returncode())
