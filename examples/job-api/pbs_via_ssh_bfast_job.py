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
   report it at: https://github.com/oweidner/bliss/issues
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
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
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'

        # create a job service for Futuregrid's 'india' PBS cluster
        # and attach the SSH security context to it
        js = saga.job.Service("pbs+ssh://india.futuregrid.org")
        js.session.contexts.append(ctx)

        # describe our job
        jd = saga.job.Description()
        # resource requirements
        jd.wall_time_limit  = 5 #minutes
        jd.total_cpu_count = 1     
        # environment, executable & arguments
        jd.environment       = {'BFAST_DIR':'/N/u/oweidner/bfast'}
        jd.working_directory = '/N/u/oweidner/bfast/tmp/'     
        jd.executable        = '$BFAST_DIR/bin/bfast'
        jd.arguments         = ['match', '-A 1',
                                '-r $BFAST_DIR/data/small/reads_5K/reads.10.fastq',
                                '-f $BFAST_DIR/data/small/reference/hg_2122.fa']
        # output options
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
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":
    main()

# INFO: The PBS script generated behind the scenes by the  
#       plugin looks like this (SAGA_VERBOSE=6 shows it):

#         #!/bin/bash 
#         #PBS -N bliss_job 
#         #PBS -V     
#         #PBS -v BFAST_DIR=/N/u/oweidner/bfast, 
#         #PBS -d /N/u/oweidner/bfast/tmp/ 
#         #PBS -o bfast_job_Sun_Nov_27_21:29:42_2011.stdout 
#         #PBS -e bfast_job_Sun_Nov_27_21:29:42_2011.stderr 
#         #PBS -l walltime=0:05:00 
#         #PBS -l nodes=1:ppn=8
# 
#         $BFAST_DIR/bin/bfast match -A 1 -r $BFAST_DIR/data/small/reads_5K/reads.10.fastq -f $BFAST_DIR/data/small/reference/hg_2122.fa 


