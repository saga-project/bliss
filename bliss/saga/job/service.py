#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object
from bliss.saga.url import Url

class Service(Object):
    '''Represents a SAGA job service as defined in GFD.90'''
    def __init__(self, url):
        '''Construct a new job service object'''
        
        if(type(url) == str):
            Object.url = Url(str(url))
        else:
            # assume it's a URL object
            Object.url = url

        Object.__init__(self)
        self.plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self.logger.info("Bound to plugin instance {!s}".format(repr(self.plugin)))

    def create_job(self, job_description):
        '''Create a new job object from the given job description'''
        return self.plugin.create_job(job_description)

    def get_job(self, job_id):
        '''Return the job object from the given job id'''
        return self.plugin.get_job(job_id)

    def list(self):
        '''List all jobs known or managed by this service'''
        return self.plugin.list()

