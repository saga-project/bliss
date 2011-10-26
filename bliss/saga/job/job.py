#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

import copy
from bliss.saga.object import Object
from bliss.saga import exception


class Job(Object):

    # possible job states
    Canceled = "Canceled"
    Done     = "Done"
    Failed   = "Failed"
    New      = "New"
    Running  = "Running"
    Unknown  = "Unknown"

    '''Represents a SAGA job as defined in GFD.90'''
    def __init__(self):
        '''[NOT IMPLEMENTED] Constructor'''
        Object.__init__(self, Object.type_saga_job_job)

    def _init_from_service__(self, service_obj, job_desc):
        '''Constructor'''
        self.service = service_obj
        self.url = service_obj.url
        self._job_description = job_desc

        self._plugin = Object._get_plugin(self) # throws 'NoSuccess' on error
        self._plugin.register_job_object(job_obj=self, service_obj=self.service)
        self._logger.info("Object bound to plugin {!s}".format(repr(self._plugin)))


    def __del__(self):
        if self._plugin is not None:
            self._plugin.unregister_job_object(self)
        else:
            pass # can't throw here

    def get_stderr(self):
        '''[NOT IMPLEMENTED] Return a file object representing the stderr stream of the spawned job'''
        raise exception.Exception(exception.Error.NotImplemented, "Bliss doesn't suppport get_stderr()")

    def get_stdout(self):
        '''[NOT IMPLEMENTED] Return a file object representing the stdout stream of the spawned job'''
        raise exception.Exception(exception.Error.NotImplemented, "Bliss doesn't suppport get_stdout()")

    def get_description(self):
        '''Return the job description this job was created from'''
        if self._plugin is not None:
            return self._job_description
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")

    def get_state(self):
        '''Return the current state of the job'''
        if self._plugin is not None:
            return self._plugin.job_get_state(self)
            return None
        else:
            raise exception.Exception(exception.Error.NoSuccess, "Object not bound to a plugin")


