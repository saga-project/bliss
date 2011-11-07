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

from openssh_wrapper import SSHConnection

class PBSSHCmdLineWrapper():
    '''A wrapper around the PBS command line tools via SSH'''

    __slots__ = {'prochandle', '_jd', '_plugin', 'returncode', 
                 'pid', 'state' }

    def __init__(self, jobdescription, contexts, plugin):
        '''Constructor'''
        self._jd = jobdescription
        self._plugin = plugin
        
        self.prochandle = None
        self.pid = None
        self.returncode = None
        self.state = bliss.saga.job.Job.New

    ######################################################################
    ##
    def _pbscript_generator(self, jd):
        '''Generates a PBS script from a SAGA job description.
        '''
        pbs_params = str()
        exec_n_args = str()

        if jd.executable is not None:
            exec_n_args += "%s " % (jd.executable) 
        if jd.arguments is not None:
            for arg in jd.arguments:
                exec_n_args += "%s " (arg)

        pbs_params += "#PBS -N %s \n" % "bliss_job" 
             
        if jd.output is not None:
            pbs_params += "#PBS -o %s \n" % jd.output
        if jd.error is not None:
            pbs_params += "#PBS -e %s \n" % jd.error 

        pbscript = "\n#!/bin/bash \n%s \n%s" % (pbs_params, exec_n_args)
        self._plugin.log_info("Generated PBS script: %s" % (pbscript))
        return pbscript

    def _execute_globusrun(self):
        cmdline = "/opt/globus-5.0.4//bin/globusrun"
        print self._rsl_generator(self._jd) 
        try:
            (out, err) = subprocess.Popen(cmdline, 
                                          stderr=subprocess.PIPE, 
                                          stdout=subprocess.PIPE).communicate()
            print "out %s" % out
            print "err %s" % err
        except Exception, ex:
            print "SNAP"
        
        

    def run(self):
        if self._jd.arguments is not None:
             cmdline = copy.deepcopy(self._jd.arguments)
        else:
             cmdline = []
        cmdline.insert(0, self._jd.executable)


        self._pbscript_generator(self._jd)

        self.prochandle = subprocess.Popen(cmdline, 
                                           executable=self._jd.executable,
                                           stderr=subprocess.STDOUT, 
                                           stdout=subprocess.PIPE, 
                                           env=self._jd.environment)
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
    
