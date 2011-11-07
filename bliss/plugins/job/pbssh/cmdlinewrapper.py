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

from bliss.plugins.utils import CommandWrapper

##############################################################################
##
class PBSService():
    '''XX'''

    ##########################################################################
    ##
    def __init__(self, plugin, service_obj):
        '''Constructor'''
        self._pi = plugin
        self._so = service_obj
        self._url = service_obj._url
        self._cw = None

    ##########################################################################
    ##  
    def _check_context(self): 
        '''sets self._cw to a usable access configuration or throws'''
        
        # see if we run stuff on the local machine 
        if self._url.scheme == "pbs":
            if self._url.host != "localhost":
                self._pi.log_error_and_raise("11", "Can't use %s as hostname in conjunction with pbs:// schema. Try pbs+ssh:// instead" % (self._url.host))
            self._use_ssh = False
            cw = CommandWrapper(via_ssh=False)
            result = cw.run("pbs-config", ["--version"])
            if result.returncode != 0:
                raise Exception("Couldn't find PBS tools on %s" % (self._url))
            else:
                self._cw = cw

        elif self._url.scheme == "pbs+ssh":
            # iterate over all SSH contexts to see if one of them is
            # usable. we stop after we have found one.
            usable_ctx = None
            for ctx in self._so.session.contexts:
                if ctx.type is bliss.saga.Context.SSH:
                    try:
                        cw = CommandWrapper(via_ssh=True,
                                            ssh_username=ctx.userid, 
                                            ssh_hostname=self._url.host, 
                                            ssh_key=ctx.userkey)
                        result = cw.run("true")
                        if result.returncode == 0:
                            usable_ctx = ctx
                            self._pi.log_info("Using context %s to access %s succeeded" % (ctx, self._url))
                            break
                    except Exception, ex:
                        self._pi.log_warning("Using context %s to access %s failed because: %s" % (ctx, self._url, result.error))

            if usable_ctx is None:
                # see if we can use system defaults to run
                # stuff via ssh
                cw = CommandWrapper(ssh_hostname=self._url.host, via_ssh=True)
                result = cw.run("true")
                if result.returncode != 0:
                    self._pi.log_warning("Using no context %s to access %s failed because: %s" % (ctx, self._url, result.error))
                else:
                    self._cw = cw
                    self._pi.log_info("Using no context to access %s succeeded" % (self._url))

            if self._cw is None:
                # at this point, either self._cw contains a usable 
                # configuration, or the whole thing should go to shit
                self._pi.log_error_and_raise("11", "Couldn't find a way to access %s" % (self._url))
            
            # now let's see if we can find PBS
            result = self._cw.run("pbs-config --version")
            if result.returncode != 0:
                self._pi.log_error_and_raise("11", "Couldn't find PBS command line tools on %s: %s" % (self._url, result.stderr))
            else:
                self._pi.log_info("Found PBS command line tools on %s. Version: %s" % (self._url, result.stdout))


    def get_job_status(self, jobid):
        '''Return the job status according to pstat'''

    def list_jobs(self, jobid):
        '''Return the jobs known to qstat'''
        if self._cw == None:
            self._check_context


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


    def run(self):
        '''run the job using qsub'''
        cw = CommandWrapper()

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
    
