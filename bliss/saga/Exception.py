#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


import traceback
import StringIO

def _get_traceback(prefix="\n*** "):
    '''returns the last traceback as a string with a given prefix'''
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    if fp.getvalue() == "None\n":
        return "(No Traceback)"
    else:
        return prefix+fp.getvalue() 

class Error:

    AlreadyExists = 'AlreadyExists'
    AuthenticationFailed = 'AuthenticationFailed'
    AuthorizationFailed = 'AuthorizationFailed'
    BadParameter = 'BadParameter'
    DoesNotExist = 'DoesNotExist'
    IncorrectState = 'IncorrectState'
    IncorrectURL = 'IncorrectURL'
    NoSuccess = 'NoSuccess'
    NotImplemented = 'NotImplemented'
    PermissionDenied = 'PermissionDenied'
    Timeout =  'Timeout'

class Exception(Exception):
       def __init__(self, error, msg):
           self.error     = error
           '''Contains the L{Error} type.'''
           self.msg       = msg
           '''Contains the error message.'''
           self.traceback = _get_traceback()
           '''Contains the traceback (if existent).'''
 
       def __str__(self):
           '''String representation.'''
           string = "SAGA Exception (%s): %s" % (str(self.error), str(self.msg))
           return (string)
