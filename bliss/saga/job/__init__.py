# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

''' 
    Job Management
    ==============

    Introduction
    ------------

    The job management API allows to create (via a :class:`bliss.saga.job.Service`) and manage
    :class:`bliss.saga.job.Job` instances. A job is, for the purpose of the SAGA API, an instance
    of a specific application, i.e. one or more processes of a specific
    executable.  

    **Example**::

     # create a job description...
     jd = saga.job.Description()
    
     # ... and fill it with information about the job to be started
     jd.executable = "/usr/local/bin/blast"
     jd.arguments = ["-i", "/data/in/x_42"]
     jd.spmd_variation = "MPI"
     jd.number_of_processes = 64
    
     # the job is to be started via globus on some remote host: contact the
     # respective submission point via its URL: 
     js = saga.job.Service("gram://remote.host.net/")

     # the thus created job service instance accepts the previously created job
     # description and instantiates a job instance.
     j = js.create_job(jd)
    
     # a job is a stateful representation of the remote (set of) process(es).  It
     # can be run, suspended, resumed and waited upon:
     j.run()
     j.suspend()
     j.resume()
     j.wait()

     # during the execution, and after termination, the job can be inspected for
     # state, and for some additional information
     print "id   :  %s"  %  str(j.get_job_id())
     print "state:  %s"  %  str(j.get_state())
     print "descr:  %s"  %  str(j.get_description())


    The above example shows most of the semantics of the job package -- additional
    information, such as about file staging and state model etc., can be found in
    the individual class documentations.


    Bliss Job API Classes
    ---------------------

    .. toctree::
       :maxdepth: 1
    
       Description.rst
       Service.rst
       Job.rst

'''

__author__    = "Ole Christian Weidner, et al."
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.job.Job         import Job
from bliss.saga.job.Job         import JobID
from bliss.saga.job.Service     import Service
from bliss.saga.job.Description import Description

