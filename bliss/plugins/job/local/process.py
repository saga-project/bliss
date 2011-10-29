#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import copy
import subprocess
import bliss.saga.job


class LocalJobProcess():
    '''A wrapper around a subprocess'''

    def __init__(self, executable, arguments, environment):
        self.executable = executable
        self.arguments = arguments
        self.environment = environment
        
        self.prochandle = None
        self.pid = None
        self.state = bliss.saga.job.Job.New
        

    def run(self):
        cmdline = copy.deepcopy(self.arguments)
        cmdline.insert(0, self.executable)
        self.prochandle = subprocess.Popen(cmdline, 
                                           executable=self.executable,
                                           stderr=subprocess.STDOUT, 
                                           stdout=subprocess.PIPE, 
                                           env=self.environment)
        self.pid = self.prochandle.pid
        self.state = bliss.saga.job.Job.Running

    def getpid(self):
        return self.pid

    def getstate(self):
        if self.state == bliss.saga.job.Job.Running:
            # only update if still running 
            rc = self.prochandle.poll() 
            if rc is not None:
                if rc != 0:
                    self.state = bliss.saga.job.Job.Failed
                else:
                    self.state = bliss.saga.job.Job.Done

        return self.state

    def terminate(self):
        self.prochandle.terminate()
        self.state = bliss.saga.job.Job.Canceled


    def wait(self):
        self.prochandle.wait()
    
