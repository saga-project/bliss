# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga
import os
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
        FILE1 = open("/tmp/bliss-test.file1", "w", 0)
        FILE1.close()
        FILE2 = open("/tmp/bliss-test.file2", "w", 0)
        FILE2.close()


    def tearDown(self):
        # Fixture:
        # called immediately after the test method has been called
        if os.path.isfile("/tmp/bliss-test.file1"):
            os.remove("/tmp/bliss-test.file1")
        if os.path.isfile("/tmp/bliss-test.file2"):
            os.remove("/tmp/bliss-test.file2")


    ###########################################################################
    #
    def test_context_type_SSH(self):

        c1 = saga.Context()
        c1.type = saga.Context.SSH
        c1.userkey=("/tmp/bliss-test.file1")
        try:
            c1.userkey=("non_existing_file_2345435")
            self.fail("'userkey' shouldn't accept a non-exsisting file'")
        except saga.Exception, e: 
            pass

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
                    assert(ctx.userkey == "/tmp/bliss-test.file1")

        if not found:
            self.fail("Coulnd't find context!")

    ###########################################################################
    #
    def test_context_type_EC2(self):

        c1 = saga.Context()
        c1.type = saga.Context.EC2
        c1.userkey  = "/tmp/bliss-test.file1"
        try:
            c1.userkey=("non_existing_file_2345435")
            self.fail("'userkey' shouldn't accept a non-exsisting file'")
        except saga.Exception, e: 
            pass

        c1.usercert = "/tmp/bliss-test.file2"        
        try:
            c1.usercert=("non_existing_file_2345435")
            self.fail("'usercert' shouldn't accept a non-exsisting file'")
        except saga.Exception, e: 
            pass

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
                    assert(ctx.userkey == "/tmp/bliss-test.file1")
                    assert(ctx.usercert == "/tmp/bliss-test.file2")

        if not found:
            self.fail("Coulnd't find context!")

    ###########################################################################
    #
    def test_context_type_X509(self):

        c1 = saga.Context()
        c1.type = saga.Context.X509
        c1.userkey  = "/tmp/bliss-test.file1"
        try:
            c1.userkey=("non_existing_file_2345435")
            self.fail("'userkey' shouldn't accept a non-exsisting file'")
        except saga.Exception, e: 
            pass

        c1.usercert = "/tmp/bliss-test.file2"     
        try:
            c1.usercert=("non_existing_file_2345435")
            self.fail("'usercert' shouldn't accept a non-exsisting file'")
        except saga.Exception, e: 
            pass
   
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
            if ctx.type == saga.Context.X509:
                if ctx == c1:
                    found = True
                    assert(ctx.userkey == "/tmp/bliss-test.file1")
                    assert(ctx.usercert == "/tmp/bliss-test.file2")

        if not found:
            self.fail("Coulnd't find context!")

      
