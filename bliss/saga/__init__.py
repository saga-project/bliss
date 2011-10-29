#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

''' Bliss.saga is a partial and rather 'laissez-faire' implementation of the OGF SAGA standard (GFD.90).
   
    More information can be found at: U{http://oweidner.github.com/bliss}
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.exception import Exception, Error
from bliss.saga.url       import Url
from bliss.saga           import job  
