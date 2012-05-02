#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga
import unittest

###############################################################################
#
class ContextTests(unittest.TestCase):
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
    def test_context_type_SSH(self):

        c1 = saga.Context()
        c1.type = saga.Context.SSH
        c1.userkey="/Users/s1063117/id_rsa"
        s1 = saga.Session()
        s1.add_context(c1)

        s1.add_context(c1)
        s1.add_context(c1)

        js = saga.job.Service("fork://localhost")
        js_s = js.get_session()
        js_s.add_context(c1)

        jk = saga.job.Service("fork://localhost")
        found = False
        for ctx in js.get_session().list_contexts():
            if ctx.type == saga.Context.SSH:
                if ctx == c1:
                    found = True
                    assert(ctx.userkey == "/Users/s1063117/id_rsa")

        if not found:
            self.fail("Coulnd't find context!")

    ###########################################################################
    #
    def test_context_type_EC2(self):

        c1 = saga.Context()
        c1.type = saga.Context.EC2
        c1.userkey  ="/Users/s1063117/ec2_key"
        c1.usercert ="/Users/s1063117/ec2_cert"        
        s1 = saga.Session()
        s1.add_context(c1)

        s1.add_context(c1)
        s1.add_context(c1)

        js = saga.job.Service("fork://localhost")
        js_s = js.get_session()
        js_s.add_context(c1)

        jk = saga.job.Service("fork://localhost")
        found = False
        for ctx in js.get_session().list_contexts():
            if ctx.type == saga.Context.EC2:
                if ctx == c1:
                    found = True
                    assert(ctx.userkey == "/Users/s1063117/ec2_key")
                    assert(ctx.usercert == "/Users/s1063117/ec2_cert")

        if not found:
            self.fail("Coulnd't find context!")
       
