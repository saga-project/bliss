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
        run_id = str(int(time.time()))
        # create a working directory on the remote machine
        workdir = "%s/tmp/run/%s" % (bfast_base_dir.path, run_id)
        basedir = saga.filesystem.Directory(bfast_base_dir, session=session)
        basedir.make_dir(workdir)

        jd = saga.job.Description()
        jd.wall_time_limit   = "0:05:00"
        jd.total_cpu_count   = 1     
        jd.environment       = {'BFAST_DIR':bfast_base_dir.path}
        jd.working_directory = workdir     
        jd.output            = 'bfast.out'     
        jd.error             = 'bfast.err' 
        jd.executable        = '$BFAST_DIR/bin/bfast'
        jd.arguments         = ['match', '-A 1',
                                '-r $BFAST_DIR/data/small/reads_5K/reads.10.fastq',
                                '-f $BFAST_DIR/data/small/reference/hg_2122.fa']

        myjob = js.create_job(jd)
        myjob.run()

        start = time.time()
        print "\nJob #%s started with ID '%s' and working directory: '%s'"\
          % (jobno, myjob.jobid, workdir)

        myjob.wait()

        diff = time.time()-start
        print "Job #%s with ID '%s' finished (RC: %s). Elapsed time: %.0fs"\
          % (jobno, myjob.jobid, myjob.exitcode, diff)

        # copy output and error files back to the local machine
        local_file = saga.Url('sftp://localhost//tmp/bfast.out.'+run_id)
        basedir.copy(workdir+'/bfast.out', local_file)
        print "Job #%s output copied to local machine: %s (%s bytes)" \
          % (jobno, local_file, basedir.get_size(workdir+'/bfast.out'))

        return diff

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":

    NUMJOBS = 32

    execution_host = saga.Url("pbs+ssh://queenbee.loni.org") 
    ctx = saga.Context()
    ctx.type = saga.Context.SSH
    ctx.userid  = 'oweidner' # like 'ssh username@host ...'
    ctx.userkey = '/Users/s1063117/.ssh/id_rsa' # like ssh -i ...'

    session = saga.Session()
    session.contexts.append(ctx)

    js = saga.job.Service(execution_host, session)
  
    print "\n-------------------------------------"
    print "Submitting %s jobs sequentially" % NUMJOBS
 
    total_time = 0.0 

    for i in range (0, NUMJOBS):
        total_time += run_bfast(i, session, js)

    print "\n-------------------------------------"
    print "Total elapsed time: %.0fs\n" % total_time

