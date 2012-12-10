# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import copy
import socket
import time
import string
import getpass
import subprocess
import bliss.saga
import os.path

from bliss.utils.command_wrapper import CommandWrapper, CommandWrapperException
from bliss.utils.job.transfer_directives import TransferDirectives
from bliss.utils.jobid import JobID

################################################################################
################################################################################

def condor_to_saga_jobstate(cdrjs):
    '''translates a condor one-letter state to saga'''

    # From: http://pages.cs.wisc.edu/~adesmet/status.html
    # 
    # JobStatus in job ClassAds
    # 
    # 0   Unexpanded  U
    # 1   Idle    I
    # 2   Running R
    # 3   Removed X
    # 4   Completed   C
    # 5   Held    H
    # 6   Submission_err  E

    if int(cdrjs) == 0:
        return bliss.saga.job.Job.Pending   
    elif int(cdrjs) == 1:
        return bliss.saga.job.Job.Pending
    elif int(cdrjs) == 2:
        return bliss.saga.job.Job.Running
    elif int(cdrjs) == 3:
        return bliss.saga.job.Job.Canceled
    elif int(cdrjs) == 4:
        return bliss.saga.job.Job.Done
    elif int(cdrjs) == 5:
        return bliss.saga.job.Job.Pending
    elif int(cdrjs) == 6:
        return bliss.saga.job.Job.Failed
    else:
        return bliss.saga.job.Job.Unknown

################################################################################
################################################################################

class CondorJobInfo(object):
    '''Encapsulates infos about a Condor job 
    '''

    def __init__(self, condor_q, plugin):
        '''Constructor: initialize from qstat -f <jobid> string.
        '''

        ## There is data for this job! 
        if len(condor_q) > 1000:
            try:
                for line in condor_q.split("\n"):
                    if "JobStatus" in line and "LastJobStatus" not in line:
                        self._job_state = line.split("=")[1].strip()
                    elif 'ClusterId' in line:
                        self._jobid = line.split("=")[1].strip()
                    elif 'ExitStatus' in line:
                        self._job_exitcode = line.split("=")[1].strip()

            except Exception, ex:
                raise Exception("Couldn't parse %s: %s" \
                  % (condor_q, ex))

    @property 
    def state(self):
        return condor_to_saga_jobstate(self._job_state)

    @property 
    def jobid(self):
        return self._jobid

    #@property 
    #def gridresource(self):
    #    return self._job_gridres.walltime

    @property 
    def exitcode(self):
        return self._job_exitcode


################################################################################
################################################################################

class CondorService:
    '''Encapsulates Condor command line tools.
    '''

    def __init__(self, plugin, service_obj):
        '''Constructor'''
        self._pi    = plugin
        self._so    = service_obj
        self._url   = service_obj._url
        self._cw    = None
        self._ppn   = 1 # number of processors per node. defaults to 1
        self._nodes = 1 # total number of nodes. defaults to 1

        if self._url.scheme in ["condor"]:
            if (self._url.host != "localhost") and (self._url.host != socket.gethostname()):
                self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Can't use the Condor plug-in remotely. Only condor://localhost URLs are valid")

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
        
        ################################################################# 
        ## ...:// URL
        if self._url.scheme in ["condor"]:
            self._use_ssh = False
            try:
                ## EXECUTE SHELL COMMAND
                cw = CommandWrapper.initAsLocalWrapper(logger=self._pi)
                cw.connect()
                self._cw = cw
            except CommandWrapperException, ex:
                self._pi.log_error("Problem creating local Condor command wrapper for %s: %s." \
                    % (self._url, ex))

        ################################################################# 
        ## ...+SSH:// URL
        elif self._url.scheme in ["condor+ssh"]:
            # first, we construct a list of possible SSH login credentials
            credentials = list()
            # we start with the contexts:
            for ctx in self._so.session.contexts:
                if ctx.type is bliss.saga.Context.SSH:
                    credentials.append({'username':ctx.userid,
                                        'userkey' :ctx.userkey,
                                        'mode' : 'context'})
                    # if a username is defined in the url, we also 
                    # want to try that
                    if self._url.username is not None:
                        credentials.append({'username':self._url.username,
                                            'userkey' :ctx.userkey,
                                            'mode' : 'context+url.username'}) 
            # next, we construct credentials with just usernames
            if self._url.username is not None:
                credentials.append({'username': self._url.username,
                                    'userkey' : None,
                                    'mode' : 'url.username'}) 

            credentials.append({'username': getpass.getuser(),
                                'userkey' : None,
                                'mode' : 'local.username'}) 

            # now, we simply iterate over the credentials and try to
            # establish a connection with every single one. as soon
            # as we've found a working one, we're done.
            for cred in credentials:
                try:
                    cw = CommandWrapper.initAsSSHWrapper(logger=self._pi,
                                                         username=cred['username'], 
                                                         hostname=self._url.host, 
                                                         userkey=cred['userkey'])
                    cw.connect()
                    self._cw = cw
                    self._pi.log_info("SSH: Using credential %s to access %s." \
                        % (cred, self._url.host))                            
                    break
                except CommandWrapperException, ex:
                    self._pi.log_error("SSH: Can't use credential %s to access %s." \
                        % (cred, self._url.host))       
          
        ################################################################# 
        ## ...+GSISSH:// URL
        elif self._url.scheme in ["condor+gsissh"]:
            # first, we construct a list of possible SSH login credentials
            credentials = list()
            # we start with the contexts:
            for ctx in self._so.session.contexts:
                if ctx.type is bliss.saga.Context.X509:
                    credentials.append({'username':ctx.userid,
                                        'x509_userproxy' :ctx.userproxy,
                                        'mode' : 'context'})
                    # if a username is defined in the url, we also 
                    # want to try that
                    if self._url.username is not None:
                        credentials.append({'username':self._url.username,
                                            'x509_userproxy' :ctx.userproxy,
                                            'mode' : 'context+url.username'}) 
            # next, we construct credentials with just usernames
            if self._url.username is not None:
                credentials.append({'username': self._url.username,
                                    'x509_userproxy' : None,
                                    'mode' : 'url.username'})

            credentials.append({'username': getpass.getuser(),
                                'x509_userproxy' : None,
                                'mode' : 'local.username'}) 

            # now, we simply iterate over the credentials and try to
            # establish a connection with every single one. as soon
            # as we've found a working one, we're done.
            for cred in credentials:
                try:
                    cw = CommandWrapper.initAsGSISSHWrapper(logger=self._pi,
                                                            username=cred['username'], 
                                                            hostname=self._url.host, 
                                                            x509_userproxy=cred['x509_userproxy'])
                    cw.connect()
                    self._cw = cw
                    self._pi.log_info("GSISSH: Using credential %s to access %s." \
                        % (cred, self._url.host))                            
                    break
                except CommandWrapperException, ex:
                    self._pi.log_error("GSISSH: Can't use credential %s to access %s." \
                        % (cred, self._url.host))       
           
        # at this point, either self._cw contains a usable 
        # configuration, or the whole thing should go to shit
        if self._cw is None:
            self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                "Couldn't find a way to access %s" % (self._url))
        else:
            # now let's see if we can find PBS
            result = self._cw.run("which condor_submit")# --version")
            if result.returncode != 0:
                 self._pi.log_error_and_raise(bliss.saga.Error.NoSuccess, 
                  "Couldn't find Condor command line tools: %s" % (result.stderr))
            else:
                self._pi.log_debug("Found Condor command line tools: %s" \
                                   % (result.stdout))
                   
            #si = self.get_service_info()
            #if si.GlueHostArchitectureSMPSize != None:
            #    self._ppn = si.GlueHostArchitectureSMPSize
          
        return self._service_info

    ######################################################################
    ##
    def list_jobs(self):
        '''Return the jobs known to qstat'''
        jobids = []
        if self._cw == None:
            self._check_context()
       
        ## EXECUTE SHELL COMMAND 
        result = self._cw.run("qstat -f1")
        if result.returncode != 0:
            raise Exception("Error running 'qstat': %s" % result.stderr)

        lines = result.stdout.split("\n\n")
        for line in lines:
            jobinfo = PBSJobInfo(line, self._pi)
            self._known_jobs_update(jobinfo.jobid, jobinfo)
            jobids.append(bliss.utils.jobid.JobID(self._url, jobinfo.jobid))
        return jobids


    ######################################################################
    ##
    def get_jobinfo(self, saga_jobid):
        '''Returns a running Condor job as saga object'''
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
        elif type(saga_jobid) == bliss.utils.jobid.JobID:
            native_id = saga_jobid.native_id
        else:
            raise Exception("Unsupported job ID format: %s. Expected format: [service_url]-[native_id]." % saga_jobid)

        if self._known_jobs_exists(native_id):
            if self._known_jobs_is_final(native_id):
                return self._known_jobs[native_id]

        result = self._cw.run("condor_q -long %s" % (native_id))
        time.sleep(1)
        if result.returncode != 0:
            if self._known_jobs_exists(native_id):
                ## if the job is on record but can't be reached anymore,
                ## this probablty means that it has finished and already
                ## kicked out qstat. in that case we just set it's state 
                ## to done.
                jobinfo = self._known_jobs[native_id]
                jobinfo._job_state = 4 # Condor 'Complete'
                return jobinfo
            else:
                ## something went wrong.
                raise Exception("Error running 'condor_q': %s" % result.stderr)

        elif (result.returncode == 0 and len(result.stdout) < 1000): # yes, this is bad!
                jobinfo = self._known_jobs[native_id]
                if jobinfo.state == bliss.saga.job.Job.Running:
                    # previous state was running. so we are most def. DONE
                    jobinfo._job_state = 4 # Condor 'Complete'
                else:
                    jobinfo._job_state = 6 # Condor 'Failed'
                return jobinfo

        jobinfo = CondorJobInfo(result.stdout, self._pi)
        jobinfo._jobid = native_id
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
    def _condor_script_generator(self, jd, service_url):
        '''Generates a Condor script from a SAGA job description.
        '''
        condor_file = str()

        ##### OPTIONS PASSED VIA JOB SERVICE URL #####
        ##
        if service_url.query is not None:
            from bliss.utils.configfile import ConfigQuery
            condor_file += "\n##### DEFAULT OPTIONS AND OPTIONS PASSED VIA JOB SERVICE URL #####\n##"
            # special treatment for universe - defaults to 'vanilla'
            if 'universe' not in ConfigQuery(service_url.query).as_dict():
                condor_file += "\nuniverse = vanilla"
            for (key, value) in ConfigQuery(service_url.query).as_dict().iteritems():
                condor_file += "\n%s = %s" % (key, value)


        ##### OPTIONS PASSED VIA JOB DESCRIPTION #####
        ##
        condor_file += "\n\n##### OPTIONS PASSED VIA JOB SERVICE URL #####\n##"
        requirements = "requirements = "

        # executable -> executable
        if jd.executable is not None:
            condor_file += "\nexecutable = %s" % jd.executable

        # arguments -> arguments
        arguments = "arguments = "
        if jd.arguments is not None:
            for arg in jd.arguments:
                arguments += "%s " % (arg)
        condor_file += "\n%s" % arguments

        # file_transfer -> transfer_input_files
        if jd.file_transfer is not None:
            td = TransferDirectives(jd.file_transfer)

            if len(td.in_append_dict) > 0:
                raise Exception('FileTransfer append syntax (>>) not supported by Condor: %s' % td.in_append_dict)
            if len(td.out_append_dict) > 0:
                raise Exception('FileTransfer append syntax (<<) not supported by Condor: %s' % td.out_append_dict)
            
            if len(td.in_overwrite_dict) > 0:
                transfer_input_files = "transfer_input_files = "
                for (source, target) in td.in_overwrite_dict.iteritems():
                    # make sure source is file an not dir
                    (s_path, s_entry) = os.path.split(source)
                    if len(s_entry) < 1:
                        raise Exception('Condor accepts only files (not directories) as FileTransfer sources: %s' % source)
                    # make sure target is just a file 
                    (t_path, t_entry) = os.path.split(target)
                    if len(t_path) > 1:
                        raise Exception('Condor accepts only filenames (without paths) as FileTransfer targets: %s' % target)
                    # make sure source and target file are the same
                    if s_entry != t_entry:
                        raise Exception('For Condor source file name and target file name have to be identical: %s != %s' % (s_entry, t_entry))
                    # entry ok - add to job script
                    transfer_input_files += "%s, " % source
                condor_file += "\n%s" % transfer_input_files

            if len(td.out_overwrite_dict) > 0:
                transfer_output_files = "transfer_output_files = "
                for (source, target) in td.out_overwrite_dict.iteritems():
                    # make sure source is file an not dir
                    (s_path, s_entry) = os.path.split(source)
                    if len(s_entry) < 1:
                        raise Exception('Condor accepts only files (not directories) as FileTransfer sources: %s' % source)
                    # make sure target is just a file 
                    (t_path, t_entry) = os.path.split(target)
                    if len(t_path) > 1:
                        raise Exception('Condor accepts only filenames (without paths) as FileTransfer targets: %s' % target)
                    # make sure source and target file are the same
                    if s_entry != t_entry:
                        raise Exception('For Condor source file name and target file name have to be identical: %s != %s' % (s_entry, t_entry))
                    # entry ok - add to job script
                    transfer_output_files += "%s, " % source
                condor_file += "\n%s" % transfer_output_files

        # always define log
        condor_file += "\nlog = saga-condor-job-$(cluster).log "

        # output -> output
        if jd.output is not None:
            condor_file += "\noutput = %s " % jd.output

        # error -> error
        if jd.error is not None:
            condor_file += "\nerror = %s " % jd.error 

        # environment -> environment
        environment = "environment = "
        if jd.environment is not None:
            variable_list = str()
            for key in jd.environment.keys(): 
                variable_list += "%s=%s;" % (key, jd.environment[key])
            environment += "%s " % variable_list
        condor_file += "\n%s" % environment

        # project -> +ProjectName
        if jd.project is not None:
            condor_file += "\n+ProjectName = \"%s\"" % str(jd.project)

        # candidate hosts -> SiteList + requirements
        if jd.candidate_hosts is not None:
            hosts = ""
            for host in jd.candidate_hosts:
                hosts += "%s, " % host
            sitelist = "+SiteList = \"%s\"" % hosts
            requirements += "(stringListMember(GLIDEIN_ResourceName,SiteList) == True)"
            condor_file += "\n%s" % sitelist
            condor_file += "\n%s" % requirements

        condor_file += "\n\nqueue"

        self._pi.log_debug("Generated Condor script: %s" % (condor_file))
        return condor_file


    ######################################################################
    ##
    def submit_job(self, job):
        '''Submits a job to PBS and returns a jobinfo structure.
        '''
        if self._cw == None:
            self._check_context()

        script = self._condor_script_generator(job.get_description(), self._url)

        result = self._cw.run("echo \'%s\' | condor_submit -" % (script))

        if result.returncode != 0:
            raise Exception("Error running 'condor_submit': %s. Script was: %s" % (result.stdout, script))
        else:
            ji = CondorJobInfo("", self._pi)
            for line in result.stdout.split("\n"):
                if "** Proc" in line:
                    ji._jobid = line.split()[2][:-1]
                elif "JobStatus" in line:
                    ji._job_state = line.split(" = ")[1].strip()

            self._known_jobs_update(ji.jobid, ji)

            jobinfo = self.get_jobinfo(bliss.utils.jobid.JobID(self._url, 
                                       ji._jobid))
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
                self.get_jobinfo(saga_jobid)._job_state = 3 # Condor 'Canceled'
            #return jobinfo
