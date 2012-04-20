!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''Bliss (BLiss IS SagaA) is a pragmatic and light-weight implementation of the OGF SAGA standard (GFD.90).
   
   More information can be found at: U{http://saga-project.github.com/bliss}
'''

__author__    = "Ole Christian Weidner, et al."
__copyright__ = "Copyright 2011-2012, Ole Christian Weidner"
__license__   = "MIT"

# Base "look-and-feel packages"
from bliss.saga.Url       import Url 
from bliss.saga.Object    import Object
from bliss.saga.Session   import Session 
from bliss.saga.Context   import Context
from bliss.saga.Exception import Exception 
from bliss.saga.Exception import Error 

# API packages
from bliss.saga           import filesystem
from bliss.saga           import resource
from bliss.saga           import job
