#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a group of job to 
   a PBS jobmanager via ssh using a job container.

   Job containers are implemented by a Bliss job plugin
   and hence can behave differently between different 
   implementations. In the case of the PBS plugin, 
   the startup time for a container of n jobs is equivalent
   with the startup time for n indivdual jobs. Hoever, the
   wait() implementation is for n jobs is much faster than 
   calling wait() for each job individually. 

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import time
import bliss.saga as saga

def main():
    
    try:
        # set up the security context:
        # if no security context is defined, the PBS
        # plugin will pick up the default set of ssh 
        # credentials of the user, i.e., ~/.ssh/id_rsa
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        ctx.usercert = '/Users/oweidner/.ssh/id_rsa' # like ssh -i ...'
 
        # create a job service for Futuregrid's 'india' PBS cluster
        # and attach the SSH security context to it
        js = saga.job.Service("pbs+ssh://alamo.futuregrid.org")
        js.session.contexts.append(ctx)

        # describe our job
        jd = saga.job.Description()
        # resource requirements
        jd.walltime_limit  = "0:05:00"
        jd.total_cpu_count = 1     
        # environment, executable & arguments
        jd.environment = {'SLEEP_TIME':'10'}       
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['$SLEEP_TIME']

        # create a new job container
        container = saga.job.Container(js)

        # create 16 jobs
        for i in range(16):
            container.add(js.create_job(jd))

        print "\n...starting jobs...\n"
        container.run()

        print "\n...waiting for jobs...\n" 
        container.wait(saga.job.WaitMode.All)

        for job in container.list():
            print "Job ID %s (State: %s)" \
              % (job.jobid, job.get_state())

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

