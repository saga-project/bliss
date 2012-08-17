#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import time
import bliss.saga as saga

def run_bfast_p(numjobs, session, jobservice):
   
    bfast_base_dir = saga.Url("sftp://queenbee.loni.org/work/oweidner/bfast")
 
    try:
        container = saga.job.Container(jobservice)

        for jobno in range(0, numjobs):
            workdir = "%s/tmp/run/%s" % (bfast_base_dir.path, str(int(time.time())))
            basedir = saga.filesystem.Directory(bfast_base_dir, session=session)
            basedir.make_dir(workdir)

            jd = saga.job.Description()
            jd.wall_time_limit   = 5 #minutes
            jd.total_cpu_count   = 1     
            jd.environment       = {'BFAST_DIR':bfast_base_dir.path}
            jd.working_directory = workdir     
            jd.executable        = '$BFAST_DIR/bin/bfast'
            jd.arguments         = ['match', '-A 1',
                                    '-r $BFAST_DIR/data/small/reads_5K/reads.10.fastq',
                                    '-f $BFAST_DIR/data/small/reference/hg_2122.fa']

            container.add(js.create_job(jd))
            print "Added job #%s with working directory '%s' to container"\
              % (jobno, workdir)

        cstart = time.time()
        container.run()
        cdiff = time.time()-cstart
        start = time.time()
        print "Container with %s jobs started. It took %.0fs." % (numjobs, cdiff)

        container.wait()

        diff = time.time()-start
        print "Container finished running. Elapsed time: %.0fs."\
          % (diff)

        return diff

    except saga.Exception, ex:
        print "An error occured: %s" % (str(ex))
        sys.exit(-1)


if __name__ == "__main__":

    NUMJOBS = 32

    execution_host = saga.Url("pbs+ssh://queenbee.loni.org") 
    ctx = saga.Context()
    ctx.context_type = saga.Context.SSH
    ctx.user_id  = 'oweidner' # like 'ssh username@host ...'
    ctx.user_key = '/Users/s1063117/.ssh/id_rsa' # like ssh -i ...'

    session = saga.Session()
    session.contexts.append(ctx)

    js = saga.job.Service(execution_host, session)
 
    for i in range (0, 32): 
        print "\n-------------------------------------"
        print "Submitting %s jobs in parallel\n" % NUMJOBS
 
        total_time = run_bfast_p(NUMJOBS, session, js)

        print "\n-------------------------------------"
        print "Total elapsed time: %.0fs\n" % total_time

