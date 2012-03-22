#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a job to an SGE 
   jobmanager via ssh using a custom security context.

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=4 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import time
import bliss.saga as saga

def main():
    
    try:
        # set up a security context (optional)
        # if no security context is defined, the PBS
        # plugin will pick up the default set of ssh 
        # credentials of the user, i.e., ~/.ssh/id_rsa
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'tg802352' # like 'ssh username@host ...'
#        ctx.usercert = '/home1/01125/yye00/.ssh/id_rsa' # like ssh -i ...'
 
        # create a job service for TACC's 'lonestar' SGE cluster
        # and attach the SSH security context to it
        js = saga.job.Service("sge+ssh://lonestar.tacc.utexas.edu") # replace with lonestar
        js.session.contexts.append(ctx)

        # describe our job
        jd = saga.job.Description()
        # project to use
        jd.project = "TG-MCB090174"
       
        jd.queue   = "development"

        # resource requirements
        jd.wall_time_limit  = 5 # minutes
        jd.total_cpu_count = 12
        # the email notification
        jd.contact = "oweidner@cct.lsu.edu" 
        # environment, executable & arguments
        jd.environment = {'SLEEP_TIME':'10'}       
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['$SLEEP_TIME']
        # output options
        jd.output = "bliss_sgessh_job.stdout"
        jd.error  = "bliss_sgessh_job.stderr"

        # create the job (state: New)
        myjob = js.create_job(jd)

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...starting job...\n"
        # run the job (submit the job to PBS)
        myjob.run()

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...waiting for job...\n"
        # wait for the job to either finish or fail
        myjob.wait()

        print "Job State : %s" % (myjob.get_state())
        print "Exitcode  : %s" % (myjob.exitcode)

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

