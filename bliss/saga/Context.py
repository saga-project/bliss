# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

import logging
import os.path

from bliss.saga.Object import Object 

from bliss.saga.Attributes import AttributeInterface
from bliss.saga.Exception import Exception as SAGAException
from bliss.saga.Exception import Error as SAGAError

class Context(AttributeInterface, Object):
    '''Looesely defines a SAGA Context object as defined in GFD.90.
    '''

    SSH      = "SSH"
    '''A security context type based on public/private keys.''' 
    EC2      = "EC2"
    '''A security context type for Eucalyptus / EC2 applications.'''
    X509     = "X509"
    '''A security context type based on X.509 certificates.'''
    
    ######################################################################
    ## 
    def __init__(self):
        '''Constructor'''

        Object.__init__(self, objtype=Object.Type.Context, apitype=Object.Type.BaseAPI)
        AttributeInterface.__init__(self)

        self._type      = None
        self._userid    = None
        self._userpass  = None
        self._usercert  = None
        self._userkey   = None
        self._userproxy = None

      
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

        self.__logger = logging.getLogger(self.__class__.__name__+'('+str(hex(id(self)))+')')


    ######################################################################
    ##
    def _log_and_raise_if_file_doesnt_exist(self, filename):
        '''Logs and raises an error if "filename" doesn't exist'''
        msg = "File '%s' doesn't exist." % (filename)
        self.__logger.error(msg)
        raise SAGAException(msg, SAGAError.DoesNotExist)

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
            if not os.path.isfile(val):
                self._log_and_raise_if_file_doesnt_exist(val)
            else:
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
            if not os.path.isfile(val):
                self._log_and_raise_if_file_doesnt_exist(val)
            else:
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
            if not os.path.isfile(val):
                self._log_and_raise_if_file_doesnt_exist(val)
            else: 
                self._userproxy = val
        return locals()
    userproxy = property(**userproxy())

