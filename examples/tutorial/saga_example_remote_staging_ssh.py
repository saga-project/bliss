# https://github.com/saga-project/bliss/wiki/SAGA-Tutorial-Part-2%3A-Local-Job-Submission

import sys
import bliss.saga as saga

def main():
    try:
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # your identity on the remote machine
        #ctx.userkey = '/Users/oweidner/.ssh/rsa_work'

        ses = saga.Session()
        ses.contexts.append(ctx) 
        # create a job service for lonestar
        js = saga.job.Service("ssh://localhost")

        # describe our job
        jd = saga.job.Description()

        jd.environment       = {'MYOUTPUT':'"Hello from SAGA"'}       
        jd.executable        = '/bin/echo'
        jd.arguments         = ['$MYOUTPUT']
        jd.output            = "myjob.stdout"
        jd.error             = "myjob.stderr"

        # create the job (state: New)
        myjob = js.create_job(jd)

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...starting job...\n"
        # run the job 
        myjob.run()

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())

        print "\n...waiting for job...\n"
        # wait for the job to either finish or fail
        myjob.wait()

        print "Job State : %s" % (myjob.get_state())
        print "Exitcode  : %s" % (myjob.exitcode)

        outfilesource = 'sftp://localhost/Users/oweidner/myjob.stdout'
        outfiletarget = 'file://localhost/tmp/'
        out = saga.filesystem.File(outfilesource, session=ses)
        out.copy(outfiletarget)

        print "Staged out %s to %s (size: %s bytes)" % (outfilesource, outfiletarget, out.get_size())

    except saga.Exception, ex:
        print "An error occured during job execution: %s" % (str(ex))
        sys.exit(-1)

if __name__ == "__main__":
    main()
