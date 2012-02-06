#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to use the 'PBSBigJob+SSH' pilot 
   job via the SAGA resource API.

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered an issue with the code, 
   please report it: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import time
import bliss.saga as saga

def main():
    
    try:
        # Set up a security context (optional). If no security context 
        # is defined, the BigJobSSH plugin will pick up the default set 
        # of ssh credentials for the user, i.e., ~/.ssh/id_rsa
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        ctx.usercert = '/Users/oweidner/.ssh/id_rsa_fg' # like ssh -i ...'
 
        # Create a resource manager for Futuregrid's 'india' PBS cluster
        # and attach the SSH security context to it
        rm = saga.resource.Manager("pbsbigjob+ssh://alamo.futuregrid.org")
        rm.session.contexts.append(ctx)


        # Next, define a compute resource with 64 cores.
        cdesc = saga.resource.ComputeDescription()
        cdesc.cores = '64'

        # Now we can create a compute resource object from the 
        # description and wait for it to reach 'Active' state.
        cr64 = rm.create_compute(cdesc)
        cr64.wait(saga.resource.State.Active)

        # Create a job service from the compute resource
        js = saga.job.Service.from_compute(cr64)

        # describe our job
        jd = saga.job.Description()
        # resource requirements
        jd.wall_time_limit  = "0:05:00"
        jd.total_cpu_count = 1     
        # environment, executable & arguments
        jd.environment = {'SLEEP_TIME':'10'}       
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['$SLEEP_TIME']
        # output options
        jd.output = "bliss_pbssh_job.stdout"
        jd.error  = "bliss_pbssh_job.stderr"

        

        #print "Job ID    : %s" % (myjob.jobid)
        #print "Job State : %s" % (myjob.get_state())

        #print "\n...starting job...\n"
        # run the job (submit the job to PBS)
        #myjob.run()

        #print "Job ID    : %s" % (myjob.jobid)
        #print "Job State : %s" % (myjob.get_state())

        #print "\n...waiting for job...\n"
        # wait for the job to either finish or fail
        #myjob.wait()

        #print "Job State : %s" % (myjob.get_state())
        #print "Exitcode  : %s" % (myjob.exitcode)


        # Finally, we can release the compute resource
        rm.release_compute(cr64)

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

