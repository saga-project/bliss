#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from urlparse import urlparse

from bliss.saga.object import Object as SAGAObject

class Url(SAGAObject):
    '''Looesely defines a SAGA Url class as defined in GFD.90.'''

    def __init__(self, urlstring=''):
        '''Construct a new Url from a string'''
        SAGAObject.__init__(self, SAGAObject.Url)

        self._urlobj  = urlparse(urlstring)
        
        # retarded workaround for older urlparse implementations
        # that support only a fixed set of schemes (e.g., no 'fork://')
        if self._urljob.scheme != "http":
            oldscheme = self._urlobj.scheme        
            self._urlobj.scheme = "http"
            self._urlobj = urlparse(str(self._urlobj))
            self._urlobj.scheme = oldscheme
        
        self.scheme   = self._urlobj.scheme
        assert(self.scheme == oldscheme)

        self.host     = self._urlobj.netloc
        self.path     = self._urlobj.path
        self.params   = self._urlobj.params
        self.quey     = self._urlobj.query
        self.fragment = self._urlobj.fragment

        # legacy support
        self.url      = self._urlobj.geturl()

    def __del__(self):
        '''Destructor (tear-down the Url object).'''

    def __str__(self):
        '''String representation'''
        return self._urlobj.geturl()

    @property
    def scheme(self):
        '''The scheme part of the Url.'''

        def fget(self):
            return self.scheme

        def fset(self, scheme):
            self.scheme = scheme

    @property
    def host(self):
        '''The host part of the Url (Warning: currenlty returns "url.netloc")'''

        def fget(self):
            return self.host

        def fset(self, host):
            self.host = host

    @property
    def path(self):
        '''The path part of the Url.'''

        def fget(self):
            return self.path

        def fset(self, path):
            self.path = path

    @property
    def params(self):
        '''The params part of the Url.'''

        def fget(self):
            return self.params

        def fset(self, params):
            self.params = params

    @property
    def query(self):
        '''The query part of the Url.'''

        def fget(self):
            return self.query

        def fset(self, query):
            self.query = query

    @property
    def fragment(self):
        '''The fragment part of the Url.'''

        def fget(self):
            return self.fragment

        def fset(self, fragment):
            self.fragment = fragment
