# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

class Error:
    """The SAGA error types.

       SAGA error types are used by the :class:`bliss.saga.Exception` class to 
       indicate the type of error that has occured.
    """

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
    ''' Bliss does not implement this method. '''
