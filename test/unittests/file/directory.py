#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

import bliss.saga as saga
import unittest, os, uuid

###############################################################################
#
class FilesystemDirectoryTests(unittest.TestCase):
    """
    Tests for the saga.job.Description API
    """
    def setUp(self):
        # Fixture:
        # called immediately before calling the test method
        self._dir1 = "/tmp/"+str(uuid.uuid1())

    def tearDown(self):
        # Fixture:
        # called immediately after the test method has been called
        if os.path.exists(self._dir1):
            os.removedirs(self._dir1)

    ###########################################################################
    #
    def test_make_dir(self):
        """
        Tests directory.make_dir
        """

        try:
            d = saga.filesystem.Directory("sftp://localhost/")
            d.make_dir(self._dir1)
        except saga.Exception, ex:
            self.fail("Unexpected exception: %s" % ex)

        # now, make_dir should fail since the directoy already exists
        try:
            d.make_dir(self._dir1)
            self.fail("make_dir should have failed without 'Overwrite' flag set")
        except saga.Exception, ex:
            pass

        # now, make_dir should work since the 'Overwrite' flag is set
        try:
            d.make_dir(self._dir1, saga.filesystem.Overwrite)
        except saga.Exception, ex:
            self.fail("Unexpected exception: %s" % ex)
            
