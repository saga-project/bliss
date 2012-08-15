# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import copy
import socket
import time
import string
import subprocess
import bliss.saga

from bliss.utils.command_wrapper import CommandWrapper

################################################################################
################################################################################

def pbs_to_saga_jobstate(pbsjs):
    '''translates a pbs one-letter state to saga'''
    if pbsjs == 'C':
        return bliss.saga.job.Job.Done
    elif pbsjs == 'E':
        return bliss.saga.job.Job.Running
    elif pbsjs == 'H':
        return bliss.saga.job.Job.Pending
    elif pbsjs == 'Q':
        return bliss.saga.job.Job.Pending
    elif pbsjs == 'R':
        return bliss.saga.job.Job.Running 
    elif pbsjs == 'T': 
        return bliss.saga.job.Job.Running 
    elif pbsjs == 'W':
        return bliss.saga.job.Job.Pending
    elif pbsjs == 'S':
        return bliss.saga.job.Job.Pending
    elif pbsjs == 'X':
        return bliss.saga.job.Job.Canceled
    else:
        return bliss.saga.job.Job.Unknown

################################################################################
################################################################################

class PBSServiceInfo(object):
    '''Encapsulates infos about a PBS cluster as returned by qstat & pbsnodes.
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

        lines = qstat_a_output.split("\n")
        for line in lines: 
            if line.find(" R ") != -1:
                jobs_running += 1
            elif line.find(" Q ") != -1:
                jobs_waiting += 1

        self.GlueCEStateRunningJobs = str(jobs_running)
        self.GlueCEStateWaitingJobs = str(jobs_waiting)
        self.GlueCEStateTotalJobs = str(jobs_running+jobs_waiting)

        if pbsnodes_output is not None:
            # get all sorts of useful info about the 
            # PBS cluster and translate it into GLUE
            # schema attributes
            cpus_total   = 0
            cpus_free    = 0
            cpus_pernode = 0

            self._nodeinfo=list()
            for node_raw in pbsnodes_output.split('\n\n'):
                lines = node_raw.split('\n')
                node_data = dict()
                for line in lines[1:]:
                    (key, value) = line.split(" = ")
                    key = key.strip()
                    node_data[key] = value
                self._nodeinfo.append(node_data)
                
                try: 
                    cpus_total += int(node_data['np'])
                    if node_data['state'] == 'free':
                        try:
                            cpus_free += int(node_data['np'])
                            for item in node_data['status'].split(','):
                                (key, val) = item.split("=")
                                if key == 'physmem':
                                    self.GlueHostMainMemoryRAMSize = val.replace('kb','')
                        except Exception, ex:
                            plugin.log_wrning("Can't determine GlueHostMainMemoryRAMSize.")
                except Exception, ex:
                    pass # this is messy, but it seems to work

            self.GlueSubClusterPhysicalCPUs = str(cpus_total)
            self.GlueCEStateFreeCPUs = str(cpus_free)
            self.GlueHostArchitectureSMPSize = self._nodeinfo[0]['np']


    def has_attribute(self, key):
        if self.__dict__[key] != None:
            return True
        else: 
            return False

    def get_attribute(self, key):
        return self.__dict__[key]

################################################################################
################################################################################

class PBSJobInfo(object):
    '''Encapsulates infos about a PBS job as returned by qstat -f1.
    '''

    def __init__(self, qstat_f_output, plugin):
        '''Constructor: initialize from qstat -f <jobid> string.
        '''
        
        #plugin.log_debug("Got raw qstat output: %s" % qstat_f_output)
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
            #plugin.log_debug("Parsed qstat output: %s" % str(self.__dict__))


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

class PBSService:
    '''Encapsulates PBS command line tools.
    '''

    def __init__(self, plugin, service_obj):
        '''Constructor'''
        self._pi    = plugin
        self._so    = service_obj
        self._url   = service_obj._url
        self._cw    = None
        self._ppn   = 1 # number of processors per node. defaults to 1
        self._nodes = 1 # total number of nodes. defaults to 1

        if self._url.scheme == "pbs":
            if (self._url.host != "localhost") and (self._url.host != socket.gethostname()):
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Can't use %s as a (non-local) hostname in conjunction with pbs:// schema. Try pbs+ssh:// instead" \
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
        if self._url.scheme in ["pbs", "torque", "xt5torque"]:
            self._use_ssh = False
            cw = CommandWrapper(plugin=self._pi, via_ssh=False)
            
            result = cw.run("which pbsnodes")#, ["--version"])
            if result.returncode != 0:
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't find PBS tools on %s" % (self._url))
            else:
                self._cw = cw

        elif self._url.scheme in ["pbs+ssh", "torque+ssh", "xt5torque+ssh"]:
            # iterate over all SSH contexts to see if one of them is
            # usable. we stop after we have found one.
            usable_ctx = None
            for ctx in self._so.session.contexts:
                if ctx.context_type is bliss.saga.Context.SSH:
                    if ctx.user_key is not None:
                        import os.path
                        if not os.path.isfile(ctx.user_key):
                            self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                                                         "user_key %s doesn't exist." % ctx.user_key)
                    try:
                        cw = CommandWrapper(plugin=self._pi, via_ssh=True,
                                            ssh_username=ctx.user_id, 
                                            ssh_hostname=self._url.host, 
                                            ssh_key=ctx.user_key)
                        result = cw.run("true")
                        if result.returncode == 0:
                            usable_ctx = ctx
                            self._cw = cw
                            self._pi.log_debug("Using context %s to access %s succeeded" \
                              % (ctx, self._url))
                            break
                    except Exception, ex:
                        self._pi.log_debug("Using context %s to access %s failed: %s" \
                          % (ctx, self._url, ex))

            if usable_ctx is None:
                # see if we can use system defaults to run
                # stuff via ssh
                cw = CommandWrapper(plugin=self._pi, ssh_hostname=self._url.host, via_ssh=True)
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
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "Couldn't find a way to access %s" % (self._url))
            
            # now let's see if we can find PBS
            result = self._cw.run("which pbsnodes")# --version")
            if result.returncode != 0:
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "Couldn't find PBS command line tools on %s: %s" % (self._url, result.stderr))
            else:
                self._pi.log_info("Found PBS command line tools on %s at %s" \
                  % (self._url, result.stdout.replace('/pbsnodes', '')))
               
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
            qstat_result = self._cw.run("qstat -a")
            if qstat_result.returncode != 0:
                raise Exception("Error running 'qstat': %s" % qstat_result.stderr)
            pbsnodes_result = self._cw.run("pbsnodes")
            if pbsnodes_result.returncode != 0:
                raise Exception("Error running 'pbsnodes': %s" % pbsnodes_result.stderr)

            self._service_info = PBSServiceInfo(qstat_result.stdout,
                                                pbsnodes_result.stdout, self._pi)
            self._service_info_last_update = time.time()

        else: 
            if self._service_info_last_update+15.0 < time.time():
                # older than 15 seconds. update.
                self._pi.log_info("15s service info cache expired. Updating local service info.")
                qstat_result = self._cw.run("qstat_result -a")
                if qstat_result.returncode != 0:
                    raise Exception("Error running 'qstat': %s" % qstat_result.stderr)
                pbsnodes_result = self._cw.run("pbsnodes")
                if pbsnodes_result.returncode != 0:
                    raise Exception("Error running 'pbsnodes': %s" % pbsnodes_result.stderr)

                self._service_info = PBSServiceInfo(qstat_result.stdout,
                                                    pbsnodes_result.stdout, self._pi)
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

        if type(saga_jobid) == str:
            try:
                (p1, native_id) = saga_jobid.split(']-[')
                if native_id[-1] != ']':
                    raise Exception()
                else:
                   native_id = native_id.rstrip(']')    
            except Exception:
                raise Exception("Unsupported job ID format: %s. Expected format: [service_url]-[native_id]." % saga_jobid)
        elif type(saga_jobid) == bliss.saga.job.JobID:
            native_id = saga_jobid.native_id
        else:
            raise Exception("Unsupported job ID format: %s. Expected format: [service_url]-[native_id]." % saga_jobid)

        if self._known_jobs_exists(native_id):
            if self._known_jobs_is_final(native_id):
                return self._known_jobs[native_id]


        result = self._cw.run("qstat -f1 %s" % (native_id))
        if result.returncode != 0:
            if self._known_jobs_exists(native_id):
                ## if the job is on record but can't be reached anymore,
                ## this probablty means that it has finished and already
                ## kicked out qstat. in that case we just set it's state 
                ## to done.
                jobinfo = self._known_jobs[native_id]
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
        result = self._cw.run("qstat -f1 %s" % nativeids)
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
                jobinfo = PBSJobInfo(result, self._pi)
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

    def shellquote(self, s):
        return "'" + s.replace("'", "'\\''") + "'"

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

        if jd.name is not None:
            pbs_params += "#PBS -N %s \n" % jd.name
        else:
            pbs_params += "#PBS -N %s \n" % "bliss_job"
 
        pbs_params += "#PBS -V     \n"

        if jd.environment is not None:
            variable_list = str()
            for key in jd.environment.keys(): 
                variable_list += "%s=%s," % (key, jd.environment[key])
            pbs_params += "#PBS -v %s \n" % variable_list

        if jd.working_directory is not None:
            pbs_params += "#PBS -d %s \n" % jd.working_directory 
        if jd.output is not None:
            pbs_params += "#PBS -o %s \n" % jd.output
        if jd.error is not None:
            pbs_params += "#PBS -e %s \n" % jd.error 
        if jd.wall_time_limit is not None:
            hours = jd.wall_time_limit/60
            minutes = jd.wall_time_limit%60
            pbs_params += "#PBS -l walltime=%s:%s:00 \n" % (str(hours), str(minutes))
        if jd.queue is not None:
            pbs_params += "#PBS -q %s \n" % jd.queue
        if jd.project is not None:
            pbs_params += "#PBS -A %s \n" % str(jd.project)
        if jd.contact is not None:
            pbs_params += "#PBS -m abe \n"
       
        if self._url.scheme in ["xt5torque", "xt5torque+ssh"]:
            # Special case for TORQUE on Cray XT5s
            self._pi.log_info("Using Cray XT5 spepcific modifications, i.e., -l size=xx instead of -l nodes=x:ppn=yy ")
            if jd.total_cpu_count is not None:
                pbs_params += "#PBS -l size=%s" % jd.total_cpu_count
        else:
            # Default case (non-XT5)
            if jd.total_cpu_count is not None:
                tcc = int(jd.total_cpu_count)
                tbd = float(tcc)/float(self._ppn)
                if float(tbd) > int(tbd):
                    pbs_params += "#PBS -l nodes=%s:ppn=%s" % (str(int(tbd)+1), self._ppn)
                else:
                    pbs_params += "#PBS -l nodes=%s:ppn=%s" % (str(int(tbd)), self._ppn)

        pbscript = "\n#!/bin/bash \n%s \n%s" % (pbs_params, exec_n_args)
        self._pi.log_debug("Generated PBS script: %s" % (pbscript))
        return pbscript


    ######################################################################
    ##
    def submit_job(self, job):
        '''Submits a job to PBS and returns a jobinfo structure.
        '''
        if self._cw == None:
            self._check_context()

        script = self._pbscript_generator(job.get_description())

        # filter the script - esapce problematic characters
        #scprpt = script.replace("'", "\'")
        #script = script.replace("\"", "\\\"")
        result = self._cw.run("echo \'%s\' | qsub" % (script))
 
        if result.returncode != 0:
            if len(result.stderr) < 1:
                error = result.stdout
            else:
                error = result.stderr
            raise Exception("Error running 'qsub': %s. Script was: %s" % (error, script))
        else:
            #depending on the PBS configuration, the job can already 
            #have disappeared from the queue at this point. that's why
            #we create a dummy job info here
            ji = PBSJobInfo("", self._pi)
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
                self.get_jobinfo(saga_jobid)._job_state = 'X' # pseudo-PBS 'Canceled'
            #return jobinfo
