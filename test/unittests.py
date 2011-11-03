#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import sys
import unittest

# import the test cases
from api import *

if __name__ == '__main__':
    suite_job = unittest.TestLoader().loadTestsFromTestCase(JobDescriptionTests)
    alltests = unittest.TestSuite([suite_job])
    result = unittest.TextTestRunner(verbosity=10).run(alltests)
    sys.exit(not result.wasSuccessful())
