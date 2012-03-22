#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import copy
import time
import string
import subprocess
import bliss.saga

from bliss.plugins.utils import CommandWrapper

################################################################################
################################################################################

def sge_to_saga_jobstate(sgejs):
    '''translates a pbs one-letter state to saga'''
    if sgejs == 'C':
        return bliss.saga.job.Job.Done
    elif sgejs == 'E':
        return bliss.saga.job.Job.Running
    elif sgejs == 'H':
        return bliss.saga.job.Job.Waiting
    elif sgejs == 'Q':
        return bliss.saga.job.Job.Waiting
    elif sgejs == 'R':
        return bliss.saga.job.Job.Running 
    elif sgejs == 'T': 
        return bliss.saga.job.Job.Running 
    elif sgejs == 'W':
        return bliss.saga.job.Job.Waiting
    elif sgejs == 'S':
        return bliss.saga.job.Job.Waiting 
    elif sgejs == 'X':
        return bliss.saga.job.Job.Canceled
    else:
        return bliss.saga.job.Job.Unknown

################################################################################
################################################################################

class SGEServiceInfo(object):
    '''Encapsulates infos about a SGE cluster as returned by ??? .
    '''
    
    def __init__(self, qstat_a_output, pbsnodes_output, plugin):
        '''Constructure: initializa data from 'qstat -a' and 'pbsnodes'.
        '''
        self.GlueCEStateTotalJobs        = None
        self.GlueCEStateRunningJobs      = None
        self.GlueCEStateWaitingJobs      = None
        self.GlueCEStateFreeCPUs         = None

        self.GlueHostProcessorModel      = None
        self.GlueHostProcessorClockSpeed = None
        self.GlueHostMainMemoryRAMSize   = None

        self.GlueHostArchitectureSMPSize = None
        self.GlueSubClusterPhysicalCPUs  = None

        # from man qstat(1)
        # C -  Job is completed after having run/
        # E -  Job is exiting after having run.
        # H -  Job is held.
        # Q -  job is queued, eligible to run or routed.
        # R -  job is running.
        # T -  job is being moved to new location.
        # W -  job is waiting for its execution time
        #      (-a option) to be reached.

        jobs_running = 0
        jobs_waiting = 0


        # yye00 modified all of this
        lines = qstat_a_output.split("\n")
        for line in lines: 
            if line.find(" R ") != -1:
                jobs_running += 1
            elif line.find(" Q ") != -1:
                jobs_waiting += 1

        self.GlueCEStateRunningJobs = str(jobs_running)
        self.GlueCEStateWaitingJobs = str(jobs_waiting)
        self.GlueCEStateTotalJobs = str(jobs_running+jobs_waiting)

        # hack to work on lonestar
        self.GlueSubClusterPhysicalCPUs = "256"
        self.GlueCEStateFreeCPUs = "256"
        self.GlueHostArchitectureSMPSize = "12"


    def has_attribute(self, key):
        if self.__dict__[key] != None:
            return True
        else: 
            return False

    def get_attribute(self, key):
        return self.__dict__[key]

################################################################################
################################################################################

class SGEJobInfo(object):
    '''Encapsulates infos about a SGE job as returned by qstat -f1.
    '''

    def __init__(self, qstat_f_output, plugin):
        '''Constructor: initialize from qstat -f <jobid> string.
        '''
        
        plugin.log_debug("Got raw qstat output: %s" % qstat_f_output)
        if len(qstat_f_output) > 0:
            try:
                lines = qstat_f_output.split("\n")
                self._jobid = lines[0].split(":")[1].strip()
            except Exception, ex:
                raise Exception("Couldn't parse %s: %s" \
                  % (qstat_f_output, ex))

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
        return sge_to_saga_jobstate(self._job_state)

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

class SGEService:
    '''Encapsulates SGE command line tools.
    '''

    def __init__(self, plugin, service_obj):
        '''Constructor'''
        self._pi    = plugin
        self._so    = service_obj
        self._url   = service_obj._url
        self._cw    = None
        self._ppn   = 1 # number of processors per node. defaults to 1
        self._nodes = 1 # total number of nodes. defaults to 1

        if self._url.scheme == "sge":
            if self._url.host != "localhost":
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Can't use %s as hostname in conjunction with sge:// schema. Try sge+ssh:// instead" \
                  % (self._url.host))

        # Indicates when the service information was last updated
        # Service information is updated only every 10 seconds or 
        # so to avoid crazy network traffic 
        self._service_info_last_update = 0.0
        self._service_info = None
        
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

    def _known_jobs_is_final(self, native_jobid):
        if self._known_jobs[native_jobid].state == bliss.saga.job.Job.Done:
            return True
        elif self._known_jobs[native_jobid].state == bliss.saga.job.Job.Failed:
            return True
        elif self._known_jobs[native_jobid].state == bliss.saga.job.Job.Canceled:
            return True
        else:
            return False
 
    ######################################################################
    ##
    def _check_context(self): 
        '''sets self._cw to a usable access configuration or throws'''
        
        # see if we run stuff on the local machine 
        if self._url.scheme == "sge":
            self._use_ssh = False
            cw = CommandWrapper(via_ssh=False)
            result = cw.run("which qstat")#, ["--version"]) ### CHANGE to sge tool name
            if result.returncode != 0:
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't find SGE tools on %s" % (self._url))
            else:
                self._cw = cw

        elif self._url.scheme == "sge+ssh":
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
                        self._pi.log_warning("Using context %s to access %s failed." \
                          % (ctx, self._url))

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
            result = self._cw.run("which qstat")# --version") ### CHANGE to SGE tools
            if result.returncode != 0:
                self._pi.log_error_and_raise("11", "Couldn't find SGE command line tools on %s: %s" \
                  % (self._url, result.stderr))
            else:
                self._pi.log_info("Found SGE command line tools on %s at %s" \
                  % (self._url, result.stdout.replace('/qstat', '')))
               
                si = self.get_service_info()
                if si.GlueHostArchitectureSMPSize != None:
                    self._ppn = si.GlueHostArchitectureSMPSize
         
                    #self._ppn   = int(nodes[1].split(" = ")[1].strip())
                #    self._pi.log_info("%s seems to have %s nodes and %s processors (cores) per node" \
                #      % (self._url, self._nodes, self._ppn))
          

    ######################################################################
    ##
    def get_service_info(self):
        '''Returns a single saga.job service description'''
        if self._cw == None:
            self._check_context()
        
        if self._service_info == None:
            # initial creation
            self._pi.log_info("Service info cache empty. Updating local service info.")
            qstat_result = self._cw.run("qstat -g c")
            if qstat_result.returncode != 0:
                raise Exception("Error running 'qstat': %s" % qstat_result.stderr)
            sgeqstat_result = self._cw.run("qstat -g c")
            if sgeqstat_result.returncode != 0:
                raise Exception("Error running 'qstat': %s" % sgeqstat_result.stderr)

            self._service_info = SGEServiceInfo(qstat_result.stdout,
                                                sgeqstat_result.stdout, self._pi)
            self._service_info_last_update = time.time()

        else: 
            if self._service_info_last_update+15.0 < time.time():
                # older than 15 seconds. update.
                self._pi.log_info("15s service info cache expired. Updating local service info.")
                qstat_result = self._cw.run("qstat_result -g c")
                if qstat_result.returncode != 0:
                    raise Exception("Error running 'qstat': %s" % qstat_result.stderr)
                sgeqstat_result = self._cw.run("qstat -g c")
                if sgeqstat_result.returncode != 0:
                    raise Exception("Error running 'qstat -g c': %s" % sgeqstat_result.stderr)

                self._service_info = SGEServiceInfo(qstat_result.stdout,
                                                    sgeqstat_result.stdout, self._pi)
                self._service_info_last_update = time.time()
            else:
                self._pi.log_info("15s cache not expired yet. Using local service info.")
        
        return self._service_info

    ######################################################################
    ##
    def list_jobs(self):
        '''Return the jobs known to qstat'''
        jobids = []
        if self._cw == None:
            self._check_context()
        
        result = self._cw.run("qstat ")
        if result.returncode != 0:
            raise Exception("Error running 'qstat': %s" % result.stderr)

        lines = result.stdout.split("\n\n")
        for line in lines:
            jobinfo = SGEJobInfo(line, self._pi)
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
            if self._known_jobs_is_final(saga_jobid.native_id):
                return self._known_jobs[saga_jobid.native_id]


        result = self._cw.run("qstat -f -j %s" % (saga_jobid.native_id))
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

        jobinfo = SGEJobInfo(result.stdout, self._pi)
        self._known_jobs_update(jobinfo.jobid, jobinfo)

        return jobinfo


    ######################################################################
    ##
    def get_jobinfo_bulk(self, saga_jobids):

        '''Returns a running PBS job as saga object'''
        if self._cw == None:
            self._check_context()

        jobinfos = list()
        nativeids = str()
        # pre-filter finished jobs
        for jobid in saga_jobids:
            if self._known_jobs_exists(jobid.native_id):
                if self._known_jobs_is_final(jobid.native_id):
                    jobinfos.append(self._known_jobs[jobid.native_id])
                else:
                    nativeids += ("%s " % (jobid.native_id))
        # run bulk qstat
        result = self._cw.run("qstat -f -j %s" % nativeids)
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
                raise Exception("Error running %s: %s" \
                  % (result.executable, result.stderr))
        # create JobInfo objects
        for result in result.stdout.split('\n\n'):
            if result.find("Unable to copy") != -1:
                # error that pops up sometimes. Ignore
                pass
            else:
                jobinfo = SGEJobInfo(result, self._pi)
                self._known_jobs_update(jobinfo.jobid, jobinfo)
                jobinfos.append(jobinfo)

        return jobinfos


    ######################################################################
    ##
    def get_job_state(self, saga_jobid):
        '''Returns the state of the job with the given jobid.
        '''
        return self.get_jobinfo(saga_jobid).state

    ######################################################################
    ##
    def get_bulk_job_states(self, saga_jobids):
        '''Returns a list of states for the job with the given jobids.
        '''
        #jobids_str = list()
        ##for jobid in saga_jobids:
        #    jobids_str.append(str(jobid))
        #self._pi.log_info("Trying to get bulk states for: %s " \
        #  % (jobids_str))

        states = list()
        for jobinfo in self.get_jobinfo_bulk(saga_jobids):
            states.append(jobinfo.state)
        return states

    ######################################################################
    ##
    def _sge_script_generator(self, jd):
        '''Generates a SGE script from a SAGA job description.
        '''
        sge_params = str()
        exec_n_args = str()

        if jd.executable is not None:
            exec_n_args += "%s " % (jd.executable) 
        if jd.arguments is not None:
            for arg in jd.arguments:
                exec_n_args += "%s " % (arg)

        sge_params += "#SGE -N %s \n" % "bliss_job" 
        sge_params += "#SGE -V     \n"

        if jd.environment is not None:
            variable_list = str()
            for key in jd.environment.keys(): 
                variable_list += "%s=%s," % (key, jd.environment[key])
            sge_params += "#SGE -v %s \n" % variable_list

        if jd.working_directory is not None:
            sge_params += "#SGE -d %s \n" % jd.working_directory 
        if jd.output is not None:
            sge_params += "#SGE -o %s \n" % jd.output
        if jd.error is not None:
            sge_params += "#SGE -e %s \n" % jd.error 
        if jd.wall_time_limit is not None:
            sge_params += "#SGE -l h_rt=%s \n" % jd.wall_time_limit
        if jd.queue is not None:
            sge_params += "#SGE -q %s \n" % jd.queue
        if jd.project is not None:
            sge_params += "#SGE -A %s \n" % jd.project[0]
        if jd.contact is not None:
            sge_params += "#SGE -m be \n"
            sge_params += "#SGE -M %s \n" % jd.contact
        

        if jd.total_cpu_count is not None:
            sge_params += "#SGE -pe %sway %s" % (self._ppn, str(jd.total_cpu_count))

        sgescript = "\n#!/bin/bash \n%s \n%s" % (sge_params, exec_n_args)
        self._pi.log_info("Generated SGE script: %s" % (sgescript))
        return sgescript


    ######################################################################
    ##
    def submit_job(self, job):
        '''Submits a job to SGE and returns a jobinfo structure.
        '''
        if self._cw == None:
            self._check_context()

        script = self._sge_script_generator(job.get_description())

        # filter the script
        script = script.replace("\"", "\\\"")
        result = self._cw.run("echo \"%s\" | qsub" % (script))
 
        if result.returncode != 0:
            if len(result.stderr) < 1:
                error = result.stdout
            else:
                error = result.stderr
            raise Exception("Error running 'qsub': %s. Script was: %s" % (error, script))
        else:
            #depending on the SGE configuration, the job can already 
            #have disappeared from the queue at this point. that's why
            #we create a dummy job info here
            ji = SGEJobInfo("", self._pi)
            ji._jobid = result.stdout.split("\n")[0]
            ji._job_state = "R"
            self._known_jobs_update(ji.jobid, ji)

            jobinfo = self.get_jobinfo(bliss.saga.job.JobID(self._url, 
              result.stdout.split("\n")[0]))
            return jobinfo

    ######################################################################
    ##
    def cancel_job(self, saga_jobid):
        '''Cancel the job.
        '''
        if self._cw == None:
            self._check_context()

        result = self._cw.run("qdel %s" % (saga_jobid.native_id))
 
        if result.returncode != 0:
            raise Exception("Error running 'qdel': %s" % result.stderr)
        else:
            jobinfo = self.get_jobinfo(saga_jobid)
            if jobinfo.state == bliss.saga.job.Job.Done:
                self.get_jobinfo(saga_jobid)._job_state = 'X' # pseudo-SGE 'Canceled'
            #return jobinfo
