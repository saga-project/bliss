# https://github.com/saga-project/bliss/wiki/SAGA-Tutorial-Part-2%3A-Local-Job-Submission

import sys
import bliss.saga as saga

def main():
    try: 
        # create a job service for lonestar
        js = saga.job.Service("fork://localhost")

        # describe our job
        jd = saga.job.Description()

        jd.environment     = {'MYOUTPUT':'"Hello from SAGA"'}       
        jd.executable      = '/bin/echo'
        jd.arguments       = ['$MYOUTPUT']
        jd.output          = "my1stjob.stdout"
        jd.error           = "my1stjob.stderr"

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

    except saga.Exception, ex:
        print "An error occured during job execution: %s" % (str(ex))
        sys.exit(-1)

if __name__ == "__main__":
    main()
