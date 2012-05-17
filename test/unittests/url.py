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
class UrlTests(unittest.TestCase):
    """
    Tests for the saga.Url class
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    ###########################################################################
    #
    def test_url_compatibility(self):
    
        u1 = saga.Url("ssh://user:pwd@hostname.domain:9999/path")

        if u1.scheme != "ssh":
            self.fail("unexpected value for scheme")

        if u1.username != "user":
            self.fail("unexpected value for username")

        if u1.password != "pwd":
            self.fail("unexpected value for password")

        if u1.host != "hostname.domain":
            self.fail("unexpected value for host")

        if u1.port != int(9999):
            self.fail("unexpected value for port")

    ###########################################################################
    #
    def test_url_scheme_issue(self):
    
        u1 = saga.Url("unknownscheme://user:pwd@hostname.domain:9999/path")
        if u1.scheme != "unknownscheme":
            self.fail("unexpected value for scheme")

        if u1.username != "user":
            self.fail("unexpected value for username")

        if u1.password != "pwd":
            self.fail("unexpected value for password")

        if u1.host != "hostname.domain":
            self.fail("unexpected value for host")

        if u1.port != int(9999):
            self.fail("unexpected value for port")
