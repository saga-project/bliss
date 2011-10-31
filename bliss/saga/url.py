#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import urlparse 

from bliss.saga.object import Object as SAGAObject

urlparse.uses_netloc.append("fork")
urlparse.uses_fragment.append("fork")

class Url(SAGAObject):
    '''Looesely defines a SAGA Url class as defined in GFD.90.'''

    __slots__ = ('_urlobj', 'scheme', 'host', 'port', 'path', 'params', 'query', 'fragment', 'url')

    def __init__(self, urlstring=''):
        '''Construct a new Url from a string'''

        SAGAObject.__init__(self, SAGAObject.Url)

        self._urlobj  = urlparse.urlparse(urlstring)
        
        if self._urlobj.netloc.find(":") > 0:
            (host,port) = self._urlobj.netloc.split(":")
        else:
            host = self._urlobj.netloc
            port = ""

        self.scheme   = self._urlobj.scheme
        '''The scheme part of the Url.'''
        self.host     = host
        '''The host part of the Url.'''
        self.port     = port
        '''The port part of the Url.'''
        self.path     = self._urlobj.path
        '''The path part of the Url.'''
        self.params   = self._urlobj.params
        '''The params part of the Url.'''
        self.query    = self._urlobj.query
        '''The query part of the Url.'''
        self.fragment = self._urlobj.fragment
        '''The fragment part of the Url.'''
        self.url      = self._urlobj.geturl()
        '''The Url as string (same as __str__).'''

    def __del__(self):
        '''Destructor (tear-down the Url object).'''

    def __str__(self):
        '''Return Url as string.'''
        return self.url

    def get_scheme(self):
        '''Legacy method: return the 'scheme' property.'''
        return self.scheme

    def set_scheme(self, val):
        '''Legacy method: set the 'scheme' property.'''
        self.scheme = val

    def get_host(self):
        '''Legacy method: return the 'host' property.'''
        return self.scheme

    def set_host(self, val):
        '''Legacy method: set the 'host' property.'''
        self.host = val

    def get_port(self):
        '''Legacy method: return the 'port' property.'''
        return self.port

    def set_port(self, port):
        '''Legacy method: set the 'port' property.'''
        self.port = val

    def get_fragment(self):
        '''Legacy method: return the 'fragment' property.'''
        return self.fragment

    def set_fragment(self, val):
        '''Legacy method: set the 'fragment' property.'''
        self.fragment = val

    def get_path(self):
        '''Legacy method: return the 'path' property.'''
        return self.path

    def set_path(self, val):
        '''Legacy method: set the 'path' property.'''
        self.path = val

    def get_query(self):
        '''Legacy method: return the 'query' property.'''
        return self.quey

    def set_query(self, query):
        '''Legacy method: set the 'query' property.'''
        self.query = val
