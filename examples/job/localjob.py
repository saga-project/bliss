#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''This examples shows how to submit a simple job to the 
   local machine.
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga

def main():
    
    try: 
        # start a local job service
        js = saga.job.Service("fork://localhost")

        # describe our job
        jd = saga.job.Description()
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['10']

        # create & run the job
        myjob = js.create_job(jd)

        print "Job State : {!s}".format(myjob.get_state())

        myjob.run()

        print "Job ID    : {!s}".format(myjob.get_job_id())
        print "Job State : {!s}".format(myjob.get_state())
        print "waiting for job ..."

        myjob.wait()

        print "Job State : {!s}".format(myjob.get_state())

    except saga.Exception, ex:
        print "Oh, snap! An error occured: {!s}".format(str(ex))

    ## do it the old-school way 
    ## (compatible with CCT's SAGA Python bindings
    
    try: 
        # define lower-case aliases 
        saga.exception = saga.exception.Exception
        saga.job.service = saga.job.service.Service
        saga.job.description = saga.job.description.Description

        # start a local job service
        js = saga.job.service("fork://localhost")

        # describe our job
        jd = saga.job.description()
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['10']

        # create & run the job
        myjob = js.create_job(jd)

        print "Job State : {!s}".format(myjob.get_state())

        myjob.run()

        print "Job ID    : {!s}".format(myjob.get_job_id())
        print "Job State : {!s}".format(myjob.get_state())
        print "waiting for job ..."

        myjob.wait()

        print "Job State : {!s}".format(myjob.get_state())

    except saga.exception, ex:
        print "Oh, snap! An error occured: {!s}".format(str(ex))


if __name__ == "__main__":
    main()

