#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

'''SAGA Job Package (compatibility) API.
'''

__author__    = "Ole Christian Weidner"
__email__     = "ole.weidner@me.com"
__copyright__ = "Copyright 2011, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.job._job_api import Job as SJob
class job(SJob):
    '''Loosely defines a SAGA Job as defined in GFD.90.
    '''
    pass

Canceled = SJob.Canceled
Done     = SJob.Done 
Failed   = SJob.Failed
New      = SJob.New
Running  = SJob.Running
Waiting  = SJob.Waiting
Unknown  = SJob.Unknown


from bliss.saga.job._job_api import JobID as SJobID
class job_id(SJobID):
    '''Defines a JobID. This is not part of GFD.90.
    '''
    pass

from bliss.saga.job._container_api import Container as SContainer
class container(SContainer):
    '''Loosely defines a SAGA Job Container. It roughly resembles a GFD.90 task_container.
    '''
    pass

from bliss.saga.job._container_api import WaitMode as SWaitMode
class wait_mode(SWaitMode):
    '''Loosely defines a SAGA WaitMode as defined in GFD.90.
    '''
    pass

from bliss.saga.job._service_api import Service as SService
class service(SService):
    '''Loosely defines a SAGA Job Service as defined in GFD.90.
    '''
    pass

from bliss.saga.job._description_api import Description as SDescription
class description(SDescription):
    '''Loosely defines a SAGA Job Description as defined in GFD.90.
    '''
    pass

