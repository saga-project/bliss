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
class ExceptionTests(unittest.TestCase):
    """
    Tests for the saga.Exception class
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    ###########################################################################
    #
    def test_exception_properties(self):
    
        e1 = saga.Exception(saga.Error.NotImplemented, "Not Implemented!")

        try:
            e1.message = "set"
            self.fail("message should be read-only")

            e1.error = "set"
            self.fail("error should be read-only")

            e1.traceback = "set"
            self.fail("traceback should be read-only")

        except Exception, e:
            pass

        if e1.message != "Not Implemented!":
            self.fail("message contains the wrong string!")

        if e1.error != saga.Error.NotImplemented:
            self.fail("error contains the wrong type!")

        if e1.traceback != "(No Traceback)":
            self.fail("There shouldn't be a traceback!")

        print e1

    ###########################################################################
    #
    def test_exception_string_rep(self): 

        e1 = saga.Exception(saga.Error.NotImplemented, "Not Implemented")

        if str(e1) != "SAGA Exception (NotImplemented): Not Implemented":
            self.fail("Something's wrong with the string representation")

    ###########################################################################
    #
    def test_exception_string_rep(self): 

        e1 = saga.Exception(saga.Error.NotImplemented, "Not Implemented")

        if unicode(e1) != unicode("SAGA Exception (NotImplemented): Not Implemented"):
            self.fail("Something's wrong with the string representation")

    ###########################################################################
    #
    def test_exception_traceback(self):
   
        try:
            saga.job.Service("notgonnawork!")
        except saga.Exception, e:
            if e.traceback == "(No Traceback)":
                self.fail("There should be a traceback!")
            else:
                pass

