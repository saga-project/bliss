#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import sys
import getpass
import bliss.saga as saga

def run(url, username, queue, project):
    """Test if we can execute a remote bash script via 'bash -c'
    """
    try:
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = username # like 'ssh username@host ...'

        js = saga.job.Service(url)
        js.session.contexts.append(ctx)

        # describe our job
        jd = saga.job.Description()

        jd.queue   = queue
        jd.project = project
        jd.wall_time_limit = 5 # minutes
    
        # environment, executable & arguments
        jd.environment = {'MYOUTPUT':'"Hello from Bliss"'}       
        jd.executable  = '/bin/echo'
        jd.arguments   = ['$MYOUTPUT']

        # output options
        jd.output = "bliss_job.01.stdout"
        jd.error  = "bliss_job.01.stderr"

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
      print "(2) Make sure the file bliss_job.01.stdout exists"
      print "(3) Make sure bliss_job.01.stdout contains the string 'Hello from Bliss'"
      print ""
      print "If (1)-(3) are ok, this test can be considered as PASSED\n"


def usage():
    print 'Usage: python %s ' % __file__
    print '                <URL>'
    print '                <REMOTEUSERNAME (default: local username)>'
    print '                <QUEUE (default: None)>'
    print '                <PROJECT (default: None)>'

def main():
    remoteusername = getpass.getuser()
    queue = None
    project = None
    js_url = None

    args = sys.argv[1:]
    if len(args) < 1:
        usage()
        sys.exit(-1)
    else:
        js_url = args[0]

    try:
        remoteusername = args[1]
        queue = args[2]
        project = args[3]
    except IndexError:
        pass 

    run(js_url, remoteusername, queue, project)

if __name__ == '__main__':
    main()
