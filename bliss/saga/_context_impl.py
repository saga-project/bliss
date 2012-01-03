#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga._attributes_impl import AttributeInterface

class Context(AttributeInterface, object):
    '''Looesely defines a SAGA Context object as defined in GFD.90.
    '''

    SSH      = "SSH"
    '''A security context type based on public/private keys.''' 
    X509     = "X509"
    '''A security context type based on X.509 certificates.'''
    X509_SSH = "X509+SSH"
    '''A security context type for X.509 via SSH.'''
    BigJob = "BigJob"
    '''A security context type for BigJob'''


    #__dict__ = {'_type', '_userkey', '_usercert', '_userproxy'}
  
    def __init__(self):
        '''Constructor'''
        self._type      = None
        self._userid    = None
        self._userpass  = None
        self._usercert  = None
        self._userkey   = None
        self._userproxy = None

        AttributeInterface.__init__(self)
      
        # register properties with the attribute interface 
        self._register_rw_attribute     (name="Type", 
                                         accessor=self.__class__.type) 
        self._register_rw_attribute     (name="UserID", 
                                         accessor=self.__class__.userid)  
        self._register_rw_attribute     (name="UserPass", 
                                         accessor=self.__class__.userpass)  
        self._register_rw_attribute     (name="UserCert", 
                                         accessor=self.__class__.usercert)  
        self._register_rw_attribute     (name="UserKey", 
                                         accessor=self.__class__.userkey)  
        self._register_rw_attribute     (name="UserProxy", 
                                         accessor=self.__class__.userproxy)  

    ######################################################################
    ##
    def __del__(self):
        '''Destructor.'''
        pass

    ######################################################################
    ##
    def __str__(self):
        '''String represenation.
        '''
        return "\n[\n Context Type: %s\n UserID: %s\n UserPass: %s\n UserCert: %s\n UserKey: %s\n UserProxy: %s\n]" % \
                (self.type, self.userid, self.userpass, self.usercert, self.userkey, self.userproxy)

    ######################################################################
    ## Property: type
    def type():
        doc = "Context type."
        def fget(self):
            return self._type
        def fset(self, val):
            self._type = val
        return locals()
    type = property(**type())


    ######################################################################
    ## Property: userid
    def userid():
        doc = "User ID or user name to use."
        def fget(self):
            return self._userid
        def fset(self, val):
            self._userid = val
        return locals()
    userid = property(**userid())

    ######################################################################
    ## Property: userpass
    def userpass():
        doc = "User password (use with care)."
        def fget(self):
            return self._userpass
        def fset(self, val):
            self._userpass = val
        return locals()
    userpass = property(**userpass())

    ######################################################################
    ## Property: usercert
    def usercert():
        doc = "Location of a user certificate."
        def fget(self):
            return self._usercert
        def fset(self, val):
            self._usercert = val
        return locals()
    usercert = property(**usercert())

    ######################################################################
    ## Property: userkey
    def userkey():
        doc = "Location of a user key."
        def fget(self):
            return self._userkey
        def fset(self, val):
            self._userkey = val
        return locals()
    userkey = property(**userkey())

    ######################################################################
    ## Property: userproxy
    def userproxy():
        doc = "Location of a user proxy."
        def fget(self):
            return self._userproxy
        def fset(self, val):
            self._userproxy = val
        return locals()
    userproxy = property(**userproxy())

