#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
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
    def test_scalar_string_properties(self):
        """
        Tests the saga.job.description attribute interface (scalar string attributes)
        """
 
        properties = {"Executable"       : "executable",
                      "Queue"            : "queue",
                      "Project"          : "project",
                      "Output"           : "output",
                      "Error"            : "error",
                      "WorkingDirectory" : "working_directory",
                      "Contact"          : "contact",
                      "SPMDVariation"    : "spmd_variation",
        }

        try:
            svalue = 'jsaoiudjca89s7d'
            vvalue = ['sdsd', 'cus6v']
            jd = saga.job.Description()

            for (attr_key, attr_val) in properties.items():

                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
                if jd.attribute_exists(attr_key) != False:
                    self.fail("Attribute Error - should have been False")

                setattr(jd, attr_val, svalue)
                if getattr(jd, attr_val) != svalue:
                    self.fail("Attribute Error - unexpected value")
                if jd.get_attribute(attr_key) != svalue:
                    self.fail("Attribute Error - unexpected value")

                with self.assertRaises(saga.Exception):
                    setattr(jd, attr_val, 12)  # shouldn't accept anything but str

                jd.set_attribute(attr_key, "XX")
                if getattr(jd, attr_val) != "XX":
                    self.fail("Attribute Error - unexpected value")

                jd.remove_attribute(attr_key)
                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
 
        except saga.Exception, e: 
            self.fail(e)

    ###########################################################################
    #
    def test_scalar_int_properties(self):
        """
        Tests the saga.job.description attribute interface (scalar int attributes)
        """
 
        properties = {"TotalCPUCount"    : "total_cpu_count",
                      "NumberOfProcesses": "number_of_processes",
                      "WallTimeLimit"    : "wall_time_limit"
        }

        try:
            svalue = 123423
            vvalue = [5345, 567567]
            jd = saga.job.Description()

            for (attr_key, attr_val) in properties.items():

                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
                if jd.attribute_exists(attr_key) != False:
                    self.fail("Attribute Error - should have been False")

                setattr(jd, attr_val, svalue)
                if getattr(jd, attr_val) != svalue:
                    self.fail("Attribute Error - unexpected value")
                if jd.get_attribute(attr_key) != svalue:
                    self.fail("Attribute Error - unexpected value")

                with self.assertRaises(saga.Exception):
                    setattr(jd, attr_val, "adads")  # shouldn't accept anything but int

                jd.set_attribute(attr_key, 16)
                if getattr(jd, attr_val) != 16:
                    self.fail("Attribute Error - unexpected value")

                jd.remove_attribute(attr_key)
                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
 
        except saga.Exception, e: 
            self.fail(e)

    ###########################################################################
    #
    def test_vector_dict_properties(self):
        """
        Tests the saga.job.description attribute interface (vector 'dict' attributes)
        """
 
        properties = {"Environment"    : "environment",
        }

        try:
            svalue = {'foo':'bar'}
            vvalue = [{'key1':'val1'}, {'key2':'val2'}]
            jd = saga.job.Description()

            for (attr_key, attr_val) in properties.items():

                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
                if jd.attribute_exists(attr_key) != False:
                    self.fail("Attribute Error - should have been False")

                setattr(jd, attr_val, svalue)
                if getattr(jd, attr_val) != svalue:
                    self.fail("Attribute Error - unexpected value")
                if jd.get_vector_attribute(attr_key) != svalue:
                    self.fail("Attribute Error - unexpected value")

                with self.assertRaises(saga.Exception):
                    setattr(jd, attr_val,["ss", "gg"])  # shouldn't accept anything but int

                jd.set_vector_attribute(attr_key, {"x":"z"})
                if getattr(jd, attr_val) != {"x":"z"}:
                    self.fail("Attribute Error - unexpected value")

                jd.remove_attribute(attr_key)
                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
 
        except saga.Exception, e: 
            self.fail(e)



    ###########################################################################
    #
    def test_vector_list_properties(self):
        """
        Tests the saga.job.description attribute interface (vector 'dict' attributes)
        """
 
        properties = {"Arguments"    : "arguments",
        }

        try:
            svalue = ['foo','bar']
            vvalue = [['key1','val1'], ['key2','val2']]
            jd = saga.job.Description()

            for (attr_key, attr_val) in properties.items():

                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
                if jd.attribute_exists(attr_key) != False:
                    self.fail("Attribute Error - should have been False")

                setattr(jd, attr_val, svalue)
                if getattr(jd, attr_val) != svalue:
                    self.fail("Attribute Error - unexpected value")
                if jd.get_vector_attribute(attr_key) != svalue:
                    self.fail("Attribute Error - unexpected value")

                with self.assertRaises(saga.Exception):
                    setattr(jd, attr_val, {"ss":"gg"})  # shouldn't accept anything but list

                jd.set_vector_attribute(attr_key, ["x","z"])
                if getattr(jd, attr_val) != ["x","z"]:
                    self.fail("Attribute Error - unexpected value")

                jd.remove_attribute(attr_key)
                if getattr(jd, attr_val) != None:
                    self.fail("Attribute Error - should have been None")
 
        except saga.Exception, e: 
            self.fail(e)

