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
        jd.environment = {'MYOUTPUT':'"Hello from Bliss (via job container)"'}       
        jd.executable  = '/bin/echo'
        jd.arguments   = ['$MYOUTPUT']

        # create a new job container
        container = saga.job.Container(js)

        for i in range(4):
            jd.output = "bliss_container_job.%s.stdout" % str(i)
            jd.error  = "bliss_container_job.%s.stderr" % str(i)
            container.add(js.create_job(jd))

        print "\n...starting jobs...\n"
        container.run()

        print "\n...waiting for jobs...\n" 
        container.wait(saga.job.WaitMode.All)

        failed = False
        why = ""

        for job in container.list():
            print "Job ID %s (State: %s)" \
              % (job.jobid, job.get_state())
            if job.get_state() != saga.job.Job.Done:
                failed = True
                why = "Job returned with state '%s'."


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
      print "(3) Make sure bliss_job.01.stdout contains the string 'Hello from Bliss (via job container)'"
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
