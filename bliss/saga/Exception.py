#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"


import traceback
import StringIO

def _get_traceback(prefix="\n*** "):
    # FIXME: prefix by default should be empty
    '''returns the last traceback as a string with a given prefix'''
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    if fp.getvalue() == "None\n":
        return "(No Traceback)"
    else:
        return prefix+fp.getvalue() 


class Error:

    # entity errors
    AlreadyExists        = 'AlreadyExists'
    ''' The entity to be created already exists. '''

    DoesNotExist         = 'DoesNotExist'
    ''' An operation tried to access a non-existing entity. '''

    IncorrectState       = 'IncorrectState'
    ''' The operation is not allowed on the entity in its current state. '''

    
    # parameter errors
    BadParameter         = 'BadParameter'
    ''' A given parameter is out of bound or ill formatted. '''

    IncorrectURL         = 'IncorrectURL'
    ''' The given URL could not be interpreted, for example due to an incorrect schema.''' 


    # security errors
    AuthenticationFailed = 'AuthenticationFailed'
    ''' The backend could not establish a valid identity. '''

    AuthorizationFailed  = 'AuthorizationFailed'
    ''' The used identity is not allowed to use the backend, '''

    PermissionDenied     = 'PermissionDenied'
    ''' The used identity is not permitted to perform the requested operation.  '''


    # implementation / backend errors
    Timeout              =  'Timeout'
    ''' The interaction with the backend times out. '''

    NoSuccess            = 'NoSuccess'
    ''' Some other error occurred. '''

    NotImplemented       = 'NotImplemented'
    ''' Bliss does not (yet) implement this method, for the backend in use. '''



class Exception(Exception):
       ''' The Exception class encapsulates information about error conditions
       encountered by Bliss.

       Additionally to the error message (e.msg), the exception also provides
       a trace to the code location where the error condition got raised
       (e.traceback), and an error code (e.error) which identifies the type of
       error encountered.  That error code reduces the need to parse the error
       message, and helps the application to react on specific conditions.

       Example::

         dir = saga..filesystem.Directory ("ssh://remote.host.net/data/")

         try :
           dir.mkdir ('stage')
           dir.cd ('stage/')
         except Exception as e :
           if e.error == saga.Error.AlreadyExists :
             # that's ok
             dir.cd ('stage/')
           else
             # oy, can't do that - so lets use /tmp
             dir.cd ('/tmp/')
           fi

       '''
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

