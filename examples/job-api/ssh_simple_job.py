#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit an SSH job 
   using a custom security context.

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/saga-project/bliss/issues
'''

__author__    = "Ashley Zebrowski"
__copyright__ = "Copyright 2012, Ashley Zebrowski"
__license__   = "MIT"

import sys, time
import bliss.saga as saga

def main():
    
    try:
        # Optional:
        # Set up a security context
        # if no security context is defined, the SFTP
        # plugin will pick up the default set of ssh 
        # credentials of the user, i.e., ~/.ssh/id_rsa
        #
        #ctx = saga.Context()
        #ctx.type = saga.Context.SSH
        #ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        #ctx.userkey = '/Users/oweidner/.ssh/rsa_work' # like ssh -i ...'
   
        # Optional:  
        # Append the custom security context to the session
        #session = saga.Session()
        #session.contexts.append(ctx)
 
        # create a job service for Futuregrid's 'alamo' machine
        # and attach the SSH security context to it
        js = saga.job.Service("ssh://alamo.futuregrid.org")
        # Alternatively: 
        # Use custom session 
        #js = saga.job.Service("ssh://alamo.futuregrid.org", session=session)

        # describe our job
        jd = saga.job.Description()

        # environment, executable & arguments
        jd.environment = {'SLEEP_TIME':'10'}       
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['$SLEEP_TIME']

        # output options
        jd.output = "bliss_ssh_job.stdout"
        jd.error  = "bliss_ssh_job.stderr"

        # create the job (state: New)
        myjob = js.create_job(jd)

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...starting job...\n"
        # run the job (submit the job via SSH)
        myjob.run()

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...waiting for job...\n"
        # wait for the job to either finish or fail
        myjob.wait()

        print "Job State : %s" % (myjob.get_state())
        print "Exitcode  : %s" % (myjob.exitcode)

    except saga.Exception, ex:
        print "An error occured during job execution: %s" % (str(ex))
        sys.exit(-1)

if __name__ == "__main__":
    main()
