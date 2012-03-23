#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga
import unittest

###############################################################################
#
class JobContainerTests(unittest.TestCase):
    """
    Tests for the saga.job.Description API
    """
    def setUp(self):
        # Fixture:
        # called immediately before calling the test method
        pass 

    def tearDown(self):
        # Fixture:
        # called immediately after the test method has been called
        pass

    ###########################################################################
    #
    def test_container(self):

        ctx = saga.Context()
        ctx.type = saga.Context.SSH
        ctx.userid  = 'oweidner' # like 'ssh username@host ...'
        ctx.userkey = '/Users/oweidner/.ssh/id_rsa_fg' # like ssh -i ...'
 
        # create a job service for Futuregrid's 'india' PBS cluster
        # and attach the SSH security context to it
        js = saga.job.Service("pbs+ssh://india.futuregrid.org")
        js.session.contexts.append(ctx)

        # describe our job
        jd = saga.job.Description()
        # resource requirements
        jd.walltime_limit  = "0:05:00"
        jd.total_cpu_count = 1     
        # environment, executable & arguments
        jd.environment = {'SLEEP_TIME':'10'}       
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['$SLEEP_TIME']
        # output options
        jd.output = "bliss_pbssh_job.stdout"
        jd.error  = "bliss_pbssh_job.stderr"

        # create a new job container
        container = saga.job.Container(js)

        # create the job (state: New)
        myjob = js.create_job(jd)
        container.add(myjob)
        container.remove(myjob)

