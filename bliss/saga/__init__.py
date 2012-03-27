#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''Bliss (BLiss IS SagaA) is a pragmatic, light-weight 
   implementation of the OGF SAGA standard (GFD.90).
   
   More information can be found at: U{http://oweidner.github.com/bliss}
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

# Base "look-and-feel packages"
from bliss.saga.exception_api import Exception as SException
class Exception(SException):
    '''Loosely defines a SAGA Exception as defined in GFD.90.
    '''
    pass

from bliss.saga.exception_api import Error as SError
class Error(SError):
    '''Loosely defines a SAGA Error as defined in GFD.90.
    '''
    pass

from bliss.saga.object_api import Object as SObject
class Object(SObject):
    '''Loosely defines a SAGA Object as defined in GFD.90.
    '''
    pass

from bliss.saga.url_api import Url as SUrl
class Url(SUrl):
    '''Loosely defines a SAGA URL as defined in GFD.90.
    '''
    pass

from bliss.saga.session_api import Session as SSession
class Session(SSession):
    '''Loosely defines a SAGA Session as defined in GFD.90.
    '''
    pass

from bliss.saga.context_api import Context as SContext
class Context(SContext):
    '''Loosely defines a SAGA Context as defined in GFD.90.
    '''
    pass

# API packages
from bliss.saga           import filesystem
from bliss.saga           import resource
from bliss.saga           import job
from bliss.saga           import sd
  
