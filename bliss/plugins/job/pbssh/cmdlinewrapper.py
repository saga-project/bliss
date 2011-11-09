#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import copy
import time
import string
import subprocess
import bliss.saga

from bliss.plugins.utils import CommandWrapper

def pbs_to_saga_jobstate(pbsjs):
    '''translates a pbs one-letter state to saga'''
    if pbsjs == 'C':
        return bliss.saga.job.Job.Done
    elif pbsjs == 'E':
        return bliss.saga.job.Job.Running
    elif pbsjs == 'H':
        return bliss.saga.job.Job.Waiting
    elif pbsjs == 'Q':
        return bliss.saga.job.Job.Waiting
    elif pbsjs == 'R':
        return bliss.saga.job.Job.Running 
    elif pbsjs == 'T': 
        return bliss.saga.job.Job.Running 
    elif pbsjs == 'W':
        return bliss.saga.job.Job.Waiting
    elif pbsjs == 'S':
        return bliss.saga.job.Job.Waiting
    else:
        return bliss.saga.job.Job.Unknown

##############################################################################
##
class PBSJobInfo():
    '''Encapsulates a PBS job'''
    ##########################################################################
    ##
    def __init__(self, qstat_string):
        '''Initialize from qstat string'''
        cols= qstat_string.split()
        self.jobid    = cols[0]
        self.user     = cols[2]
        self.queue    = cols[5]
        self.name     = cols[1]
        self.state    = pbs_to_saga_jobstate(cols[4])

    Canceled = "Canceled"
    '''Indicates that the job has been canceled either by the user or the system'''
    Done     = "Done"
    '''Indicates that the job has successfully executed''' 
    Failed   = "Failed"
    '''Indicates that the execution of the job has failed'''
    New      = "New"
    '''Indicates that the job hasn't been started yet'''
    Running  = "Running"
    '''Indicates that the job is executing'''
    Waiting  = "Waiting"
    '''Indicates that the job is waiting to be executed (NOT IN GFD.90)'''
    Unknown  = "Unknown"
    '''Indicates that the job is in an unexpected state'''


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
        if self._url.scheme == "pbs":
            if self._url.host != "localhost":
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Can't use %s as hostname in conjunction with pbs:// schema. Try pbs+ssh:// instead" \
                  % (self._url.host))

        self._known_jobs = dict()

    def _known_jobs_update(self, native_jobid, job_info):
        self._known_jobs[native_jobid] = job_info

    def _known_jobs_remove(self, native_jobid):
        self._known_jobs.remove(native_jobid)

    def _known_jobs_exists(self, native_jobid):
        if native_jobid in self._known_jobs:
            return True
        else: 
            return False

    def _known_jobs_is_done(self, native_jobid):
        if self._known_jobs[native_jobid].state == bliss.saga.job.Job.Done:
            return True
        else:
            return False
 
    ##########################################################################
    ##  
    def _check_context(self): 
        '''sets self._cw to a usable access configuration or throws'''
        
        # see if we run stuff on the local machine 
        if self._url.scheme == "pbs":
            self._use_ssh = False
            cw = CommandWrapper(via_ssh=False)
            result = cw.run("pbs-config", ["--version"])
            if result.returncode != 0:
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't find PBS tools on %s" % (self._url))
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
                            self._cw = cw
                            self._pi.log_info("Using context %s to access %s succeeded" % (ctx, self._url))
                            break
                    except Exception, ex:
                        self._pi.log_warning("Using context %s to access %s failed because: %s" \
                          % (ctx, self._url, result.error))

            if usable_ctx is None:
                # see if we can use system defaults to run
                # stuff via ssh
                cw = CommandWrapper(ssh_hostname=self._url.host, via_ssh=True)
                result = cw.run("true")
                if result.returncode != 0:
                    self._pi.log_warning("Using no context %s to access %s failed because: %s" \
                      % (ctx, self._url, result.error))
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
                self._pi.log_error_and_raise("11", "Couldn't find PBS command line tools on %s: %s" \
                  % (self._url, result.stderr))
            else:
                self._pi.log_info("Found PBS command line tools on %s. Version: %s" \
                  % (self._url, result.stdout))


    ######################################################################
    ##
    def list_jobs(self):
        '''Return the jobs known to qstat'''
        jobids = []
        if self._cw == None:
            self._check_context()
        
        result = self._cw.run("qstat")
        lines = result.stdout.splitlines(True)
        for line in lines[2:]:
            jobinfo = PBSJobInfo(line)
            self._known_jobs_update(jobinfo.jobid, jobinfo)
            jobids.append(bliss.saga.job.JobID(self._url, jobinfo.jobid))
        return jobids


    ######################################################################
    ##
    def get_jobinfo(self, saga_jobid):
        '''Returns a running PBS job as saga object'''
        if self._cw == None:
            self._check_context()

        if self._known_jobs_exists(saga_jobid.native_id):
            if self._known_jobs_is_done(saga_jobid.native_id):
                return self._known_jobs[saga_jobid.native_id]


        result = self._cw.run("qstat %s" % (saga_jobid.native_id))
        lines = result.stdout.split("\n")
        if len(lines) != 3:
            # if we don't get any return value, but the job
            # is known, it must be in 'done' state
            if self._known_jobs_exists(saga_jobid.native_id):
                jobinfo = self._known_jobs[saga_jobid.native_id]
                jobinfo.status = bliss.saga.job.Job.Done
                return jobinfo
            else:
                self._pi.log_error_and_raise(bliss.saga.Error.DoesNotExist, 
                "Job with ID '%s' doesn't exist (anymore)" % saga_jobid)

        jobinfo = PBSJobInfo(lines[2])
        self._known_jobs_update(jobinfo.jobid, jobinfo)

        return jobinfo


    ######################################################################
    ##
    def get_job_state(self, saga_jobid):
        '''Returns the state of the job with the given jobid'''
        return self.get_jobinfo(saga_jobid).state


class PBSSHCmdLineWrapper(object):
    '''A wrapper around the PBS command line tools via SSH'''

    #__slots__ = {'prochandle', '_jd', '_plugin', 'returncode', 
    #             'pid', 'state' }

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
    
