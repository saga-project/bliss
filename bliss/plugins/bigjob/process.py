#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import copy
import time
import subprocess
import bliss.saga

def filter_error(reply):
    if type(reply) is dict and reply.has_key('error'):
        raise Exception("The server replied with an error: %s" % reply['error'])
    else:
        return reply

def bj_to_saga_state(bjstate):
    if bjstate == 'Running':
        return bliss.saga.job.Job.Running
    elif bjstate == 'New':
        return bliss.saga.job.Job.New
    elif bjstate == 'Failed':
        return bliss.saga.job.Job.Failed
    elif bjstate == 'Done':
        return bliss.saga.job.Job.Done
    elif bjstate == 'Unknown':
        return bliss.saga.job.Job.Unknown
    else:
        return bliss.saga.job.Job.Unknown
        
       

class LocalJobProcess(object):
    '''A wrapper around a subprocess'''

#    __slots__ = {'prochandle', 'executable', 'arguments', 
#                 'environment', 'returncode', 'pid', 'state',
#                 't_created', 't_started', 't_finished'}

    def __init__(self, jobdescription, plugin, proxy, pilot):
        self.proxy       = proxy
        self.pilot       = pilot
        
        self.executable  = jobdescription.executable
        self.arguments   = jobdescription.arguments
        self.environment = jobdescription.environment
        
        self.prochandle = None
        self.pid = None
        self.returncode = None
        self.state = bliss.saga.job.Job.New
        self.pi = plugin
        

    def __del__(self):
        if self._job_output is not None:
            self._job_output.close()
        if self._job_error is not None:
            self._job_error.close()


    def run(self, jd):
#                                           env=self.environment)
       # Translate job description to workunit description


        wud = {'executable'          : jd.executable,
               'arguments'           : jd.arguments,
               'number_of_processes' : jd.number_of_processes,
               'spmd_variation'      : 'single',
               'working_directory'   : jd.working_directory,
               'output'              : jd.output,
               'error'               : jd.error
              }

        self.pid = filter_error(self.proxy.bj_workunit_add(self.pilot, wud))
        self.state = bj_to_saga_state(filter_error(self.proxy.bj_workunit_status(self.pilot, self.pid)['state']))
        self.pi.log_info("Submitted workunit: %s. Status: %s" % (str(self.pid), str(self.state)))


#bliss.saga.job.Job.Running

    def getpid(self, serviceurl):
        return "[%s]-[%s]" % (serviceurl, self.pid)

    def getstate(self):
        if self.pid is None:
            self.state = bliss.saga.job.Job.Unknown
        else:
            self.state = bj_to_saga_state(filter_error(self.proxy.bj_workunit_status(self.pilot, self.pid)['state']))
        return self.state

    def terminate(self):
        self.prochandle.terminate()
        self.state = bliss.saga.job.Job.Canceled


    def wait(self, timeout):
        if timeout == -1:
            # wait forever
            while True:
                self.state = bj_to_saga_state(filter_error(self.proxy.bj_workunit_status(self.pilot, self.pid)['state']))
                if self.state == bliss.saga.job.Job.Done or self.state == bliss.saga.job.Job.Failed:
                    break
                time.sleep(1)
        else:
            t_beginning = time.time()
            seconds_passed = 0
            while True:
                self.state = bj_to_saga_state(filter_error(self.proxy.bj_workunit_status(self.pilot, self.pid)['state']))
                if self.state == bliss.saga.job.Job.Done or self.state == bliss.saga.job.Job.Failed:
                    break
                seconds_passed = time.time() - t_beginning
                if timeout and seconds_passed > timeout:
                    break
        return 0

    def get_exitcode(self):
        return self.returncode

    
