#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import copy
import time
import subprocess
import bliss.saga


class GRAMCmdLineWrapper():
    '''A wrapper around the globus tools'''

    __slots__ = {'prochandle', 'executable', 'arguments', 
                 'environment', 'returncode', 'pid', 'state',
                 't_created', 't_started', 't_finished'}

    def __init__(self, executable, arguments, environment):
        self.executable = executable
        self.arguments = arguments
        self.environment = environment
        
        self.prochandle = None
        self.pid = None
        self.returncode = None
        self.state = bliss.saga.job.Job.New

    def _execute_globusrun(self):
        cmdline = "/opt/globus-5.0.4//bin/globusrun"
        try:
            (out, err) = subprocess.Popen(cmdline, 
                                          stderr=subprocess.PIPE, 
                                          stdout=subprocess.PIPE).communicate()
            print "out %s" % out
            print "err %s" % err
        except Exception, ex:
            print "SNAP"
        
        

    def run(self):
        cmdline = copy.deepcopy(self.arguments)
        cmdline.insert(0, self.executable)


        self._execute_globusrun()

        self.prochandle = subprocess.Popen(cmdline, 
                                           #executable=self.executable,
                                           stderr=subprocess.STDOUT, 
                                           stdout=subprocess.PIPE, 
                                           env=self.environment)
        self.pid = self.prochandle.pid
        self.state = bliss.saga.job.Job.Running

    def getpid(self, serviceurl):
        return "[%s]-[%s]" % (serviceurl, self.pid)

    def getstate(self):
        if self.state == bliss.saga.job.Job.Running:
            # only update if still running 
            self.returncode = self.prochandle.poll() 
            if self.returncode is not None:
                if self.returncode != 0:
                    self.state = bliss.saga.job.Job.Failed
                else:
                    self.state = bliss.saga.job.Job.Done

        return self.state

    def terminate(self):
        self.prochandle.terminate()
        self.state = bliss.saga.job.Job.Canceled


    def wait(self, timeout):
        if timeout == -1:
            self.returncode = self.prochandle.wait()
        else:
            t_beginning = time.time()
            seconds_passed = 0
            while True:
                self.returncode = self.prochandle.poll()
                if self.returncode is not None:
                    break
                seconds_passed = time.time() - t_beginning
                if timeout and seconds_passed > timeout:
                    break
                time.sleep(0.1)

    def get_exitcode(self):
        return self.returncode
    
