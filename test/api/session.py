#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga
import unittest

###############################################################################
#
class SessionTests(unittest.TestCase):
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
    def test_session(self):

        js = saga.job.Description()
        jd = saga.job.Description()
        
        if js.get_session() != jd.get_session():
            self.fail("Both objects should return the same (default) session")

        if js.get_session() != saga.Object._Object__shared_state["default_session"]:
            self.fail("Object should return default session")

        if jd.get_session() != saga.Object._Object__shared_state["default_session"]:
            self.fail("Object should return default session")

        js = saga.job.Service("fork://localhost")
        if js.get_session() != saga.Object._Object__shared_state["default_session"]:
            self.fail("Object should return default session")

        js = saga.job.Service("fork://localhost", session=saga.Session())
        if js.get_session() == saga.Object._Object__shared_state["default_session"]:
            self.fail("Object should not return default session")


        c1 = saga.Context()
        s1 = saga.Session()
        s1.add_context(c1)

        if len(s1.list_contexts()) != 1:
            self.fail("Context list length should be 1")

        s1.remove_context(c1)
        
        if len(s1.list_contexts()) != 0:
            self.fail("Context list length should be 0")

        s2 = saga.Session()

        js1 = saga.job.Service("fork://localhost", session=s1)
        js2 = saga.job.Service("fork://localhost", session=s2)
   
        if js1.get_session() == js2.get_session():
            self.fail("Sessions shouldn't be identical")

       

