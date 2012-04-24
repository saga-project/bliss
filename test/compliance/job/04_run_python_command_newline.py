#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import sys
import bliss.saga as saga

def run(url):
    """Test if we can execute a remote python script via 'python -c'
    """
    try:
        js = saga.job.Service(url)
    
        # describe our job
        jd = saga.job.Description()

        # environment, executable & arguments
        jd.environment = {'MYOUTPUT':'"Hello from Bliss"'}       
        jd.executable  = 'python'
        jd.arguments   = ['-c', '"import sys \nimport os \nprint os.environ[\\"MYOUTPUT\\"] \nprint sys.version"']

        # output options
        jd.output = "bliss_job.04.stdout"
        jd.error  = "bliss_job.04.stderr"

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

        failed = False
        why = ""
        if myjob.get_state() != saga.job.Job.Done:
            failed = True
            why = "Job returned in state 'Failed'."

    except saga.Exception, ex:
        failed = True
        why = str(ex)

    if failed == True:
       print ""
       print "============================================"
       print "The job seems to have FAILED!"
       print "============================================"
       print "                                            "
       print "%s" % (why)
       print "Please run this test again with SAGA_VERBOSE=5 "
       print "and report the results at: "
       print ""
       print "https://github.com/saga-project/bliss/issues\n"

    else: 
      print ""
      print "============================================"
      print "The job seems to have executed successfully!"
      print "============================================"
      print "                                            "
      print "NOW, SOME MANUAL CHECKING IS REQUIRED!      "
      print "                                            "
      print "(1) Login to %s                             " % (url)
      print "(2) Make sure the file bliss_job.04.stdout exists"
      print "(3) Make sure bliss_job.04.stdout contains:"
      print "  Hello from Bliss" 
      print "  <Python interpreter version information>"
      print ""
      print "If (1)-(3) are ok, this test can be considered as PASSED\n"


def usage():
    print 'Usage: python run_remote_exe.py <URL>'
    sys.exit(-1)

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    run(args[0])

if __name__ == '__main__':
    main()
