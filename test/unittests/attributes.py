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
class AttributeTests(unittest.TestCase):
    """
    Tests for the saga.AttributeInterface API
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
    def test_job_desc(self):

        d = saga.job.Description() 
        d.executable = 'A'
        d.arguments  = ['b', 'c']
        
        if str(d) != "{'executable': 'A', 'arguments': ['b', 'c']}" :
            self.fail("Unexpected string representation: %s"  %  str(d))

