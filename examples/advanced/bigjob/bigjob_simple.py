#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a job to a bigjob 
   service using an (optional) custom security context. 

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import time
import bliss.saga as saga

def main():
    
    try:
        # set up a security context (optional) that describes 
        # our log-in credentials for the bigjob service. 
        # if the bigjob service doesn't have security enabled,
        # this is not necessary. 
        ctx = saga.Context()
        ctx.type = saga.Context.BigJob
        ctx.userid   = 'oweidner' 
        ctx.userpass = 'indianpaleale'

        session = saga.Session()
        session.contexts.append(ctx)

        # create a job service that connects to a bigjob 
        # server running.
        js = saga.job.Service("bigjob://engage-submit3.renci.org:28082/engage.fork.test", session=session)

        # describe our job
        jd = saga.job.Description()
        # resource requirements
        jd.wall_time_limit  = "0:05:00"
        jd.number_of_processes = 1     
        # environment, executable & arguments
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['10']
        # output options
        jd.output = "bigjob_via_saga_api.stdout"
        jd.error  = "bigjob_via_saga_api.stderr"

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

