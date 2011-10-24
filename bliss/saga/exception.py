#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


class Error:

    AlreadyExists = 'AlreadyExists'
    AuthenticationFailed = 'AuthenticationFailed'
    AuthorizationFailed = 'AuthorizationFailed'
    BadParameter = 'BadParameter'
    DoesNotExist = 'DoesNotExist'
    IncorrectState = 'IncorrectState'
    IncorrectURL = 'IncorrectURL'
    NoSuccess = 'NoSuccess'
    NotImlemented = 'NotImplemented'
    PermissionDenied = 'PermissionDenied'
    Timeout =  'Timeout'

class Exception(Exception):
       def __init__(self, error, msg):
           self.error = error
           self.msg   = msg
 
       def __str__(self):
           string = "SAGA Exception ({!s}): {!s}".format(str(self.error), str(self.msg))
           return (string)
