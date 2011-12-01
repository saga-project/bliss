#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to copy a file to a remote 
   host via ssh using a custom security context.

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

def main(jobno, session, jobservice):
   
    bfast_base_dir = saga.Url("sftp://queenbee.loni.org/work/oweidner/bfast")
 
    try:
        workdir = "%s/tmp/run/%s" % (bfast_base_dir.path, str(int(time.time())))
        basedir = saga.filesystem.Directory(bfast_base_dir, session=session)
        basedir.make_dir(workdir)

        jd = saga.job.Description()
        jd.wall_time_limit   = "0:05:00"
        jd.total_cpu_count   = 1     
        jd.environment       = {'BFAST_DIR':bfast_base_dir.path}
        jd.working_directory = workdir     
        jd.executable        = '$BFAST_DIR/bin/bfast'
        jd.arguments         = ['match', '-A 1',
                                '-r $BFAST_DIR/data/small/reads_5K/reads.10.fastq',
                                '-f $BFAST_DIR/data/small/reference/hg_2122.fa']

        myjob = js.create_job(jd)
        myjob.run()

        time.sleep(1)
        print "Job #%s started with ID '%s' and working directory: '%s'"\
          % (jobno, myjob.jobid, workdir)

        myjob.wait()

        print "Job #%s with ID '%s' finished (RC: %s). Output available in: '%s'"\
          % (jobno, myjob.jobid, myjob.exitcode, workdir)

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))

if __name__ == "__main__":

    execution_host = saga.Url("pbs+ssh://queenbee.loni.org") 
    ctx = saga.Context()
    ctx.type = saga.Context.SSH
    ctx.userid  = 'oweidner' # like 'ssh username@host ...'
    ctx.usercert = '/Users/s1063117/.ssh/id_rsa' # like ssh -i ...'

    session = saga.Session()
    session.contexts.append(ctx)

    js = saga.job.Service(execution_host, session)
    

    for i in range (0,64):
        main(i, session, js)

