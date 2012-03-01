#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''Bliss (BLiss IS SagaA) is a pragmatic, light-weight implementation of the OGF SAGA standard (GFD.90).

   B{ATTENTION:} The bliss.sagacompat module only exists to ensure B{compatibility} with existing SAGA implementations (U{http://www.saga-project.org}) and its use is B{highly discouraged}. Please use the bliss.saga module (U{http://oweidner.github.com/bliss/apidoc/}) instead!
   
   More information can be found at: U{http://oweidner.github.com/bliss}
'''
__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

# Base "look-and-feel packages"
from bliss.saga.exception_impl import Exception as SException
class exception(SException):
    '''Loosely defines a SAGA Exception as defined in GFD.90.
    '''
    pass

from bliss.saga.exception_impl import Error as SError
class error(SError):
    '''Loosely defines a SAGA Error as defined in GFD.90.
    '''
    pass

from bliss.saga.object_impl import Object as SObject
class object(SObject):
    '''Loosely defines a SAGA Object as defined in GFD.90.
    '''
    pass

from bliss.saga.url_impl import Url as SUrl
class url(SUrl):
    '''Loosely defines a SAGA URL as defined in GFD.90.
    '''
    pass

from bliss.saga.session_impl import Session as SSession
class session(SSession):
    '''Loosely defines a SAGA Session as defined in GFD.90.
    '''
    pass

from bliss.saga.context_impl import Context as SContext
class context(SContext):
    '''Loosely defines a SAGA Context as defined in GFD.90.
    '''
    pass

# API packages
from bliss.sagacompat import filesystem
from bliss.sagacompat import job
from bliss.sagacompat import sd
  
