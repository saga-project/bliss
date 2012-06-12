# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

''' B{Resource Management}

    The resource API provides the means to create, discover, manage and use
    resources, in particular compute and storage resources (L{resource.Compute},
    L{resource.Storage}).  A L{resource.Manager} class acts as resource
    provider, providing stateful resource instances.

    B{Example}::

      # describe the resource requirements
      cd = saga.resource.ComputeDescription()
      cd.slots = 16

      # obtain a handle to a suitable resource, and wait until it is active
      rm = saga.resource.Manager(url)
      cr = rm.create_compute(cd)
      cr.wait(saga.resource.State.Active)

      # submit a large job onto the now active resource
      jd = saga.job.Description()
      jd.executable = '/bin/my/executable'
      jd.number_of_processes = 16

      js = cr.get_job_service()
      j  = js.create_job(jd)
      j.run()
      j.wait()

      # once the job is finished, we do not need the compute resource anymore:
      cr.destroy()


    Note that in the example above, there is no indication on how the resource
    is provided -- that is fully up to the resource manager.  The resource could
    be a existing compute cluster of that size, a advanced reservation slice on
    an even larger cluster, a pilot job slice on a cluster, or a virtual cluster
    provided via IaaS.  That is also the reason why resource instances are
    stateful: for most of the possible backends listed above, resources are not
    necessarily provisioned instantly, and they do have a finite lifetime.

    The resource package also manages storage resources, in a manner very
    similar to example 1.  It does not handle the co-location of compute and
    data resources -- that is left to either the backend, or to the application
    itself.
'''

__author__    = "Ole Christian Weidner, et al."
__copyright__ = "Copyright 2012, Ole Christian Weidner"
__license__   = "MIT"

from bliss.saga.resource.State              import State
from bliss.saga.resource.Manager            import Manager
from bliss.saga.resource.Compute            import Compute
from bliss.saga.resource.ComputeDescription import ComputeDescription 
from bliss.saga.resource.StorageDescription import StorageDescription
from bliss.saga.resource.Storage            import Storage
