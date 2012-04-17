# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import traceback
import StringIO
import subprocess

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
       It can either execute them locally or via ssh.
    '''

    ######################################################################
    ##
    def __init__(self, via_ssh=None, ssh_username=None, 
                 ssh_hostname=None, ssh_key=None):
        '''Constructor'''
        self._via_ssh = via_ssh
        self._ssh_username = ssh_username
        self._ssh_hostname = ssh_hostname
        self._ssh_key = ssh_key

        if self._via_ssh is True:
            if self._ssh_hostname is None:
                raise Exception("No hostname defined")  
          
            self._ssh_connection = SSHConnection(server=self._ssh_hostname, 
                                                 identity_file=self._ssh_key,
                                                 login=self._ssh_username)

    def run(self, executable, arguments=[]):
        '''Runs a command (blocking)'''
        cmd = executable
        for arg in arguments:
            cmd += " %s " % (arg)

        if self._via_ssh is True:
            result = self._ssh_connection.run(cmd)

            cwr = CommandWrapperResult(command=cmd,
                                       stdout=result.stdout,
                                       stderr=result.stderr,
                                       returncode=result.returncode)
            return cwr                
        else:
            job_error = None
            job_output = None
            returncode = None

            pid = subprocess.Popen(cmd, shell=True, 
                                      #executable=self.executable,
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
            out, err = pid.communicate() 

            cwr = CommandWrapperResult(command=cmd,
                                       stdout=out,
                                       stderr=err,
                                       returncode=pid.returncode)
            return cwr                


class CommandWrapperResult(object):
    '''Represents a result.
    '''
    def __init__(self, command, stdout=None, stderr=None, returncode=None):
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    def __str__(self):
        return unicode(self).decode('utf-8', 'ignore')

    def __unicode__(self):
        ret = []
        ret.append(u'command: %s' % unicode(self.command))
        ret.append(u'stdout: %s' % unicode(self.stdout))
        ret.append(u'stderr: %s' % unicode(self.stderr))
        ret.append(u'returncode: %s' % unicode(self.returncode))
        return u'\n'.join(ret)

