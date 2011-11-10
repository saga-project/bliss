#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga
import unittest

###############################################################################
#
class JobDescriptionTests(unittest.TestCase):
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
    def test_scalar_properties(self):
        """
        Tests for the saga.job.description attribute interface 
        """
 
        properties = {"Executable" : "executable",
                      "Queue"      : "queue",
                      "Project"    : "project",
                      "Output"     : "output",
                      "Error"      : "error"}

        try:
            svalue = 'jsaoiudjca89s7d'
            vvalue = ['sdsd', 'cus6v']
            jd = saga.job.Description()

            for attrib in properties:

                if getattr(jd, 'executable') != None:
                    self.fail("Attribute Error - should have been None")
                if jd.attribute_exists("Executable") != False:
                    self.fail("Attribute Error - should have been False")

                setattr(jd, 'executable', svalue)
                if getattr(jd, 'executable') != svalue:
                    self.fail("Attribute Error - unexpected value")
                if jd.get_attribute("Executable") != svalue:
                    self.fail("Attribute Error - unexpected value")

                jd.set_attribute("Executable", "XX")
                if getattr(jd, 'executable') != "XX":
                    self.fail("Attribute Error - unexpected value")

                jd.remove_attribute("Executable")
                if getattr(jd, 'executable') != None:
                    self.fail("Attribute Error - should have been None")
 
        except saga.Exception, e: 
            self.fail(e)
             
