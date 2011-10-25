#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.object import Object

class Job(Object):
    '''Represents a SAGA job as defined in GFD.90'''
    def __init__(self, url, job_description):
        '''Constructor'''
        self.url = url
        self.job_description = job_description

        Object.__init__(self, Object.type_saga_job_job)
        self.plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self.logger.info("Object bound to plugin {!s}".format(repr(self.plugin)))

        self.plugin.register_job_object(self)

    def __del__(self):
        print "good night"
        self.plugin.unregister_job_object(self)

