#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


class Context():
    '''Looesely defines a SAGA Context object as defined in GFD.90.'''

    Default = "Default"
    '''The default (None) security context.'''
    SSH     = "SSH"
    '''A security context based on public/private keys.''' 
    X509    = "X509"
    '''A security context based on X.509 certificates.'''

    def __init__(self):
        '''Construct a new Context.'''
        self.type      = self.Default
        self.usercert  = ""
        self.userkey   = ""
        self.userproxy = ""

    def __del__(self):
        '''Destructor (tear-down the Context object).'''

    @property
    def type(self):
        '''Context type.'''

        def fget(self):
            return self.type

        def fset(self, t):
            self.type = t

    @property
    def userkey(self):
        '''Location of a user key.'''

        def fget(self):
            return self.userkey

        def fset(self, userkey):
            self.userkey = userkey

    @property
    def usercert(self):
        '''Location of a user certificate.'''

        def fget(self):
            return self.usercert

        def fset(self, usercert):
            self.usercert = usercert 

    @property
    def userproxy(self):
        '''Location of an existing certificate proxy.'''

        def fget(self):
            return self.userproxy

        def fset(self, userproxy):
            self.userproxy = userproxy 
