#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Job Package API.
'''

__author__    = "Ole Christian Weidner"
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.job.job_api import Job as SJob
class Job(SJob):
    '''Loosely defines a SAGA Job as defined in GFD.90.
    '''
    pass

from bliss.saga.job.job_api import JobID as SJobID
class JobID(SJobID):
    '''Defines a JobID. This is not part of GFD.90.
    '''
    pass

from bliss.saga.job.container_api import Container as SContainer
class Container(SContainer):
    '''Loosely defines a SAGA Job Container. It roughly resembles a GFD.90 task_container.
    '''
    pass

from bliss.saga.job.container_api import WaitMode as SWaitMode
class WaitMode(SWaitMode):
    '''Loosely defines a SAGA WaitMode as defined in GFD.90.
    '''
    pass

from bliss.saga.job.service_api import Service as SService
class Service(SService):
    '''Loosely defines a SAGA Job Service as defined in GFD.90.
    '''
    pass

from bliss.saga.job.description_api import Description as SDescription
class Description(SDescription):
    '''Loosely defines a SAGA Job Description as defined in GFD.90.
    '''
    pass

