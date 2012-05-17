# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import sys
import unittest

# import the test cases
from unittests import *

if __name__ == '__main__':

    # All non-package tests (session, context, etc)
    suite_lnf = unittest.TestLoader().loadTestsFromTestCase(SessionTests)
    suite_lnf.addTests(unittest.TestLoader().loadTestsFromTestCase(ContextTests))
    suite_lnf.addTests(unittest.TestLoader().loadTestsFromTestCase(ExceptionTests))
    suite_lnf.addTests(unittest.TestLoader().loadTestsFromTestCase(UrlTests))
    suite_lnf.addTests(unittest.TestLoader().loadTestsFromTestCase(AttributeTests))

    # Job package tests
    suite_job = unittest.TestLoader().loadTestsFromTestCase(JobDescriptionTests)

    alltests = unittest.TestSuite([suite_lnf, 
                                   suite_job])

    result = unittest.TextTestRunner(verbosity=10).run(alltests)
    sys.exit(not result.wasSuccessful())
