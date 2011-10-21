#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object

class Service(Object):
    '''Represents a SAGA job service as defined in GFD.90'''
    def __init__(self, url=None):
        '''Construct a new job service object'''
        Object.__init__(self)

    def create_job(self, job_description):
        '''Create a new job object from the given job description'''

    def get_job(self, job_id):
        '''Return the job object from the given job id'''

    def list(self):
        '''List all jobs known or managed by this service'''

