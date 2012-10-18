#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a single BFAST 
   (bfast.sourceforge.net) genmoe matching job
   to a remote PBS cluster via pbs+ssh. This example 
   is the same as pbs_via_ssh_simple_job.py, except
   that it uses a differnet executable. 
  
   The example assuems that the BFAST executable and 
   data are present on the target system. 

   If something doesn't work as expected, try to set 
   SAGA_VERBOSE=3 in your environment before you run the
   script in order to get some debug output.

   If you think you have encountered a defect, please 
   report it at: https://github.com/saga-project/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
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

        # create a job service for Futuregrid's 'india' PBS cluster
        # and attach the SSH security context to it
        js = saga.job.Service("pbs+ssh://india.futuregrid.org")
        # Alternatively: 
        # Use custom session 
        #js = saga.job.Service("pbs+ssh://india.futuregrid.org", session=session)

        # Describe our job
        jd = saga.job.Description()
        # ... resource requirements
        jd.wall_time_limit  = 5 #minutes
        jd.total_cpu_count = 1     
        # ... evironment, executable & arguments
        jd.environment       = {'BFAST_DIR':'/N/u/oweidner/software/bfast'}
        jd.working_directory = '/N/u/oweidner/software/bfast/tmp/'     
        jd.executable        = '$BFAST_DIR/bin/bfast'
        jd.arguments         = ['match', '-A 1',
                                '-r $BFAST_DIR/data/small/reads_5K/reads.10.fastq',
                                '-f $BFAST_DIR/data/small/reference/hg_2122.fa']
        # ... output options
        localtime = time.time()
        jd.output = "bfast_match_%s.stdout" % localtime
        jd.error  = "bfast_match_%s.stderr" % localtime

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
        print "An error occured during job execution: %s" % (str(ex))
        sys.exit(-1)

if __name__ == "__main__":
    main()

