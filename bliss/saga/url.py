#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from urlparse import urlparse

class Url:
    '''Defines a SAGA Url class'''
    def __init__(self, urlstring=''):
        '''Construct a new Url from a string'''
        self._urlobj  = urlparse(urlstring)
        self.scheme   = self._urlobj.scheme
        self.host     = self._urlobj.netloc
        self.path     = self._urlobj.path
        self.params   = self._urlobj.params
        self.quey     = self._urlobj.query
        self.fragment = self._urlobj.fragment

        # legacy support
        self.url      = self._urlobj.geturl()

    def __str__(self):
        '''String representation'''
        return self._urlobj.geturl()
