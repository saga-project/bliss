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

################################################################################
################################################################################

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

################################################################################
################################################################################

class PBSJobInfo(object):
    '''Encapsulates infos about a PBS job as returned by qstat -f1.'''

    def __init__(self, qstat_f_output, plugin):
        '''Constructor: initialize from qstat -f <jobid> string.
        '''
        
        plugin.log_debug("Got raw qstat output: %s" % qstat_f_output) 
        lines = qstat_f_output.split("\n")
        self._jobid = lines[0].split(":")[1].strip()

        for line in lines[1:]:
            try: 
                (key, value) = line.split(" = ")
                key = "_%s" % key.strip()
                self.__dict__[key] = value
            except Exception, ex:
                pass
        plugin.log_debug("Parsed qstat output: %s" % str(self.__dict__))


    @property 
    def state(self):
        return pbs_to_saga_jobstate(self._job_state)

    @property 
    def jobid(self):
        return self._jobid

    @property 
    def walltime_limit(self):
        return self._Resource_List.walltime

    @property 
    def output_path(self):
        return self._Output_Path

    @property 
    def error_path(self):
        return self._Error_Path

    @property 
    def queue(self):
        return self._queue

    @property 
    def exitcode(self):
        if '_exit_status' in self.__dict__:
            return self._exit_status
        else:
            return None


################################################################################
################################################################################

class PBSService():
    '''Encapsulates PBS command line tools.
    '''

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
 
    ######################################################################
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
                            self._pi.log_info("Using context %s to access %s succeeded" \
                              % (ctx, self._url))
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
        
        result = self._cw.run("qstat -f1")
        if result.returncode != 0:
            raise Exception("Error running 'qstat': %s" % result.stderr)

        lines = result.stdout.split("\n\n")
        for line in lines:
            jobinfo = PBSJobInfo(line, self._pi)
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


        result = self._cw.run("qstat -f1 %s" % (saga_jobid.native_id))
        if result.returncode != 0:
            if self._known_jobs_exists(saga_jobid.native_id):
                ## if the job is on record but can't be reached anymore,
                ## this probablty means that it has finished and already
                ## kicked out qstat. in that case we just set it's state 
                ## to done.
                jobinfo = self._known_jobs[saga_jobid.native_id]
                jobinfo._job_state = 'C' # PBS 'Complete'
                return jobinfo
            else:
                ## something went wrong.
                raise Exception("Error running 'qstat': %s" % result.stderr)

        jobinfo = PBSJobInfo(result.stdout, self._pi)
        self._known_jobs_update(jobinfo.jobid, jobinfo)

        return jobinfo


    ######################################################################
    ##
    def get_job_state(self, saga_jobid):
        '''Returns the state of the job with the given jobid.
        '''
        return self.get_jobinfo(saga_jobid).state


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
                exec_n_args += "%s " % (arg)

        pbs_params += "#PBS -N %s \n" % "bliss_job" 
             
        if jd.output is not None:
            pbs_params += "#PBS -o %s \n" % jd.output
        if jd.error is not None:
            pbs_params += "#PBS -e %s \n" % jd.error 
        if jd.working_directory is not None:
            pbs_params += "#PBS -d %s \n" % jd.working_directory
        if jd.walltime_limit is not None:
            pbs_params += "#PBS -l walltime=%s \n" % jd.walltime_limit
        if jd.queue is not None:
            pbs_params += "#PBS -q %s \n" % jd.queue
        if jd.project is not None:
            pbs_params += "#PBS -A %s \n" % jd.project[0]

        pbscript = "\n#!/bin/bash \n%s \n%s" % (pbs_params, exec_n_args)
        self._pi.log_info("Generated PBS script: %s" % (pbscript))
        return pbscript


    ######################################################################
    ##
    def submit_job(self, job):
        '''Submits a job to PBS and returns a jobinfo structure.
        '''
        if self._cw == None:
            self._check_context()

        script = self._pbscript_generator(job.get_description())
        result = self._cw.run("echo '%s' | qsub" % (script))
 
        if result.returncode != 0:
            self._pi.log_error("Error running 'qstat': %s" % result.stderr)
            raise Exception("blah")
        else:
            jobinfo = self.get_jobinfo(bliss.saga.job.JobID(self._url, 
              result.stdout.split("\n")[0]))
            return jobinfo

#    def terminate(self):
#        self.prochandle.terminate()
#        self.state = bliss.saga.job.Job.Canceled
#
#
#    def wait(self, timeout):
#        if timeout == -1:
#            self.returncode = self.prochandle.wait()
#        else:
#            t_beginning = time.time()
#            seconds_passed = 0
#            while True:
#                self.returncode = self.prochandle.poll()
#                if self.returncode is not None:
         #           break
               # seconds_passed = time.time() - t_beginning
               # if timeout and seconds_passed > timeout:
               #     break
               # time.sleep(0.1)
#
#    def get_exitcode(self):
#        return self.returncode
    
