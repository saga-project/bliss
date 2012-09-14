#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

class JobID(object):
    '''Represents a SAGA job ID (Not part of GFD.90)
      
       The SAGA :class:`bliss.saga.job.Job` ID is usually considered to be an opaque string, but
       in general is expected to be formatted as::

         '[backend-url]-[native-id]'

       (including brackets!), where 'backend-url' is the contact URL for the job
       manager (:class:`bliss.saga.job.Service`) who 'owns' the job, and 'native-id' is the job
       id as issued and understood by that job manager.

       Bliss exposes those components of the job ID in this class, which allows
       to create new IDs and to parse / split existing IDs.

       Example::

         jd = saga.job.Description()
         jd.executable = "/bin/date"
         jd.arguments  = ["-u", "-R"]

         js = saga.job.Service("fork://localhost/")
         j  = js.create_job(jd)
         j.run()

         print "job id: %s"  % j.job_id

    '''
    
    ######################################################################
    ##
    def __init__(self, service_url, native_id):
        '''Create a new job id.

           :param service_url : The URL of the job service of the job.
           :param native_id:    The native id (a.k.a. backend id) of the job.

           This function will mostly be useful for plugin developers, which
           frequently will have to create valid job IDs.
        '''
        self._service = service_url
        self._native = native_id

    ######################################################################
    ##
    def __str__(self):
        '''String representation.'''
        return "[%s]-[%s]" % (self._service, self._native)

    ######################################################################
    ##
    def service_url():
        doc = "The job id's service url component"
        def fget(self):
            return self._service
        return locals()
    service_url = property(**service_url())

    ######################################################################
    ##
    def native_id():
        doc = "The job ID's native id component"
        def fget(self):
            return self._native
        return locals()
    native_id = property(**native_id())

