#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import time
import bliss.saga as saga

def run_bfast(jobno, session, jobservice):
   
    bfast_base_dir = saga.Url("sftp://queenbee.loni.org/work/oweidner/bfast")
 
    try:
        # create a working directory on the remote machine
        workdir = "%s/tmp/run/%s" % (bfast_base_dir.path, str(int(time.time())))
        basedir = saga.filesystem.Directory(bfast_base_dir, session=session)
        basedir.make_dir(workdir)

        jd = saga.job.Description()
        jd.wall_time_limit   = "0:05:00"
        jd.total_cpu_count   = 1     
        jd.environment       = {'BFAST_DIR':bfast_base_dir.path}
        jd.working_directory = workdir     
        jd.output            = 'bfast.out'     
        jd.error             = 'bfast.err' 
        jd.executable        = '/bin/date'#$BFAST_DIR/bin/bfast'
        #jd.arguments         = ['match', '-A 1',
        #                        '-r $BFAST_DIR/data/small/reads_5K/reads.10.fastq',
        #                        '-f $BFAST_DIR/data/small/reference/hg_2122.fa']

        myjob = js.create_job(jd)
        myjob.run()

        start = time.time()
        print "Job #%s started with ID '%s' and working directory: '%s'"\
          % (jobno, myjob.jobid, workdir)

        myjob.wait()

        diff = time.time()-start
        print "Job #%s with ID '%s' finished (RC: %s). Elapsed time: %.0fs"\
          % (jobno, myjob.jobid, myjob.exitcode, diff)

        # copy output and error files back to the local machine
        basedir.copy(workdir+'/bfast.*', 'sftp://localhost//tmp/')

        return diff

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":

    NUMJOBS = 2

    execution_host = saga.Url("pbs+ssh://queenbee.loni.org") 
    ctx = saga.Context()
    ctx.type = saga.Context.SSH
    ctx.userid  = 'oweidner' # like 'ssh username@host ...'
    ctx.usercert = '/Users/s1063117/.ssh/id_rsa' # like ssh -i ...'

    session = saga.Session()
    session.contexts.append(ctx)

    js = saga.job.Service(execution_host, session)
  
    print "\n-------------------------------------"
    print "Submitting %s jobs sequentially\n" % NUMJOBS
 
    total_time = 0.0 

    for i in range (0, NUMJOBS):
        total_time += run_bfast(i, session, js)

    print "\n-------------------------------------"
    print "Total elapsed time: %.0fs\n" % total_time

