#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import os.path
import copy
import time
import subprocess
import bliss.saga

from bliss.utils import which

class LocalJobProcess(object):
    '''A wrapper around a subprocess'''

#    __slots__ = {'prochandle', 'executable', 'arguments', 
#                 'environment', 'returncode', 'pid', 'state',
#                 't_created', 't_started', 't_finished'}

    def __init__(self, jobdescription, plugin):
        self.executable  = jobdescription.executable
        self.arguments   = jobdescription.arguments
        self.environment = jobdescription.environment
        self.cwd         = jobdescription.working_directory
        
        self.prochandle = None
        self.pid = None
        self.returncode = None
        self.state = bliss.saga.job.Job.New
        self.pi = plugin
        
        self.number_of_processes = 1
        self.use_mpirun = False

    def __del__(self):
        if self._job_output is not None:
            self._job_output.close()
        if self._job_error is not None:
            self._job_error.close()


    def run(self, jd):
        if jd.output is not None:
            if os.path.isabs(jd.output):
                self._job_output = open(jd.output,"w")  
            else:
                if self.cwd is not None:
                    self._job_output = open(os.path.join(self.cwd, jd.output),"w")
                else:
                    self._job_output = open(jd.output,"w")  
        else:
            self._job_output = None 

        if jd.error is not None:
            if os.path.isabs(jd.error):
                self._job_error = open(jd.error,"w")  
            else:
                if self.cwd is not None:
                    self._job_error = open(os.path.join(self.cwd, jd.error),"w")
                else:
                    self._job_error = open(jd.error,"w") 
        else:
            self._job_error = None

        if jd.spmd_variation is not None:
            if jd.spmd_variation == "MPI":
                if jd.number_of_processes is not None:
                    self.number_of_processes = jd.number_of_processes
                    self.use_mpirun = True
                self.pi.log_info("SPMDVariation=%s requested. Job will execute via 'mpirun -np %d'." % (jd.spmd_variation, self.number_of_processes))
            else:
                self.pi.log_info("SPMDVariation=%s: unknown SPMD variation. Ignoring." % jd.spmd_variation)

        # check if executable exists.
        if which(self.executable) == None:
            self.pi.log_error_and_raise(bliss.saga.Error.BadParameter, 
            "Executable doesn't exist: %s" % self.executable)        
            

        if self.use_mpirun is True:
            mpirun = which('mpirun')
            if mpirun == None:
                self.pi.log_error_and_raise(bliss.saga.Error.BadParameter, 
                "Can't find 'mpirun' in path.")        
            else:
                cmdline = '%s -np %d %s' % (mpirun, self.number_of_processes, str(self.executable))
        else:
            cmdline = str(self.executable)
        args = ""
        if self.arguments is not None:
            for arg in self.arguments:
                cmdline += " %s" % arg 

        self.pi.log_info("Trying to run: %s" % cmdline) 
 
        self.prochandle = subprocess.Popen(cmdline, shell=True, 
                                           #executable=self.executable,
                                           stderr=self._job_error, 
                                           stdout=self._job_output, 
                                           env=self.environment,
                                           cwd=self.cwd)

        self.pid = self.prochandle.pid
        self.state = bliss.saga.job.Job.Running

    def getpid(self, serviceurl):
        if self.pid == None:
            return None
        else:
            return bliss.utils.jobid.JobID(serviceurl, self.pid)

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

    
