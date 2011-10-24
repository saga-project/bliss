#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object
from bliss.saga.url import Url


class Description(Object):
    '''Represents a SAGA job description as defined in GFD.90'''
    def __init__(self):
        Object.__init__(self, Object.type_saga_job_description)        

