#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a job to a PBS 
   jobmanager via ssh using the 'pythonic' version of the API. 
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga

def main():
    
    try:
        # set up the security context
        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner'
        ctx.usercert = '/Users/oweidner/.ssh/id_rsa'
 
        # start a local job service
        js = saga.job.Service("pbs+ssh://india.futuregrid.org")
        js.session.contexts.append(ctx)

        # describe our job
        jd = saga.job.Description()
        jd.set_attribute("Executable", '/bin/date')
        jd.output = "pbsjob.stdout"
        jd.error  = "pbsjob.stderr"

        # create & run the job
        myjob = js.create_job(jd)

        print "Job State : %s" % (myjob.get_state())

        myjob.run()

        print "Job ID    : %s" % (myjob.jobid)
        print "Job State : %s" % (myjob.get_state())
        
        print "...waiting for job..."
        myjob.wait()

        print "Job State : %s" % (myjob.get_state())
        print "Exitcode  : %s" % (myjob.get_attribute("Exitcode"))

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s" % (str(ex))
        print "Traceback: %s" % ex.traceback

if __name__ == "__main__":
    main()

